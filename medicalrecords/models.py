from django.db import models

from accounts.models import Patient, Doctor

from django.utils import timezone
from inventory.models import Medicine


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_datetime"]

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.username} on {self.appointment_datetime}"


class Prescription(models.Model):
    """Ividay adhyam prescription create akkumm anit prescription medicine model vech medicine add akkaam"""

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="prescriptions"
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_prescribed = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField()
    prescription_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.patient.get_full_name()} by Dr. {self.doctor_name} on {self.date_prescribed}"


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
