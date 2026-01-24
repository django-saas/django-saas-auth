from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema


class FixedSessionRecordListEndpoint(OpenApiViewExtension):
    target_class = 'saas_auth.endpoints.sessions.SessionRecordListEndpoint'

    def view_replacement(self):
        class SessionRecordListEndpoint(self.target_class):
            @extend_schema(tags=['Session'], summary='List user sessions')
            def get(self, *args, **kwargs):
                pass

        return SessionRecordListEndpoint


class FixedSessionRecordItemEndpoint(OpenApiViewExtension):
    target_class = 'saas_auth.endpoints.sessions.SessionRecordItemEndpoint'

    def view_replacement(self):
        class SessionRecordItemEndpoint(self.target_class):
            @extend_schema(tags=['Session'], summary='Retrieve a user session')
            def get(self, *args, **kwargs):
                pass

            @extend_schema(tags=['Session'], summary='Delete a user session')
            def delete(self, *args, **kwargs):
                pass

        return SessionRecordItemEndpoint


class FixedUserTokenListEndpoint(OpenApiViewExtension):
    target_class = 'saas_auth.endpoints.tokens.UserTokenListEndpoint'

    def view_replacement(self):
        class UserTokenListEndpoint(self.target_class):
            @extend_schema(tags=['Token'], summary='List user tokens')
            def get(self, *args, **kwargs):
                pass

            @extend_schema(tags=['Token'], summary='Create a user token')
            def post(self, *args, **kwargs):
                pass

        return UserTokenListEndpoint


class FixedUserTokenItemEndpoint(OpenApiViewExtension):
    target_class = 'saas_auth.endpoints.tokens.UserTokenItemEndpoint'

    def view_replacement(self):
        class UserTokenItemEndpoint(self.target_class):
            @extend_schema(tags=['Token'], summary='Delete a user token')
            def delete(self, *args, **kwargs):
                pass

        return UserTokenItemEndpoint
