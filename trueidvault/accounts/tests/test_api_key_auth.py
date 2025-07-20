from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from accounts.models import APIKey, Service, ServicePermission
from datetime import timedelta


class APIKeyAuthTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        service = Service.objects.create(name="Service B")
        national_id_permission = ServicePermission.objects.create(
            code="validate-national-id"
        )
        self.url = reverse("validate_national_id")
        self.payload = {"national_id": "29001011234567"}

        self.valid_key = APIKey.objects.create(
            service=service,
        )
        self.valid_key.permissions.add(national_id_permission)
        self.expired_key = APIKey.objects.create(
            service=service,
            expires_at=timezone.now() - timedelta(days=1),
        )
        self.expired_key.permissions.add(national_id_permission)
        self.inactive_key = APIKey.objects.create(
            service=service,
            is_active=False,
        )
        self.inactive_key.permissions.add(national_id_permission)
        self.key_without_permission = APIKey.objects.create(
            service=service,
        )

    def test_valid_key_with_permission(self):
        self.client.credentials(HTTP_API_KEY=self.valid_key.key)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)

    def test_key_without_permission_returns_403(self):
        self.client.credentials(HTTP_API_KEY=self.key_without_permission.key)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("permission", str(response.data).lower())

    def test_expired_key(self):
        self.client.credentials(HTTP_API_KEY=self.expired_key.key)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("expired", str(response.data).lower())

    def test_inactive_key(self):
        self.client.credentials(HTTP_API_KEY=self.inactive_key.key)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("inactive", str(response.data).lower())

    def test_missing_api_key(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data.get("detail")).lower(),
                         "api key required")
