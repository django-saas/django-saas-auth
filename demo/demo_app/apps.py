from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    name = 'demo.demo_app'

    def ready(self):
        # register default roles and scopes
        from saas_base.registry import default_roles, default_scopes  # noqa
