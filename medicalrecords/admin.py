from django.contrib import admin
from .models import Appointment, Prescription, PrescriptionMedicine, Discount


admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
admin.site.register(Discount)
