from django.contrib import admin
from .models import Appointment, Prescription, PrescriptionMedicine


admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
