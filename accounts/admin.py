from django.contrib import admin

from .models import Accountant, Administrator, Nurse, Patient, Physician, Receptionist,PatientDetail

# admin.site.register(User) # Do not create users with this model
admin.site.register(Administrator)
admin.site.register(Physician)
admin.site.register(Accountant)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Receptionist)
admin.site.register(PatientDetail)
