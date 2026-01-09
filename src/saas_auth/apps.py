from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'saas_auth'
    verbose_name = 'SaaS Authentication'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from saas_base.endpoints.user import UserEndpoint
        from .serializers import UserSerializer

        UserEndpoint.serializer_class = UserSerializer
