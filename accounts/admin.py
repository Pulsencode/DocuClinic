from django.contrib import admin
from .models import Doctor, Operator, Admin, Patient, Appointment

# admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Operator)
admin.site.register(Admin)
admin.site.register(Patient)
admin.site.register(Appointment)
