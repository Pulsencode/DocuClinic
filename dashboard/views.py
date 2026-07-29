import json
from datetime import date, timedelta

from django.db.models import Count, F
from django.utils import timezone

from accounts.models import User
from appointments.models import Appointment
from inventory.models import Medicine
from medicalrecords.models import Prescription


def _last_n_months(n=5):
    today = timezone.localdate()
    year, month = today.year, today.month
    months = []

    for _ in range(n):
        months.append((year, month))
        month -= 1
        if month == 0:
            month = 12
            year -= 1

    return list(reversed(months))


def dashboard_callback(request, context):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    expiring_soon_cutoff = today + timedelta(days=30)

    todays_appointments = (
        Appointment.objects.filter(date=today)
        .select_related("patient", "physician")
        .order_by("time")
    )

    low_stock_medicines = Medicine.objects.filter(
        quantity__lte=F("minimum_stock_level")
    ).order_by("quantity")[:10]

    expired_medicines = Medicine.objects.filter(expiration_date__lt=today).order_by(
        "expiration_date"
    )[:10]

    expiring_soon_medicines = Medicine.objects.filter(
        expiration_date__gte=today,
        expiration_date__lte=expiring_soon_cutoff,
    ).order_by("expiration_date")[:10]

    upcoming_follow_ups = Prescription.objects.filter(
        follow_up_date__gte=today,
        follow_up_date__lte=today + timedelta(days=14),
    ).order_by("follow_up_date")[:10]

    appointment_labels = []
    appointment_counts = []
    for year, month in _last_n_months(5):
        appointment_labels.append(date(year, month, 1).strftime("%b %Y"))
        appointment_counts.append(
            Appointment.objects.filter(date__year=year, date__month=month).count()
        )

    status_breakdown = (
        Appointment.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
    status_labels = [entry["status"] for entry in status_breakdown]
    status_counts = [entry["count"] for entry in status_breakdown]

    context.update(
        {
            "today": today,
            "stat_today_appointments": todays_appointments.count(),
            "stat_total_patients": User.objects.filter(role="patient").count(),
            "stat_total_physicians": User.objects.filter(role="physician").count(),
            "stat_pending_appointments": Appointment.objects.filter(
                status="Pending"
            ).count(),
            "stat_scheduled_today": todays_appointments.filter(
                status="Scheduled"
            ).count(),
            "stat_completed_today": todays_appointments.filter(
                status="Completed"
            ).count(),
            "stat_low_stock": Medicine.objects.filter(
                quantity__lte=F("minimum_stock_level")
            ).count(),
            "stat_expired_medicines": Medicine.objects.filter(
                expiration_date__lt=today
            ).count(),
            "stat_expiring_soon": Medicine.objects.filter(
                expiration_date__gte=today,
                expiration_date__lte=expiring_soon_cutoff,
            ).count(),
            "stat_prescriptions_month": Prescription.objects.filter(
                prescription_date__date__gte=month_start
            ).count(),
            # "stat_vip_patients": PatientProfile.objects.filter(is_vip=True).count(),
            "todays_appointments": todays_appointments,
            "low_stock_medicines": low_stock_medicines,
            "expired_medicines": expired_medicines,
            "expiring_soon_medicines": expiring_soon_medicines,
            "upcoming_follow_ups": upcoming_follow_ups,
            "appointment_chart_labels": json.dumps(appointment_labels),
            "appointment_chart_counts": json.dumps(appointment_counts),
            "status_chart_labels": json.dumps(status_labels),
            "status_chart_counts": json.dumps(status_counts),
        }
    )

    return context
