from django.contrib import admin
from unfold.admin import ModelAdmin

from medicalrecords.models import Discount, Prescription, PrescriptionMedicine


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    warn_unsaved_form = True
    pass


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(ModelAdmin):
    warn_unsaved_form = True
    pass


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    warn_unsaved_form = True
    list_display = ("percentage",)
    search_fields = ("percentage",)
