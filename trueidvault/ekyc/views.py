from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    NationalIdRequestSerializer,
    NationalIdResponseSerializer
)

from .validators import IDValidator
from accounts.permissions import HasNationalIdPermission
from accounts.throttling import FreeAPIKeyThrottle, PremiumAPIKeyThrottle
from accounts.authentication import APIKeyAuthentication
from .tasks import log_api_call


class ValidateNationalIdView(APIView):
    """API endpoint to validate Egyptian national ID and extract data."""
    authentication_classes = [APIKeyAuthentication]
    # throttle_classes = [APIKeyRateThrottle]
    throttle_classes = [
        AnonRateThrottle,
        FreeAPIKeyThrottle,
        PremiumAPIKeyThrottle
    ]
    permission_classes = [HasNationalIdPermission]

    @swagger_auto_schema(
        operation_description="Validate an Egyptian National ID and extract data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'national_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Egyptian National ID (14 digits)'
                ),
            },
            required=['national_id'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Status message'),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_valid': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                        },
                    ),
                },
                example={
                    'id_number': '12345678901234',
                    'is_valid': True,
                    'birth_date': '1990-01-01',
                    'birth_year': '1990',
                    'gender': 'Male',
                    'serial_number': '901234'
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                },
                example={
                    'detail': 'Invalid National ID provided',
                },
            ),
        },
    )
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
