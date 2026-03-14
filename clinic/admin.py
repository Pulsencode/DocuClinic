from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(ModelAdmin):
    pass
