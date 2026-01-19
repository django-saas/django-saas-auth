from django.core.signals import setting_changed
from saas_base.settings import saas_settings
from saas_base.settings import BaseSettings


class AuthSettings(BaseSettings):
    SETTINGS_KEY = 'SAAS_AUTH'
    DEFAULT_SETTINGS = {
        'ENABLE_GRAVATAR': False,
        'GRAVATAR_OPTIONS': {'size': 400, 'default': 'identicon'},
        'LOCATION_RESOLVER': {
            'backend': 'saas_auth.location.cloudflare.CloudflareBackend',
        },
        'SESSION_RECORD_INTERVAL': 300,
        'MFA_STEP_UP_AUTH': 300,  # skip for 5 minutes
        'TOTP_DIGITS': 6,
        'TOTP_ALGORITHM': 'SHA1',
        'TOTP_PERIOD': 30,
        'TOTP_ISSUER': '',
        'TOTP_LABEL_FIELD': 'username',
    }
    IMPORT_SETTINGS = [
        'LOCATION_RESOLVER',
    ]

    @property
    def totp_issuer(self) -> str:
        if self.TOTP_ISSUER:
            return self.TOTP_ISSUER
        site = saas_settings.SITE
        return site['name']


auth_settings = AuthSettings()
setting_changed.connect(auth_settings.listen_setting_changed)
