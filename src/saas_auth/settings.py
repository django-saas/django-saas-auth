from functools import cached_property

from django.core.signals import setting_changed
from django.utils.module_loading import import_string
from saas_base.settings import BaseSettings


class AuthSettings(BaseSettings):
    SETTINGS_KEY = 'SAAS_AUTH'
    DEFAULT_SETTINGS = {
        'LOCATION_RESOLVER': {
            'backend': 'saas_auth.location.cloudflare.CloudflareBackend',
        },
        'TOKEN_KEY_GENERATOR': 'saas_auth.util.gen_token_key',
        'USER_TOKEN_RECORD_INTERVAL': 300,
        'SESSION_RECORD_INTERVAL': 300,
    }
    IMPORT_SETTINGS = [
        'LOCATION_RESOLVER',
    ]

    @cached_property
    def generate_token(self):
        return import_string(self.TOKEN_KEY_GENERATOR)


auth_settings = AuthSettings()
setting_changed.connect(auth_settings.listen_setting_changed)
