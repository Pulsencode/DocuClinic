from django.db import models
from django.utils import timezone


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
