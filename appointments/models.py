from django.db import models

from accounts.models import Patient, Physician
from medicalrecords.models import Discount


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
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL
    )
    consultation_fee = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.patient.username} with {self.physician.username} on {self.date} {self.time}"
