from datetime import datetime
import hashlib
from .constants import GOVERNORATES, Gender


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class IDValidator:
    """Base class for ID validation, extensible for multiple ID types."""

    @staticmethod
    def validate_egyptian_national_id(national_id):
        """
        Validate an Egyptian national ID and extract data.

        Args:
            national_id: 14-digit national ID string.

        Returns:
            Dict with validation result and extracted data or error message.
        """
        try:
            if not national_id.isdigit() or len(national_id) != 14:
                raise ValidationError("National ID must be 14 digits")

            # century_digit = national_id[0]
            # if century_digit not in ('2', '3'):
            #     raise ValidationError("Invalid century digit")

            # year = int(national_id[1:3])
            year = IDValidator.get_year(national_id)
            month = int(national_id[3:5])
            day = int(national_id[5:7])
            # year = year + 1900 if century_digit == '2' else year + 2000
            try:
                birth_date = datetime(year, month, day).strftime("%Y-%m-%d")
                      
            except ValueError:
                raise ValidationError("Invalid birth date")

            gender_digit = int(national_id[-2])
            gov_code = national_id[7:9]
            gender_code = (Gender.MALE if gender_digit % 2 == 1
                           else Gender.FEMALE)
            gender = Gender(gender_code).label
            governorate = GOVERNORATES.get(gov_code, "Unknown")
            return {
                "is_valid": True,
                "birth_year": year,
                "birth_date": birth_date,
                "governorate": governorate,
                "gender": gender,
                "serial_number": national_id[7:12],
            }

        except ValidationError as e:
            return {"is_valid": False, "error": str(e)}

    @staticmethod
    def hash_input(national_id: str) -> str:
        """Generate SHA-256 hash of input for logging."""
        return hashlib.sha256(national_id.encode()).hexdigest()

    def get_year(national_id):
        century_digit = int(national_id[0])
        yy = int(national_id[1:3])

        century_base_year = IDValidator.get_century_base_year(century_digit)
        year = century_base_year + yy
        if year > datetime.now().year:
            raise ValidationError("Birth year is in the future")

        return year

    def get_century_base_year(century_digit):
        """
        Given a century digit (e.g., 2, 3, 4),
        return the starting year of that century.
        """
        if century_digit < 1:
            raise ValidationError("Invalid century digit")

        return 1800 + (century_digit - 1) * 100
