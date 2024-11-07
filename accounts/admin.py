from django.contrib import admin

from .models import Accountant, Administrator, Patient, Physician

# from .models import User

# admin.site.register(User) # Do not create users with this model
admin.site.register(Administrator)
admin.site.register(Physician)
admin.site.register(Accountant)
admin.site.register(Patient)
