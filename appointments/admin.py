from django.contrib import admin

from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]
    search_fields = ["id"]
    list_filter = ["created_at"]
