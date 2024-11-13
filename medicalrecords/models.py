from django.db import models

from accounts.models import Patient, Physician

from django.utils import timezone
from inventory.models import Medicine


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.percentage}%"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    consultation_fee = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.patient.username} with {self.physician.username} on {self.date} {self.time}"


class Prescription(models.Model):
    """Ividay adhyam prescription create akkumm anit prescription medicine model vech medicine add akkaam"""

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="prescriptions"
    )
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    date_prescribed = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField()
    prescription_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.patient.get_full_name()} by Dr. {self.physician.get_full_name} on {self.date_prescribed}"


class PrescriptionMedicine(models.Model):
    """Appaam avasnaam print edukaan ith use akkaam, ith vech multiple medicine add akkaam"""

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
        return f"{self.medicine.name} for {self.prescription.patient.get_full_name()} - {self.dose}, {self.frequency}"
