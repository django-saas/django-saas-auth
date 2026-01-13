from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'saas_auth'
    verbose_name = 'SaaS Authentication'

    def ready(self):
        __import__('saas_auth.registry.default_perms')
