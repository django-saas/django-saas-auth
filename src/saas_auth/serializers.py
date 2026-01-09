from django.contrib.auth import get_user_model
from rest_framework import serializers
from saas_base.drf.serializers import FlattenModelSerializer
from .models import Session, UserProfile, UserToken


class SessionSerializer(serializers.ModelSerializer):
    current_session = serializers.SerializerMethodField()

    class Meta:
        model = Session
        exclude = ('user', 'session_key')

    def get_current_session(self, obj):
        request = self.context['request']
        return request.session.session_key == obj.session_key


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        exclude = ('user', 'picture')


class UserSerializer(FlattenModelSerializer):
    profile = UserProfileSerializer()
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions']
        flatten_fields = ['profile']


class UserTokenSerializer(serializers.ModelSerializer):
    last_used = serializers.IntegerField(source='get_last_used', read_only=True, allow_null=True)

    class Meta:
        model = UserToken
        exclude = ['user']
        extra_kwargs = {
            'key': {'read_only': True},
            'created_at': {'read_only': True},
        }
