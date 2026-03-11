import random
from datetime import date, time, timedelta

from django.utils import timezone
from faker import Faker
from faker_healthcare import HealthcareProvider

from accounting.models import (
    Account,
    AccountsPayable,
    AccountsReceivable,
    Asset,
    GeneralLedgerEntry,
    Invoice,
)
from accounts.models import (
    Accountant,
    Administrator,
    Nurse,
    Patient,
    PatientDetail,
    Physician,
    Receptionist,
)
from appointments.models import Appointment
from clinic.models import Clinic
from inventory.models import Medicine, MedicineSupplier, RouteOfAdministration, Supplier
from medicalrecords.models import Discount, Prescription, PrescriptionMedicine

fake = Faker("en_US")
fake.add_provider(HealthcareProvider)


def _random_phone_number() -> int:
    return int(fake.msisdn()[0:10])


def create_clinic() -> Clinic:
    clinic, _ = Clinic.objects.get_or_create(
        name="DocuClinic Demo Center",
        defaults={
            "address": fake.address(),
            "email": "info@docuclinic-demo.local",
            "contact_number": _random_phone_number(),
            "gst_number": "27ABCDE1234F1Z5",
            "license_number": "CLINIC-DEMO-001",
            "consultation_duration": 20,
        },
    )
    return clinic


def create_staff(
    num_physicians: int = 6,
    num_nurses: int = 6,
    num_receptionists: int = 3,
    num_accountants: int = 2,
):
    Administrator.objects.get_or_create(
        username="demo_admin",
        defaults={
            "first_name": "Demo",
            "last_name": "Admin",
            "email": "admin@docuclinic-demo.local",
            "phone_number": _random_phone_number(),
            "address": fake.address(),
            "is_staff": True,
            "is_superuser": True,
            "password": "Admin@123",
        },
    )

    physicians = []
    for i in range(num_physicians):
        first_name = fake.first_name()
        last_name = fake.last_name()
        physician, _ = Physician.objects.get_or_create(
            username=f"phy_{first_name.lower()}_{last_name.lower()}_{i}",
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "phone_number": _random_phone_number(),
                "address": fake.address(),
                "specialization": fake.job(),
                "license_number": f"PHY-LIC-{1000 + i}",
                "fee_per_consultation": random.choice([400, 500, 600, 800]),
                "password": "Password@123",
            },
        )
        physicians.append(physician)

    nurses = []
    for i in range(num_nurses):
        first_name = fake.first_name()
        last_name = fake.last_name()
        nurse, _ = Nurse.objects.get_or_create(
            username=f"nur_{first_name.lower()}_{last_name.lower()}_{i}",
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "phone_number": _random_phone_number(),
                "address": fake.address(),
                "password": "Password@123",
            },
        )
        nurses.append(nurse)

    receptionists = []
    for i in range(num_receptionists):
        first_name = fake.first_name()
        last_name = fake.last_name()
        receptionist, _ = Receptionist.objects.get_or_create(
            username=f"rec_{first_name.lower()}_{last_name.lower()}_{i}",
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "phone_number": _random_phone_number(),
                "address": fake.address(),
                "password": "Password@123",
            },
        )
        receptionists.append(receptionist)

    accountants = []
    for i in range(num_accountants):
        first_name = fake.first_name()
        last_name = fake.last_name()
        accountant, _ = Accountant.objects.get_or_create(
            username=f"acc_{first_name.lower()}_{last_name.lower()}_{i}",
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "phone_number": _random_phone_number(),
                "address": fake.address(),
                "password": "Password@123",
            },
        )
        accountants.append(accountant)

    return {
        "physicians": physicians,
        "nurses": nurses,
        "receptionists": receptionists,
        "accountants": accountants,
    }


