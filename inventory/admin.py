from django.contrib import admin
from .models import Supplier, Medicine, RouteOfAdministration, MedicineSupplier

admin.site.register(Supplier)
admin.site.register(Medicine)
admin.site.register(RouteOfAdministration)
admin.site.register(MedicineSupplier)
