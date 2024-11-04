from django.contrib import admin
from .models import Administrator, Physician, Accountant, Patient, User

admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Physician)
admin.site.register(Accountant)
admin.site.register(Patient)
