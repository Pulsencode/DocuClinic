"""Read-only appointment calendar data, respecting related-record permissions."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from accounts.models import Patient
from clinic.models import Clinic

from .models import Appointment


def can_read(user, model):
    label = model._meta.app_label
    name = model._meta.model_name
    return user.has_perm(f"{label}.view_{name}") or user.has_perm(
        f"{label}.change_{name}"
    )


def calendar_context(model_admin, request):
    today = timezone.localdate()
    try:
        selected = date.fromisoformat(request.GET.get("date", today.isoformat()))
        if not 1900 <= selected.year <= 9998:
            raise ValueError
    except ValueError:
        selected = today
    view = request.GET.get("view", "week")
    if view not in {"week", "month", "day"}:
        view = "week"
    namespace = model_admin.admin_site.name
    staff_access = can_read(request.user, get_user_model())
    return {
        "calendar_config": {
            "today": today.isoformat(),
            "date": selected.isoformat(),
            "view": view,
            "timezone": timezone.get_current_timezone_name(),
            "eventsUrl": reverse(f"{namespace}:appointments_appointment_events"),
        },
        "calendar_add_url": (
            reverse(f"{namespace}:appointments_appointment_add")
            if model_admin.has_add_permission(request)
            else None
        ),
        "calendar_table_url": reverse(f"{namespace}:appointments_appointment_table"),
        "calendar_doctors": (
            get_user_model()
            .objects.filter(role="physician")
            .only("pk", "first_name", "last_name", "username")
            .order_by("first_name", "last_name", "username")
            if staff_access
            else []
        ),
        "calendar_statuses": Appointment.STATUS_CHOICES,
        "calendar_can_search": can_read(request.user, Patient),
    }


def calendar_events(model_admin, request):
    start = date.fromisoformat(request.GET.get("start", ""))
    end = date.fromisoformat(request.GET.get("end", ""))
    if not 0 < (end - start).days <= 42 or not (1900 <= start.year <= end.year <= 9998):
        raise ValueError
    queryset = model_admin.get_queryset(request)
    patient_access = can_read(request.user, Patient)
    staff_access = can_read(request.user, get_user_model())
    status = request.GET.get("status", "")
    physician = request.GET.get("physician", "")
    search = request.GET.get("q", "").strip()[:100]
    if status:
        if status not in dict(Appointment.STATUS_CHOICES):
            raise ValueError
        queryset = queryset.filter(status=status)
    if physician:
        if not staff_access:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        queryset = queryset.filter(physician_id=int(physician))
    if search:
        if not patient_access:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        queryset = queryset.filter(
            Q(patient__first_name__icontains=search)
            | Q(patient__last_name__icontains=search)
            | Q(patient__registration_id__icontains=search)
        )
    unscheduled = queryset.filter(Q(date__isnull=True) | Q(time__isnull=True)).count()
    # Include the preceding day's appointments so a legacy event spanning midnight
    # remains visible at the start of this range. Never join denied related tables.
    queryset = queryset.filter(
        date__gte=start - timedelta(days=1), date__lt=end, time__isnull=False
    )
    fields = ["pk", "date", "time", "status", "duration_minutes"]
    if patient_access:
        fields += [
            "patient__first_name",
            "patient__last_name",
            "patient__registration_id",
        ]
    if staff_access:
        fields += [
            "physician__first_name",
            "physician__last_name",
            "physician__username",
        ]
    duration = Clinic.objects.values_list("consultation_duration", flat=True).first()
    duration = duration if duration and 1 <= duration <= 1440 else 30
    events = []
    for row in queryset.order_by("date", "time", "pk").values(*fields):
        patient = "Patient details restricted"
        doctor = "Physician details restricted"
        if patient_access:
            patient = (
                " ".join(
                    filter(
                        None, [row["patient__first_name"], row["patient__last_name"]]
                    )
                )
                or row["patient__registration_id"]
            )
        if staff_access:
            doctor = (
                " ".join(
                    filter(
                        None,
                        [row["physician__first_name"], row["physician__last_name"]],
                    )
                )
                or row["physician__username"]
            )
        events.append(
            {
                "id": row["pk"],
                "patient": patient,
                "physician": doctor,
                "date": row["date"].isoformat(),
                "time": row["time"].isoformat(),
                "duration": row["duration_minutes"] or duration,
                "estimatedDuration": row["duration_minutes"] is None,
                "status": row["status"],
                "reason": "Not recorded",
                "url": reverse(
                    f"{model_admin.admin_site.name}:appointments_appointment_change",
                    args=[row["pk"]],
                ),
            }
        )
    return {"events": events, "unscheduled": unscheduled}