def create_patients_with_details(num_patients: int = 50):
    patients = []
    for i in range(num_patients):
        first_name = fake.first_name()
        last_name = fake.last_name()
        patient, _ = Patient.objects.get_or_create(
            username=f"pat_{first_name.lower()}_{last_name.lower()}_{i}",
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "phone_number": _random_phone_number(),
                "address": fake.address(),
                "password": "Password@123",
            },
        )

        blood_type = fake.blood_type()
        age = random.randint(5, 90)
        height_cm = random.uniform(140, 190)
        weight_kg = random.uniform(45, 120)
        systolic = random.randint(100, 150)
        diastolic = random.randint(60, 95)
        pulse = random.randint(55, 110)

        details, _ = PatientDetail.objects.get_or_create(
            patient=patient,
            defaults={
                "is_vip": random.choice([True] + [False] * 4),
                "age": age,
                "gender": random.choice(["M", "F", "O"]),
                "height_in_centimeter": round(height_cm, 2),
                "weight_in_kg": round(weight_kg, 2),
                "temperature": round(random.uniform(97.0, 101.0), 1),
                "temperature_method": random.choice(
                    ["O", "T", "A"]
                ),  # Oral, Tympanic, Axillary
                "pulse": pulse,
                "bmi": round(weight_kg / ((height_cm / 100) ** 2), 2),
                "bmi_status": random.choice(
                    ["Underweight", "Normal", "Overweight", "Obese"]
                ),
                "blood_type": blood_type,
                "blood_pressure_systolic": systolic,
                "blood_pressure_diastolic": diastolic,
                "allergies": ", ".join({fake.allergy() for _ in range(2)}),
                "emergency_contact_name": fake.name(),
                "emergency_contact_number": str(_random_phone_number()),
            },
        )

        patients.append(patient)

    return patients


def create_inventory(num_medicines: int = 20):
    supplier, _ = Supplier.objects.get_or_create(
        name="Global Med Supplies",
        defaults={
            "contact_details": fake.phone_number(),
            "email": "orders@globalmedsupplies.local",
            "address": fake.address(),
        },
    )

    routes = []
    for name in ["Oral", "Injection", "Topical", "Inhalation"]:
        route, _ = RouteOfAdministration.objects.get_or_create(name=name)
        routes.append(route)

    medicines = []
    today = date.today()
    for i in range(num_medicines):
        generic_drug = fake.generic_drug()
        brand_drug = fake.brand_drug()
        route = random.choice(routes)

        medicine, _ = Medicine.objects.get_or_create(
            name=f"{generic_drug} {i}",
            defaults={
                "generic_name": generic_drug,
                "brand_name": brand_drug,
                "route_of_administration": route,
                "description": fake.text(max_nb_chars=120),
                "quantity": random.randint(50, 300),
                "expiration_date": today + timedelta(days=random.randint(60, 720)),
                "purchase_date": today - timedelta(days=random.randint(1, 365)),
                "minimum_stock_level": 20,
                "maximum_stock_level": 500,
                "storage_location": f"Shelf {random.randint(1, 5)} - Row {random.randint(1, 5)}",
            },
        )

        MedicineSupplier.objects.get_or_create(
            medicine=medicine,
            supplier=supplier,
            defaults={
                "price": random.randint(50, 2000),
                "supply_date": today - timedelta(days=random.randint(1, 60)),
            },
        )

        medicines.append(medicine)

    return medicines


def create_discounts():
    discounts = []
    for percentage in [0, 5, 10, 15, 20]:
        discount, _ = Discount.objects.get_or_create(percentage=percentage)
        discounts.append(discount)
    return discounts


def create_appointments(patients, physicians, discounts, num_appointments: int = 80):
    if not patients or not physicians:
        return []

    appointments = []
    today = timezone.localdate()
    for _ in range(num_appointments):
        patient = random.choice(patients)
        physician = random.choice(physicians)
        appointment_date = today + timedelta(days=random.randint(-10, 20))
        appointment_time = time(
            hour=random.randint(9, 18),
            minute=random.choice([0, 15, 30, 45]),
        )
        status = random.choice(["Scheduled", "Pending", "Completed", "Cancelled"])
        discount = random.choice(discounts) if random.random() < 0.3 else None
        fee = physician.fee_per_consultation or random.choice([400, 500, 600])

        appointment, _ = Appointment.objects.get_or_create(
            patient=patient,
            physician=physician,
            date=appointment_date,
            time=appointment_time,
            defaults={
                "status": status,
                "discount": discount,
                "consultation_fee": fee,
            },
        )
        appointments.append(appointment)

    return appointments


