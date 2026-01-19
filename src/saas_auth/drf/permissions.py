import time
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from saas_auth.models import MFASettings
from saas_auth.settings import auth_settings


class NotUseToken(IsAuthenticated):
    """This permission is designed for internal use"""

    def has_permission(self, request, view):
        if request.auth:
            return False
        return super().has_permission(request, view)


class IsRecentVerified(BasePermission):
    def has_permission(self, request, view):
        try:
            setting = MFASettings.objects.get(user=request.user)
        except MFASettings.DoesNotExist:
            # user doesn't configured MFA
            return True

        # user doesn't enable MFA
        if not setting.is_enabled:
            return True

        mfa_verified_at = getattr(request, 'mfa_verified_at', None)
        if not mfa_verified_at:
            return False

        return time.time() - mfa_verified_at < auth_settings.MFA_STEP_UP_AUTH
