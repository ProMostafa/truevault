from django.db import models


class ApiCallLog(models.Model):
    """Model to track API calls for usage monitoring."""
    api_key = models.CharField(max_length=100, db_index=True)
    endpoint = models.CharField(max_length=255)
    request_data_hash = models.CharField(max_length=64)  # SHA-256 hash
    response_status = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['api_key', 'timestamp']),
        ]

    def __str__(self) -> str:
        return f"{self.api_key} - {self.endpoint} - {self.timestamp}"