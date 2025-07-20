from rest_framework.permissions import BasePermission
from .models import APIKey


class HasServicePermission(BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        api_key = request.auth
        if not isinstance(api_key, APIKey):
            return False
        if self.required_permission is None:
            return True

        return api_key.permissions.filter(
            code=self.required_permission
        ).exists()


class HasNationalIdPermission(HasServicePermission):
    required_permission = "validate-national-id"
