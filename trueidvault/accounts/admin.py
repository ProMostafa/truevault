from django.contrib import admin
from .models import Service, APIKey, ServicePermission


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']


@admin.register(ServicePermission)
class ServicePermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    list_filter = ['code']


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['service', 'key', 'is_active', 'expires_at', 'created_at']
    readonly_fields = ['key', 'created_at']
    list_filter = ['is_active', 'expires_at']
