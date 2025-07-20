# core/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("API-Key")
        print(">>>>>>>>>>>>>>>>>>>> api_key", api_key)
        if not api_key:
            raise AuthenticationFailed('API key required')
        try:
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        if not api_key_obj.is_active:
            raise AuthenticationFailed("API key is inactive")

        if api_key_obj.is_expired():
            raise AuthenticationFailed("API key has expired")
        return (api_key_obj.service, api_key_obj)
