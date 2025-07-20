from django.test import TestCase
from ekyc.validators import IDValidator, ValidationError
from ekyc.constants import Gender


class NationalIdValidatorTests(TestCase):

    def test_get_century_base_year(self):
        self.assertEqual(IDValidator.get_century_base_year(2), 1900)
        self.assertEqual(IDValidator.get_century_base_year(3), 2000)
        self.assertEqual(IDValidator.get_century_base_year(4), 2100)
        self.assertEqual(IDValidator.get_century_base_year(5), 2200)
        self.assertEqual(IDValidator.get_century_base_year(9), 2600)
        with self.assertRaises(ValidationError) as context:
            IDValidator.get_century_base_year(0)
        self.assertIn("Invalid century digit", str(context.exception))
        with self.assertRaises(ValidationError) as context:
            IDValidator.get_century_base_year(-1)
        self.assertIn("Invalid century digit", str(context.exception))

    # def test_unsupported_century_digit_too_low(self):
    #     with self.assertRaises(ValidationError) as context:
    #         IDValidator.get_year("19001011234567")
    #     self.assertIn("Birth year is in the future", str(context.exception))

    # def test_unsupported_century_digit_too_high(self):
    #     with self.assertRaises(ValidationError) as context:
    #         IDValidator.get_year("49001011234567")
    #     self.assertIn("Unsupported century digit", str(context.exception))

    def test_birth_year_in_future(self):
        # Suppose today is 2025, so year 2090 is invalid
        with self.assertRaises(ValidationError) as context:
            IDValidator.get_year("39090011234567")  # 2090
        self.assertIn("Birth year is in the future", str(context.exception))

    def test_valid_national_id(self):
        """Test valid Egyptian national ID."""
        result = IDValidator.validate_egyptian_national_id("29001011234567")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["birth_year"], 1990)
        self.assertEqual(result["birth_date"], "1990-01-01")
        self.assertEqual(result["gender"], Gender.FEMALE.label)
        self.assertEqual(result["serial_number"], "12345")

    def test_invalid_length(self):
        """Test ID with incorrect length."""
        result = IDValidator.validate_egyptian_national_id("290010112345")
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error"], "National ID must be 14 digits")

    def test_invalid_century_digit(self):
        """Test ID Invalid century digit"""
        result = IDValidator.validate_egyptian_national_id("09001011234567")
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error"], "Invalid century digit")

    def test_invalid_date(self):
        """Test ID with invalid birth date."""
        result = IDValidator.validate_egyptian_national_id("29013311234567")
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error"], "Invalid birth date")
