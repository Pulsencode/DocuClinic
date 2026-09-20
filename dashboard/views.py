from datetime import date, timedelta

from django.db.models import Count, F, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from accounts.models import Patient, User
from appointments.models import Appointment
from core.settings.unfold import can_view_model
from inventory.models import Medicine
from medicalrecords.models import Prescription


def _last_n_months(today, n=5):
    year, month = today.year, today.month
    months = []
    for _ in range(n):
        months.append(date(year, month, 1))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return list(reversed(months))


def dashboard_callback(request, context):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    expiring_soon_cutoff = today + timedelta(days=30)
    can_use_admin = request.user.is_active and request.user.is_staff
    permissions = {
        "can_view_appointments": can_view_model("appointments", "appointment")(request),
        "can_view_patients": can_view_model("accounts", "patient")(request),
        "can_view_users": can_view_model("accounts", "user")(request),
        "can_view_medicines": can_view_model("inventory", "medicine")(request),
        "can_view_prescriptions": can_view_model("medicalrecords", "prescription")(
            request
        ),
    }
    context.update(permissions)
    context.update(
        today=today,
        has_dashboard_data=any(permissions.values()),
        can_add_appointment=can_use_admin
        and request.user.has_perm("appointments.add_appointment"),
        can_add_patient=can_use_admin and request.user.has_perm("accounts.add_patient"),
    )

    # Guard queries as well as cards: forbidden data must never enter the context.
    if permissions["can_view_appointments"]:
        appointments = Appointment.objects.all()
        context.update(
            appointments.aggregate(
                stat_today_appointments=Count("pk", filter=Q(date=today)),
                stat_scheduled_today=Count(
                    "pk", filter=Q(date=today, status="Scheduled")
                ),
                stat_completed_today=Count(
                    "pk", filter=Q(date=today, status="Completed")
                ),
                stat_pending_appointments=Count("pk", filter=Q(status="Pending")),
            )
        )
        todays_appointments = appointments.filter(date=today).order_by("time", "pk")
        # Appointment access does not automatically grant access to patient/staff names.
        related_fields = []
        if permissions["can_view_patients"]:
            related_fields.append("patient")
        if permissions["can_view_users"]:
            related_fields.append("physician")
        if related_fields:
            todays_appointments = todays_appointments.select_related(*related_fields)
        context["todays_appointments"] = todays_appointments[:10]

        months = _last_n_months(today)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        monthly_counts = dict(
            appointments.filter(date__gte=months[0], date__lt=next_month)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Count("pk"))
            .order_by("month")
            .values_list("month", "total")
        )
        statuses = list(
            appointments.values("status").annotate(count=Count("pk")).order_by("status")
        )
        context.update(
            appointment_chart_labels=[month.strftime("%b %Y") for month in months],
            appointment_chart_counts=[monthly_counts.get(month, 0) for month in months],
            status_chart_labels=[entry["status"] for entry in statuses],
            status_chart_counts=[entry["count"] for entry in statuses],
        )

    if permissions["can_view_patients"]:
        context.update(
            Patient.objects.aggregate(
                stat_total_patients=Count("pk"),
                stat_vip_patients=Count("pk", filter=Q(is_vip=True)),
            )
        )

    if permissions["can_view_users"]:
        context["stat_total_physicians"] = User.objects.filter(role="physician").count()

    if permissions["can_view_medicines"]:
        low_stock = Q(quantity__lte=F("minimum_stock_level"))
        expired = Q(expiration_date__lt=today)
        expiring_soon = Q(expiration_date__range=(today, expiring_soon_cutoff))
        context.update(
            Medicine.objects.aggregate(
                stat_low_stock=Count("pk", filter=low_stock),
                stat_expired_medicines=Count("pk", filter=expired),
                stat_expiring_soon=Count("pk", filter=expiring_soon),
                stat_out_of_stock=Count("pk", filter=Q(quantity=0)),
            )
        )
        context.update(
            low_stock_medicines=Medicine.objects.filter(low_stock).order_by(
                "quantity", "pk"
            )[:10],
            expired_medicines=Medicine.objects.filter(expired).order_by(
                "expiration_date", "pk"
            )[:10],
            expiring_soon_medicines=Medicine.objects.filter(expiring_soon).order_by(
                "expiration_date", "pk"
            )[:10],
        )

    if permissions["can_view_prescriptions"]:
        context.update(
            Prescription.objects.aggregate(
                stat_prescriptions_month=Count(
                    "pk", filter=Q(prescription_date__date__range=(month_start, today))
                ),
                stat_follow_ups_today=Count("pk", filter=Q(follow_up_date=today)),
            )
        )
        context["upcoming_follow_ups"] = Prescription.objects.filter(
            follow_up_date__range=(today, today + timedelta(days=14))
        ).order_by("follow_up_date", "pk")[:10]

    return context
