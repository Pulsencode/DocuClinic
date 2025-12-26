from django.contrib import admin

from .models import Discount, Prescription, PrescriptionMedicine

admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
admin.site.register(Discount)
