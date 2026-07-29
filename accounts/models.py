import random
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrator"),
        ("physician", "Physician"),
        ("nurse", "Nurse"),
        ("receptionist", "Receptionist"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="receptionist")
    registration_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "All Users"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            prefix = self.get_registration_prefix()
            self.registration_id = self.generate_registration_id(prefix)

        super().save(*args, **kwargs)

    def get_registration_prefix(self):
        prefixes = {
            "admin": "ADM",
            "physician": "PHY",
            "nurse": "NUR",
            "receptionist": "REC",
        }
        return prefixes.get(self.role, "USR")

    @staticmethod
    def generate_registration_id(prefix):
        year = datetime.now().year

        while True:
            random_number = random.randint(1000, 9999)
            registration_id = f"{prefix}{year}{random_number}"

            if not User.objects.filter(registration_id=registration_id).exists():
                return registration_id


class Patient(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )

    BLOOD_TYPE_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    )

    TEMPERATURE_METHOD_CHOICES = (
        ("O", "Oral"),
        ("A", "Axillary"),
        ("R", "Rectal"),
        ("E", "Ear"),
        ("F", "Forehead"),
    )

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    registration_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_vip = models.BooleanField(
        default=False,
        verbose_name="VIP Status",
        help_text="Enable for patients who require priority service.",
    )

    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )

    height_in_centimeter = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_in_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    temperature = models.FloatField(blank=True, null=True)
    temperature_method = models.CharField(
        max_length=1,
        choices=TEMPERATURE_METHOD_CHOICES,
        blank=True,
        null=True,
    )

    pulse = models.PositiveIntegerField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    bmi_status = models.CharField(max_length=20, blank=True, null=True)

    blood_type = models.CharField(
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    blood_pressure_systolic = models.PositiveIntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.PositiveIntegerField(blank=True, null=True)

    allergies = models.TextField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    class Meta:
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()

        return full_name or self.registration_id or f"Patient #{self.pk}"

    def get_blood_pressure(self):
        if (
            self.blood_pressure_systolic is not None
            and self.blood_pressure_diastolic is not None
        ):
            return (
                f"{self.blood_pressure_systolic}/"
                f"{self.blood_pressure_diastolic} mmHg"
            )

        return "-"

    def get_pulse_rate(self):
        if self.pulse is not None:
            return f"{self.pulse} bpm"

        return "-"

    def calculate_bmi(self):
        if (
            self.height_in_centimeter is not None
            and self.weight_in_kg is not None
            and self.height_in_centimeter > 0
        ):
            height_m = Decimal(self.height_in_centimeter) / Decimal("100")

            bmi = Decimal(self.weight_in_kg) / (height_m**2)

            self.bmi = round(float(bmi), 2)

            if self.bmi < 18.5:
                self.bmi_status = "Underweight"
            elif self.bmi < 25:
                self.bmi_status = "Normal"
            elif self.bmi < 30:
                self.bmi_status = "Overweight"
            else:
                self.bmi_status = "Obese"
        else:
            self.bmi = None
            self.bmi_status = None

    @property
    def age(self):
        if not self.date_of_birth:
            return None

        today = timezone.localdate()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day,
                )
            )
        )

    @staticmethod
    def generate_registration_id():
        year = timezone.localdate().year

        while True:
            random_number = random.randint(1000, 9999)
            registration_id = f"PAT{year}{random_number}"

            if not Patient.objects.filter(registration_id=registration_id).exists():
                return registration_id

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id()

        self.calculate_bmi()
        super().save(*args, **kwargs)
