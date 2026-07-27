from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from clinic.models import Clinic


@admin.register(Clinic)
class ClinicAdmin(ModelAdmin):
    warn_unsaved_form = True
    fieldsets = (
        (
            "Clinic Identity",
            {
                "fields": (("name", "logo"),),
            },
        ),
        (
            "Contact Details",
            {
                "fields": (
                    ("email", "contact_number"),
                    "address",
                ),
            },
        ),
        (
            "Registration & Legal",
            {
                "fields": (("gst_number", "license_number"),),
            },
        ),
        (
            "Scheduling",
            {
                "fields": ("consultation_duration",),
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        obj = Clinic.objects.first()
        if obj:
            return redirect(reverse("admin:clinic_clinic_change", args=[obj.pk]))
        # fallback: no clinic yet, let them add one
        return redirect(reverse("admin:clinic_clinic_add"))
