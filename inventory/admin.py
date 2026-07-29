from django.contrib import admin
from unfold.admin import ModelAdmin

from inventory.models import Medicine, MedicineSupplier, RouteOfAdministration, Supplier


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    warn_unsaved_form = True
    pass


@admin.register(Medicine)
class MedicineAdmin(ModelAdmin):

    warn_unsaved_form = True
    search_fields = ("name",)


@admin.register(RouteOfAdministration)
class RouteOfAdministrationAdmin(ModelAdmin):
    warn_unsaved_form = True
    pass


@admin.register(MedicineSupplier)
class MedicineSupplierAdmin(ModelAdmin):
    warn_unsaved_form = True
    pass
