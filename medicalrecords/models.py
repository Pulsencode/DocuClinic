from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.models import Patient
from inventory.models import Medicine


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.percentage}%"


class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )
    physician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prescriptions",
        limit_choices_to={"role": "physician"},
    )
    date_prescribed = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField()
    prescription_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.date_prescribed}"

    def clean(self):
        if self.physician.role != "physician":
            raise ValidationError({"physician": "Selected user is not a physician."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="medicines"
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dose = models.CharField(max_length=100)  # e.g., "500mg"
    frequency = models.CharField(max_length=100)  # e.g., "Twice a day"
    timing = models.CharField(max_length=255)  # e.g., "After meals"
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # Optional for liquid or powder form
    additional_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine.name} {self.dose}, {self.frequency}"
