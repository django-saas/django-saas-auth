from rest_framework import serializers
from saas_base.registry import perm_registry
from saas_auth.models import Session, UserToken


class SessionSerializer(serializers.ModelSerializer):
    current_session = serializers.SerializerMethodField()

    class Meta:
        model = Session
        exclude = ('user', 'session_key')

    def get_current_session(self, obj):
        request = self.context['request']
        return request.session.session_key == obj.session_key


class UserTokenSerializer(serializers.ModelSerializer):
    last_used = serializers.IntegerField(source='get_last_used', read_only=True, allow_null=True)

    class Meta:
        model = UserToken
        exclude = ['user']
        extra_kwargs = {
            'key': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate_scope(self, value: str):
        scopes = value.split(' ')
        defined_scopes = perm_registry.get_scope_keys()
        for scope in scopes:
            if scope not in defined_scopes:
                raise serializers.ValidationError(f'Scope {scope} is not defined')
        return value
