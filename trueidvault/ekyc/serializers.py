from rest_framework import serializers


class NationalIdRequestSerializer(serializers.Serializer):
    """Serializer for national ID validation request."""
    national_id = serializers.CharField(max_length=14, min_length=14)


class NationalIdResponseSerializer(serializers.Serializer):
    """Serializer for national ID validation response."""
    is_valid = serializers.BooleanField()
    birth_year = serializers.IntegerField(required=False)
    birth_date = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    serial_number = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    governorate = serializers.CharField(required=False)
