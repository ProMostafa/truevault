
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from accounts.models import APIKey, Service, ServicePermission


class NationalIdApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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

    def test_valid_request(self):
        """Test valid API request."""
        response = self.client.post(
            "/api/validate-national-id/",
            {"national_id": "29001011234567"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_valid"])
        self.assertEqual(response.data["birth_year"], 1990)
        self.assertEqual(response.data["birth_date"], "1990-01-01")
        self.assertEqual(response.data["gender"], "Female")
        self.assertEqual(response.data["serial_number"], "12345")
        self.assertEqual(response.data["governorate"], "Dakahlia")

    def test_invalid_request(self):
        """Test invalid API request."""
        response = self.client.post(
            "/api/validate-national-id/",
            {"national_id": "290010112345"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("national_id", response.data)
        self.assertEqual(
            response.data["national_id"],
            ["Ensure this field has at least 14 characters."]
        )

    # def test_api_call_logging(self):
    #     """Test API call logging."""
    #     self.client.post(
    #         "/api/validate-national-id/",
    #         {"national_id": "29001011234567"}, format="json"
    #     )
    #     self.assertTrue(ApiCallLog.objects.exists())
    #     log = ApiCallLog.objects.first()
    #     self.assertEqual(log.endpoint, "/api/validate-national-id/")
    #     self.assertEqual(log.response_status, 200)
