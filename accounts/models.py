import random
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    registration_id = models.CharField(max_length=10, unique=True, editable=False)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "All users"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def generate_registration_id(self, prefix):
        """
        Generates a registration ID with a prefix, year, and a unique random number.
        """
        year = datetime.now().year
        while True:
            random_number = random.randint(1000, 9999)
            registration_id = f"{prefix}{year}{random_number}"
            if not User.objects.filter(registration_id=registration_id).exists():
                return registration_id


class Administrator(User):
    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="ADM")
        super().save(*args, **kwargs)


class Physician(User):
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Physician"
        verbose_name_plural = "Physicians"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="PHY")
        super().save(*args, **kwargs)


class Nurse(User):
    class Meta:
        verbose_name = "Nurse"
        verbose_name_plural = "Nurses"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="NUR")
        super().save(*args, **kwargs)


class Accountant(User):
    class Meta:
        verbose_name = "Accountant"
        verbose_name_plural = "Accountants"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="ACC")
        super().save(*args, **kwargs)


class Receptionist(User):
    class Meta:
        verbose_name = "Receptionist"
        verbose_name_plural = "Receptionists"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="RES")
        super().save(*args, **kwargs)


class Patient(User):
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = self.generate_registration_id(prefix="PAT")
        super().save(*args, **kwargs)


class PatientDetail(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    BLOOD_TYPE_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    ]
    patient = models.OneToOneField(
        "accounts.Patient",
        related_name="patient_details",
        null=True,
        on_delete=models.CASCADE,
    )
    # condition = models.TextField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    height_in_centimeter = models.DecimalField(
        max_digits=5, decimal_places=2, null=True
    )
    weight_in_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    temperature = models.FloatField(blank=True, null=True)
    temperature_method = models.CharField(max_length=1, blank=True, null=True)
    pulse = models.PositiveIntegerField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    bmi_status = models.CharField(max_length=10, blank=True, null=True)

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, null=True)
    blood_pressure_systolic = models.IntegerField(null=True)
    blood_pressure_diastolic = models.IntegerField(null=True)

    allergies = models.TextField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=15, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def get_blood_pressure(self):
        return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic} mmHg"

    def get_pulse_rate(self):
        return f"{self.pulse} bpm"

    def calculate_bmi(self):
        if self.height_in_centimeter and self.weight:
            height_in_meters = self.height_in_centimeter / 100
            bmi = self.weight_in_kg / (height_in_meters**2)
            self.bmi = round(bmi, 2)
            self.save()

    def determine_bmi_status(self):
        if self.bmi:
            if self.bmi < 18.5:
                self.bmi_status = "Underweight"
            elif 18.5 <= self.bmi < 25:
                self.bmi_status = "Normal"
            elif 25 <= self.bmi < 30:
                self.bmi_status = "Overweight"
            else:
                self.bmi_status = "Obese"
            self.save()
