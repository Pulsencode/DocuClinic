from datetime import date

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import OperationalError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils import timezone
from unfold.admin import ModelAdmin

from appointments.models import Appointment, PhysicianAvailability, Weekday
from appointments.scheduling import available_slots, consultation_duration


def can_read(user, model):
    return user.has_perm(
        f"{model._meta.app_label}.view_{model._meta.model_name}"
    ) or user.has_perm(f"{model._meta.app_label}.change_{model._meta.model_name}")


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    change_form_template = "admin/appointments/appointment/change_form.html"
    list_select_related = ("patient", "physician", "discount")
    warn_unsaved_form = True
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
            "1. Choose a doctor",
            {"fields": ("physician",)},
        ),
        (
            "2. Choose a date and time",
            {"fields": ("date", "time")},
        ),
        (
            "3. Patient and appointment details",
            {
                "fields": (
                    "patient",
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

    class Media:
        css = {"all": ("appointments/booking.css",)}
        js = ("appointments/booking.js",)

    def has_add_permission(self, request):
        from accounts.models import Patient, User

        return super().has_add_permission(request) and all(
            can_read(request.user, model)
            for model in (Patient, User, PhysicianAvailability)
        )

    def get_urls(self):
        return [
            path(
                "calendar/",
                self.admin_site.admin_view(self.calendar),
                name="appointments_appointment_calendar",
            )
        ] + super().get_urls()

    def calendar(self, request):
        from accounts.models import User

        if not (
            can_read(request.user, User)
            and can_read(request.user, PhysicianAvailability)
        ):
            raise PermissionDenied
        obj = None
        if request.GET.get("appointment"):
            obj = self.get_object(request, request.GET["appointment"])
            if obj is None or not self.has_change_permission(request, obj):
                raise PermissionDenied
        elif not self.has_add_permission(request):
            raise PermissionDenied
        try:
            physician_id = int(request.GET.get("physician", ""))
            start = date.fromisoformat(request.GET.get("start", ""))
            # Keep the endpoint bounded, even for manually constructed requests.
            if not 1 <= start.year <= 9998:
                raise ValueError
            duration = (
                obj.duration_minutes if obj else None
            ) or consultation_duration()
            days = available_slots(
                physician_id, start, exclude=obj.pk if obj else None, duration=duration
            )
        except (ValueError, ValidationError) as error:
            message = (
                " ".join(error.messages)
                if isinstance(error, ValidationError)
                else "Choose a doctor and a valid week."
            )
            return JsonResponse({"error": message}, status=400)
        return JsonResponse(
            {
                "days": days,
                "duration": duration,
                "timezone": timezone.get_current_timezone_name(),
            }
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in {"patient", "physician", "discount"}:
            model = db_field.remote_field.model
            if not can_read(request.user, model):
                kwargs["queryset"] = model.objects.none()
            elif db_field.name in {
                "patient",
                "physician",
            } and request.resolver_match.url_name.endswith("_add"):
                kwargs["queryset"] = model.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        context = {
            **(extra_context or {}),
            "calendar_today": timezone.localdate().isoformat(),
        }
        try:
            return super().changeform_view(request, object_id, form_url, context)
        except (ValidationError, OperationalError) as error:
            if request.method != "POST":
                raise
            if (
                isinstance(error, OperationalError)
                and "locked" not in str(error).lower()
            ):
                raise
            # A competing booking can win after form validation. The admin's
            # transaction has rolled back; return a working retry screen.
            self.message_user(
                request,
                "The booking could not be saved because availability changed or is busy. Please select a slot and try again.",
                messages.ERROR,
            )
            return redirect(
                reverse(
                    f"{self.admin_site.name}:appointments_appointment_change",
                    args=[object_id],
                )
                if object_id
                else reverse(f"{self.admin_site.name}:appointments_appointment_add")
            )


@admin.register(Weekday)
class WeekdayAdmin(ModelAdmin):
    warn_unsaved_form = True
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PhysicianAvailability)
class PhysicianAvailabilityAdmin(ModelAdmin):
    warn_unsaved_form = True
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
