from django.urls import path
from .views import ValidateNationalIdView

urlpatterns = [
    path("validate-national-id/",
         ValidateNationalIdView.as_view(), name="validate_national_id"),
]