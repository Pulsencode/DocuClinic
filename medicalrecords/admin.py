from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Discount, Prescription, PrescriptionMedicine


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    pass


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    pass
