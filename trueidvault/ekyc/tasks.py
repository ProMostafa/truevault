from celery import shared_task
from .models import ApiCallLog


@shared_task
def log_api_call(api_key: str, endpoint: str, request_data_hash: str,
                 response_status: int, user_ip: str = None):
    """Asynchronously log API calls for tracking."""
    ApiCallLog.objects.create(
        api_key=api_key,
        endpoint=endpoint,
        request_data_hash=request_data_hash,
        response_status=response_status,
        user_ip=user_ip,
    )
