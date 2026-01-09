from django.db import models
from django.conf import settings
from saas_auth.settings import auth_settings
from saas_auth.util import gen_gravatar_url


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        editable=False,
    )
    picture = models.URLField(blank=True, null=True)
    region = models.CharField(blank=True, null=True, max_length=4)
    locale = models.CharField(blank=True, null=True, max_length=10)

    class Meta:
        db_table = 'saas_auth_user_profile'

    @property
    def avatar(self):
        if self.picture:
            return self.picture

        if not auth_settings.ENABLE_GRAVATAR:
            return None

        name = self.user.get_full_name() or self.user.username
        return gen_gravatar_url(self.user.email, name, **auth_settings.GRAVATAR_OPTIONS)

    @avatar.setter
    def avatar(self, value):
        self.picture = value
