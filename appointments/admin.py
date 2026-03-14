from django.contrib import admin
from unfold.admin import ModelAdmin

from appointments.models import Appointment, PhysicianAvailability, Weekday


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ["date", "__str__", "created_at", "status"]
    search_fields = ["id"]
    list_filter = ["created_at"]


@admin.register(Weekday)
class WeekdayAdmin(ModelAdmin):
    pass


@admin.register(PhysicianAvailability)
class PhysicianAvailabilityAdmin(ModelAdmin):
    list_display = (
        "physician",
        "display_work_days",
        "work_time_start",
        "work_time_end",
        "lunch_start",
        "lunch_end",
    )

    def display_work_days(self, obj):
        return ", ".join([day.name for day in obj.work_days.all()])

    display_work_days.short_description = "Work Days"
