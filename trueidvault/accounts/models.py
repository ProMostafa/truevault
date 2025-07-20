import secrets
from django.db import models
from django.utils import timezone
import hashlib


# Models
class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    @property
    def is_authenticated(self):
        return True  # Treat all Service instances as authenticated

    def __str__(self):
        return self.name


class ServicePermission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class APIKey(models.Model):
    TIER_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )
    key = models.CharField(max_length=64, unique=True, editable=False)
    permissions = models.ManyToManyField(ServicePermission, blank=True)
    tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default='free'
    )

    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="Optional expiration date"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        # Generate a secure random key and hash it for storage
        raw_key = secrets.token_urlsafe(32)
        hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
        return hashed_key

    def __str__(self):
        status = "Expired" if self.is_expired() else "Active"
        return f"{self.service.name} - {status}"


