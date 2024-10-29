from django.contrib import admin
from .models import Supplier, Medicine, RouteOfAdministration, MedicineSupplier, Prescription, PrescriptionMedicine

admin.site.register(Supplier)
admin.site.register(Medicine)
admin.site.register(RouteOfAdministration)
admin.site.register(MedicineSupplier)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
