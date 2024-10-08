from django.db import models


# Create your models here.
class PatientDetails(User):
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
    condition = models.TextField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, null=True)
    allergies = models.TextField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=15, null=True)