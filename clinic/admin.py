from django.contrib import admin
from unfold.admin import ModelAdmin

from clinic.models import Clinic


@admin.register(Clinic)
class ClinicAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return not Clinic.objects.exists()
