# myapp/throttles.py
from rest_framework.throttling import SimpleRateThrottle

from .models import APIKey


Free = APIKey.TIER_CHOICES[0][0]
Premium = APIKey.TIER_CHOICES[1][0]


class FreeAPIKeyThrottle(SimpleRateThrottle):
    scope = 'free_api_key'

    def get_cache_key(self, request, view):        
        api_key = request.auth  # APIKey object from authentication
        if (
            api_key and isinstance(api_key, APIKey)
            and api_key.tier == Free
            and api_key.is_active and not api_key.is_expired()
        ):  
            print(">>>>>>>>>>>>>>>>>>>> api_key", api_key)
            return f'throttle_{self.scope}_{api_key.key}'
        print(">>>>>>>>>>>>>>>>>>>> api_key", api_key)
        return None  # Skip throttling if not a free API key or invalid


class PremiumAPIKeyThrottle(SimpleRateThrottle):
    scope = 'premium_api_key'

    def get_cache_key(self, request, view):
        api_key = request.auth  # APIKey object from authentication
        if (
            api_key and isinstance(api_key, APIKey) 
            and api_key.tier == Premium 
            and api_key.is_active and not api_key.is_expired()
        ):
            return f'throttle_{self.scope}_{api_key.key}'
        return None  # Skip throttling if not a premium API key or invalid