def create_prescriptions(patients, physicians, medicines, num_prescriptions: int = 60):
    if not patients or not physicians or not medicines:
        return []

    prescriptions = []
    for _ in range(num_prescriptions):
        patient = random.choice(patients)
        physician = random.choice(physicians)
        scenario = fake.patient_scenario()

        prescription = Prescription.objects.create(
            patient=patient,
            physician=physician,
            notes="Auto-generated demo prescription.",
            diagnosis=scenario["disease"],
            follow_up_date=timezone.localdate() + timedelta(days=random.randint(7, 60)),
        )

        for _ in range(random.randint(1, 3)):
            medicine = random.choice(medicines)
            PrescriptionMedicine.objects.create(
                prescription=prescription,
                medicine=medicine,
                dose=random.choice(["250mg", "500mg", "1 tablet"]),
                frequency=random.choice(["Once a day", "Twice a day", "Thrice a day"]),
                timing=random.choice(["Before meals", "After meals", "With water"]),
                amount=random.choice([None, 5, 10]),
                additional_instructions=random.choice(
                    [
                        "",
                        "Complete the full course even if you feel better.",
                        "Avoid driving after taking this medicine.",
                    ]
                ),
            )

        prescriptions.append(prescription)

    return prescriptions


def create_accounting_data():
    cash, _ = Account.objects.get_or_create(name="Cash", type="Asset")
    revenue, _ = Account.objects.get_or_create(
        name="Consultation Revenue", type="Revenue"
    )
    expense, _ = Account.objects.get_or_create(
        name="Medical Supplies Expense", type="Expense"
    )

    today = timezone.localdate()

    for i in range(10):
        amount = random.randint(500, 5000)
        GeneralLedgerEntry.objects.get_or_create(
            date=today - timedelta(days=random.randint(1, 30)),
            description=f"Consultation revenue entry {i+1}",
            debit_account=cash,
            credit_account=revenue,
            amount=amount,
        )

    for i in range(5):
        amount = random.randint(1000, 8000)
        GeneralLedgerEntry.objects.get_or_create(
            date=today - timedelta(days=random.randint(1, 30)),
            description=f"Medical supplies purchase {i+1}",
            debit_account=expense,
            credit_account=cash,
            amount=amount,
        )

    for i in range(8):
        AccountsReceivable.objects.get_or_create(
            name=f"AR #{i+1}",
            amount=random.randint(1000, 10000),
            due_date=today + timedelta(days=random.randint(7, 60)),
            description=f"Outstanding invoice {i+1}",
            status=random.choice(["PENDING", "PAID", "OVERDUE"]),
        )

    for i in range(8):
        AccountsPayable.objects.get_or_create(
            name=f"AP #{i+1}",
            amount=random.randint(1000, 10000),
            due_date=today + timedelta(days=random.randint(7, 60)),
            description=f"Supplier invoice {i+1}",
            status=random.choice(["PENDING", "PAID", "OVERDUE"]),
        )

    for i in range(5):
        Invoice.objects.get_or_create(
            invoice_number=f"INV-{1000 + i}",
            organization_name="DocuClinic Demo Center",
            date=today - timedelta(days=random.randint(1, 60)),
            total_amount=random.randint(2000, 20000),
        )

    for i in range(5):
        value = random.randint(5000, 50000)
        Asset.objects.get_or_create(
            name=f"Medical Equipment #{i+1}",
            purchase_date=today - timedelta(days=random.randint(100, 1000)),
            purchase_value=value,
            current_value=int(value * random.uniform(0.4, 0.9)),
            current_value_date=today,
            depreciation_rate=random.uniform(5, 20),
        )


def generate_demo_data():
    """
    High-level helper that generates a complete demo dataset.
    Safe to run multiple times thanks to get_or_create usage.
    """
    create_clinic()
    staff = create_staff()
    patients = create_patients_with_details()
    medicines = create_inventory()
    discounts = create_discounts()
    create_appointments(
        patients=patients,
        physicians=staff["physicians"],
        discounts=discounts,
    )
    create_prescriptions(
        patients=patients,
        physicians=staff["physicians"],
        medicines=medicines,
    )
    create_accounting_data()
