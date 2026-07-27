from django.core.exceptions import ValidationError
from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(blank=True)
    contact_number = models.PositiveBigIntegerField(null=True, blank=True)
    gst_number = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(
        upload_to="clinic_logo", default="media/default_clinic_logo.webp"
    )
    consultation_duration = models.PositiveIntegerField(
        null=True, help_text="Duration in minutes"
    )

    def clean(self):
        if not self.pk and Clinic.objects.exists():
            raise ValidationError("Only one Clinic instance is allowed.")

    def __str__(self):
        return self.name
