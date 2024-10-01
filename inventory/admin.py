from django.contrib import admin
from .models import Supplier, Medicine, DosageForm, MedicineSupplier

admin.site.register(Supplier)
admin.site.register(Medicine)
admin.site.register(DosageForm)
admin.site.register(MedicineSupplier)
