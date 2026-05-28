from django.db import models

from accounts.models import User

# from accounts.models import Patient, Physician
from medicalrecords.models import Discount


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
        limit_choices_to={"role": "patient"},
    )
    physician = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="physician_appointments",
        limit_choices_to={"role": "physician"},
    )
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
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.patient.username} with {self.physician.username} on {self.date} {self.time}"


class Weekday(models.Model):
    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    name = models.CharField(max_length=9, choices=DAY_CHOICES, unique=True)

    class Meta:
        verbose_name = "Weekday"
        verbose_name_plural = "Weekdays"

    def __str__(self):
        return self.name


class PhysicianAvailability(models.Model):
    physician = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="physician_availability",
        limit_choices_to={"role": "physician"},
    )
    work_days = models.ManyToManyField(Weekday)
    work_time_start = models.TimeField(null=True)
    work_time_end = models.TimeField(null=True)
    lunch_start = models.TimeField(null=True, blank=True)
    lunch_end = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Physician Availability"
        verbose_name_plural = "Physician Availabilities"

    def __str__(self):
        days = ", ".join(day.get_name_display() for day in self.work_days.all())
        return f"{self.physician} available on {days}"
