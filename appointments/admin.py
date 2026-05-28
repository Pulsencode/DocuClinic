from django.contrib import admin
from unfold.admin import ModelAdmin

from appointments.models import Appointment, PhysicianAvailability, Weekday


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = (
        "patient",
        "physician",
        "date",
        "time",
        "status",
        "consultation_fee",
        "discount",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "physician",
        "discount",
    )

    search_fields = (
        "patient__username",
        "patient__first_name",
        "patient__last_name",
        "patient__registration_id",
        "physician__username",
        "physician__first_name",
        "physician__last_name",
        "physician__registration_id",
    )

    autocomplete_fields = (
        "patient",
        "physician",
        "discount",
    )

    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Appointment Details",
            {
                "fields": (
                    "patient",
                    "physician",
                    "date",
                    "time",
                    "status",
                )
            },
        ),
        (
            "Billing",
            {
                "fields": (
                    "consultation_fee",
                    "discount",
                )
            },
        ),
        (
            "System Info",
            {"fields": ("created_at",)},
        ),
    )


@admin.register(Weekday)
class WeekdayAdmin(ModelAdmin):
    list_display = ("name",)

    search_fields = ("name",)


@admin.register(PhysicianAvailability)
class PhysicianAvailabilityAdmin(ModelAdmin):
    list_display = (
        "physician",
        "work_time_start",
        "work_time_end",
        "lunch_start",
        "lunch_end",
    )

    list_filter = (
        "work_days",
        "physician",
    )

    search_fields = (
        "physician__username",
        "physician__first_name",
        "physician__last_name",
        "physician__registration_id",
    )

    autocomplete_fields = ("physician",)

    filter_horizontal = ("work_days",)

    fieldsets = (
        (
            "Physician",
            {
                "fields": (
                    "physician",
                    "work_days",
                )
            },
        ),
        (
            "Working Time",
            {
                "fields": (
                    "work_time_start",
                    "work_time_end",
                )
            },
        ),
        (
            "Lunch Break",
            {
                "fields": (
                    "lunch_start",
                    "lunch_end",
                )
            },
        ),
    )
