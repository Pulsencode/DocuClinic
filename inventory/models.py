from django.db import models
from django.utils import timezone
from accounts.models import Patient, Doctor


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


class RouteOfAdministration(models.Model):
    """This model determines the way the medicine is taken. example oral, injection etc.."""

    name = models.CharField(max_length=255)
    route_of_administration = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.route_of_administration}"


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    route_of_administration = models.ForeignKey(
        RouteOfAdministration,
        on_delete=models.SET_NULL,
        null=True,
    )
    # dosage_strength = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    purchase_date = models.DateField()
    minimum_stock_level = models.SmallIntegerField()
    maximum_stock_level = models.SmallIntegerField()
    storage_location = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.quantity} units"

    def is_expired(self):
        return self.expiration_date < timezone.now().date()


class MedicineSupplier(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    supply_date = models.DateField()

    def __str__(self):
        return f"{self.supplier.name} - {self.medicine.name} at {self.price}"


class Prescription(models.Model):
    """Ividay adhyam prescription create akkumm anit prescription medicine model vech medicine add akkaam"""
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="prescriptions"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE
    )
    date_prescribed = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

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
