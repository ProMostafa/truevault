from django.contrib import admin
from .models import ApiCallLog


@admin.register(ApiCallLog)
class ApiCallLogAdmin(admin.ModelAdmin):
    list_display = ("api_key", "endpoint", "response_status", "timestamp")
    list_filter = ("response_status", "timestamp")
    search_fields = ("api_key", "endpoint")