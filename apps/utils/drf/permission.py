from rest_framework.permissions import BasePermission
from user.models import UserStatus


class IsActiveAuthenticated(BasePermission):
    """
    激活用户
    """
    def has_permission(self, request, view):
        user_obj = request.user
        if user_obj:
            if user_obj.status == UserStatus.ENABLE:
                return True
        return False
