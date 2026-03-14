from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Medicine, MedicineSupplier, RouteOfAdministration, Supplier


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    pass


@admin.register(Medicine)
class MedicineAdmin(ModelAdmin):
    pass


@admin.register(RouteOfAdministration)
class RouteOfAdministrationAdmin(ModelAdmin):
    pass


@admin.register(MedicineSupplier)
class MedicineSupplierAdmin(ModelAdmin):
    pass
