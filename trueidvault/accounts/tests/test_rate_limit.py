
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from accounts.models import APIKey, Service, ServicePermission


class FreeRateLimitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("validate_national_id")
        service = Service.objects.create(name="Service B")
        national_id_permission = ServicePermission.objects.create(
            code="validate-national-id"
        )
        self.url = reverse("validate_national_id")
        self.valid_key = APIKey.objects.create(
            service=service,
        )
        self.valid_key.permissions.add(national_id_permission)
        self.client.credentials(HTTP_API_KEY=self.valid_key.key)

    def test_free_api_key(self):
        """Test rate limiting."""
        for _ in range(5):  # Exceed rate limit (5/minute)
            self.client.post(
                self.url,
                {"national_id": "29001011234567"}, format="json"
            )
        response = self.client.post(
            self.url,
            {"national_id": "29001011234567"}, format="json"
        )
        self.assertEqual(response.status_code, 429)


class PremiumRateLimitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("validate_national_id")
        service = Service.objects.create(name="Service B")
        national_id_permission = ServicePermission.objects.create(
            code="validate-national-id"
        )
        self.url = reverse("validate_national_id")
        self.valid_key = APIKey.objects.create(
            service=service,
            tier="premium"
        )
        self.valid_key.permissions.add(national_id_permission)
        self.client.credentials(HTTP_API_KEY=self.valid_key.key)

    def test_premium_api_key(self):
        """Test rate limiting."""
        for _ in range(100):  # Exceed rate limit (100/minute)
            self.client.post(
                self.url,
                {"national_id": "29001011234567"}, format="json"
            )
        response = self.client.post(
            self.url,
            {"national_id": "29001011234567"}, format="json"
        )
        self.assertEqual(response.status_code, 429)
