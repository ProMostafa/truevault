from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from .serializers import (
    NationalIdRequestSerializer,
    NationalIdResponseSerializer
)
from .validators import IDValidator
# from accounts.authentication import APIKeyAuthentication
from accounts.permissions import HasNationalIdPermission
from accounts.throttling import FreeAPIKeyThrottle, PremiumAPIKeyThrottle
from .tasks import log_api_call


class ValidateNationalIdView(APIView):
    """API endpoint to validate Egyptian national ID and extract data."""

    # authentication_classes = [APIKeyAuthentication]
    # throttle_classes = [APIKeyRateThrottle]
    throttle_classes = [
        AnonRateThrottle,
        FreeAPIKeyThrottle,
        PremiumAPIKeyThrottle
    ]
    permission_classes = [HasNationalIdPermission]

    def post(self, request):
        serializer = NationalIdRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        national_id = serializer.validated_data["national_id"]
        result = IDValidator.validate_egyptian_national_id(national_id)

        log_api_call.delay(
            api_key=request.auth.key,
            endpoint=self.request.path,
            request_data_hash=IDValidator.hash_input(national_id),
            response_status=status.HTTP_200_OK
            if result["is_valid"] else status.HTTP_400_BAD_REQUEST,
            user_ip=self.request.META.get("REMOTE_ADDR"),
        )

        response_serializer = NationalIdResponseSerializer(data=result)
        response_serializer.is_valid(raise_exception=True)
        return Response(
            response_serializer.data,
            status=(
                status.HTTP_200_OK
                if result["is_valid"]
                else status.HTTP_400_BAD_REQUEST
            ),
        )
