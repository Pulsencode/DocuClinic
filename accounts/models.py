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
        verbose_name = "Super Admin"
        verbose_name_plural = "Super Admins"

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


class Doctor(User):
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        self.registration_id = self.generate_registration_id(prefix="DOC")
        super().save(*args, **kwargs)


class Operator(User):
    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        self.registration_id = self.generate_registration_id(prefix="OPE")
        super().save(*args, **kwargs)


class Admin(User):
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"

    def save(self, *args, **kwargs):
        self.registration_id = self.generate_registration_id(prefix="ADM")
        super().save(*args, **kwargs)


class Patient(User):
    def save(self, *args, **kwargs):
        self.registration_id = self.generate_registration_id(prefix="PAT")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.username} - {self.registration_id}"
