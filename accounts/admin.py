from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from accounts.models import (
    Accountant,
    Administrator,
    Nurse,
    Patient,
    PatientDetail,
    Physician,
    Receptionist,
)

admin.site.unregister(Group)


@admin.register(Administrator)
class AdministratorAdmin(ModelAdmin):
    pass


@admin.register(Physician)
class PhysicianAdmin(ModelAdmin):
    pass


@admin.register(Accountant)
class AccountantAdmin(ModelAdmin):
    pass


@admin.register(Patient)
class PatientAdmin(ModelAdmin):
    pass


@admin.register(Nurse)
class NurseAdmin(ModelAdmin):
    pass


@admin.register(Receptionist)
class ReceptionistAdmin(ModelAdmin):
    pass


@admin.register(PatientDetail)
class PatientDetailAdmin(ModelAdmin):
    pass
