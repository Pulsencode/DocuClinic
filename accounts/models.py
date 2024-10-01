from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number_country_code = models.CharField(max_length=3, null=True)
    phone_number = models.PositiveIntegerField(null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Doctor(User):
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class Operator(User):
    department = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"


# TODO need to add some fields here and need to remove the admin_level
class Admin(User):
    admin_level = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
