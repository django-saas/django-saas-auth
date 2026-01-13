from __future__ import annotations

import uuid
import string
import secrets
from django.db import models, transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from saas_base.db.fields import EncryptedField


class MFASettings(models.Model):
    class Methods(models.IntegerChoices):
        TOTP = 1, 'totp'
        PASSKEY = 2, 'webauthn'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='mfa_settings',
    )
    is_totp_enabled = models.BooleanField(default=False)
    is_webauthn_enabled = models.BooleanField(default=False)
    last_used_at = models.DateTimeField(null=True)
    last_used_method = models.SmallIntegerField(
        choices=Methods.choices,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'saas_auth_mfa_settings'


class TOTPDevice(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='totp_device',
    )
    secret_key = EncryptedField()
    confirmed_at = models.DateTimeField(null=True)
    last_used_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'saas_auth_mfa_totp'

    @classmethod
    def create_device(cls, user) -> 'TOTPDevice':
        secret_key = secrets.token_bytes(20)
        return cls.objects.create(user=user, secret_key=secret_key)


class WebAuthnDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='webauthn_devices')
    name = models.CharField(max_length=64)
    credential_id = models.CharField(max_length=1024, unique=True, db_index=True)
    public_key = models.TextField()
    sign_count = models.BigIntegerField(default=0)
    transports = models.CharField(max_length=255, default='', blank=True)
    last_used_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'saas_auth_mfa_passkey'


class MFABackupCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mfa_backup_codes')
    code = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'saas_auth_mfa_codes'
        indexes = [
            models.Index(
                fields=['user'],
                name='idx_mfa_active_codes',
                condition=models.Q(used_at__isnull=True),
            ),
        ]

    @classmethod
    def generate_backup_codes(cls, user, total: int = 10) -> list[str]:
        alphabet = string.ascii_uppercase + string.digits
        alphabet = alphabet.translate(str.maketrans('', '', '0OI1'))

        codes = [''.join(secrets.choice(alphabet) for _ in range(10)) for _ in range(total)]
        with transaction.atomic():
            for code in codes:
                cls.objects.create(user=user, code=make_password(code))
        return codes

    @classmethod
    def verify_backup_code(cls, user, code: str) -> bool:
        for obj in cls.objects.filter(user=user, used_at__isnull=True).all():
            if obj.check_code(code):
                obj.used_at = timezone.now()
                obj.save()
                return True
        return False

    def check_code(self, code: str) -> bool:
        return check_password(code, self.code)
