import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import Patient

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo staff users and separate patient records."

    DEFAULT_PASSWORD = "Demo@123"

    FIRST_NAMES = (
        "Aarav",
        "Aditya",
        "Akash",
        "Ananya",
        "Arjun",
        "Arya",
        "Deepak",
        "Devika",
        "Diya",
        "Farhan",
        "Gouri",
        "Hari",
        "Ishaan",
        "Keerthana",
        "Meera",
        "Nikhil",
        "Rahul",
        "Riya",
        "Sanjay",
        "Sneha",
        "Vishnu",
        "Zoya",
    )

    LAST_NAMES = (
        "Ahmed",
        "Babu",
        "Das",
        "George",
        "Joseph",
        "Khan",
        "Kumar",
        "Menon",
        "Nair",
        "Pillai",
        "Raj",
        "Rajan",
        "Reddy",
        "Shah",
        "Thomas",
        "Varghese",
    )

    ADDRESSES = (
        "Dubai, United Arab Emirates",
        "Abu Dhabi, United Arab Emirates",
        "Sharjah, United Arab Emirates",
        "Ajman, United Arab Emirates",
        "Kochi, Kerala, India",
        "Thrissur, Kerala, India",
        "Kozhikode, Kerala, India",
        "Thiruvananthapuram, Kerala, India",
    )

    BLOOD_TYPES = (
        "A+",
        "A-",
        "B+",
        "B-",
        "O+",
        "O-",
        "AB+",
        "AB-",
    )

    GENDERS = (
        "M",
        "F",
        "O",
    )

    TEMPERATURE_METHODS = (
        "O",
        "A",
        "R",
        "E",
        "F",
    )

    ALLERGIES = (
        None,
        None,
        None,
        "No known allergies",
        "Penicillin",
        "Peanuts",
        "Dust",
        "Pollen",
        "Shellfish",
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=25,
            help="Number of demo patients to create.",
        )

        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo users and demo patients before creating.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        patient_count = max(options["patients"], 0)
        reset = options["reset"]

        self.stdout.write(self.style.WARNING("Creating accounts demo data..."))

        if reset:
            self.delete_existing_demo_data()

        users_created, users_updated = self.create_staff_users()
        patients_created = self.create_patients(patient_count)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Accounts demo data completed successfully.")
        )

        self.stdout.write(f"Staff users created: {users_created}")
        self.stdout.write(f"Staff users updated: {users_updated}")
        self.stdout.write(f"Patients created: {patients_created}")

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(f"Demo staff password: {self.DEFAULT_PASSWORD}")
        )

    def delete_existing_demo_data(self):
        demo_usernames = [
            user_data["username"] for user_data in self.get_staff_user_data()
        ]

        deleted_users, _ = User.objects.filter(username__in=demo_usernames).delete()

        deleted_patients, _ = Patient.objects.filter(
            email__startswith="demo.patient"
        ).delete()

        self.stdout.write(
            self.style.WARNING(f"Deleted demo user records: {deleted_users}")
        )
        self.stdout.write(
            self.style.WARNING(f"Deleted demo patient records: {deleted_patients}")
        )

    def get_staff_user_data(self):
        return [
            {
                "username": "admin_demo",
                "first_name": "System",
                "last_name": "Administrator",
                "email": "admin.demo@example.com",
                "role": "admin",
                "phone_number": "+971500000001",
                "address": "Dubai, United Arab Emirates",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
            {
                "username": "physician_demo",
                "first_name": "Arjun",
                "last_name": "Nair",
                "email": "physician.demo@example.com",
                "role": "physician",
                "phone_number": "+971500000002",
                "address": "Dubai, United Arab Emirates",
                "is_staff": True,
                "is_superuser": False,
                "is_active": True,
            },
            {
                "username": "physician_demo_2",
                "first_name": "Meera",
                "last_name": "Thomas",
                "email": "physician2.demo@example.com",
                "role": "physician",
                "phone_number": "+971500000003",
                "address": "Sharjah, United Arab Emirates",
                "is_staff": True,
                "is_superuser": False,
                "is_active": True,
            },
            {
                "username": "nurse_demo",
                "first_name": "Sneha",
                "last_name": "Joseph",
                "email": "nurse.demo@example.com",
                "role": "nurse",
                "phone_number": "+971500000004",
                "address": "Ajman, United Arab Emirates",
                "is_staff": True,
                "is_superuser": False,
                "is_active": True,
            },
            {
                "username": "nurse_demo_2",
                "first_name": "Devika",
                "last_name": "Menon",
                "email": "nurse2.demo@example.com",
                "role": "nurse",
                "phone_number": "+971500000005",
                "address": "Dubai, United Arab Emirates",
                "is_staff": True,
                "is_superuser": False,
                "is_active": True,
            },
            {
                "username": "receptionist_demo",
                "first_name": "Diya",
                "last_name": "Raj",
                "email": "receptionist.demo@example.com",
                "role": "receptionist",
                "phone_number": "+971500000006",
                "address": "Dubai, United Arab Emirates",
                "is_staff": True,
                "is_superuser": False,
                "is_active": True,
            },
        ]

    def create_staff_users(self):
        created_count = 0
        updated_count = 0

        for user_data in self.get_staff_user_data():
            username = user_data["username"]

            defaults = {
                key: value for key, value in user_data.items() if key != "username"
            }

            user, created = User.objects.update_or_create(
                username=username,
                defaults=defaults,
            )

            user.set_password(self.DEFAULT_PASSWORD)
            user.save()

            if created:
                created_count += 1
                message = (
                    f"Created staff user: {username} " f"({user.get_role_display()})"
                )
                self.stdout.write(self.style.SUCCESS(message))
            else:
                updated_count += 1
                message = (
                    f"Updated staff user: {username} " f"({user.get_role_display()})"
                )
                self.stdout.write(message)

        return created_count, updated_count

    def create_patients(self, count):
        created_count = 0

        for index in range(1, count + 1):
            email = f"demo.patient{index:03d}@example.com"

            if Patient.objects.filter(email=email).exists():
                self.stdout.write(f"Patient already exists: {email}")
                continue

            first_name = random.choice(self.FIRST_NAMES)
            last_name = random.choice(self.LAST_NAMES)

            height = Decimal(str(random.randint(145, 195))).quantize(Decimal("0.00"))

            weight = Decimal(str(random.randint(42, 120))).quantize(Decimal("0.00"))

            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=self.generate_phone_number(),
                address=random.choice(self.ADDRESSES),
                is_vip=random.random() < 0.15,
                date_of_birth=self.generate_date_of_birth(
                    minimum_age=5,
                    maximum_age=90,
                ),
                gender=random.choice(self.GENDERS),
                height_in_centimeter=height,
                weight_in_kg=weight,
                temperature=round(
                    random.uniform(36.0, 38.5),
                    1,
                ),
                temperature_method=random.choice(self.TEMPERATURE_METHODS),
                pulse=random.randint(55, 115),
                blood_type=random.choice(self.BLOOD_TYPES),
                blood_pressure_systolic=random.randint(
                    90,
                    165,
                ),
                blood_pressure_diastolic=random.randint(
                    55,
                    105,
                ),
                allergies=random.choice(self.ALLERGIES),
                emergency_contact_name=(
                    f"{random.choice(self.FIRST_NAMES)} " f"{last_name}"
                ),
                emergency_contact_number=(self.generate_phone_number()),
                is_active=True,
            )

            created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created patient: {patient} " f"({patient.registration_id})"
                )
            )

        return created_count

    @staticmethod
    def generate_phone_number():
        return f"+9715{random.randint(0, 9)}{random.randint(1000000, 9999999)}"

    @staticmethod
    def generate_date_of_birth(
        minimum_age=1,
        maximum_age=90,
    ):
        today = timezone.localdate()

        latest_date = today - timedelta(days=minimum_age * 365)

        earliest_date = today - timedelta(days=maximum_age * 365)

        date_range = (latest_date - earliest_date).days

        return earliest_date + timedelta(days=random.randint(0, date_range))
