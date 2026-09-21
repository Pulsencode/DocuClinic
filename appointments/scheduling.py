"""Shared calendar and write-time rules. All displayed times are clinic local time."""

from datetime import date, datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from clinic.models import Clinic

from .models import Appointment, PhysicianAvailability


def consultation_duration():
    duration = Clinic.objects.values_list("consultation_duration", flat=True).first()
    if not duration or duration > 1440:
        raise ValidationError(
            "Set a valid consultation duration in Clinic Settings first."
        )
    return duration


def available_slots(physician_id, start_date, days=7, exclude=None, duration=None):
    duration = duration or consultation_duration()
    if not isinstance(duration, int) or not 1 <= duration <= 1440:
        raise ValidationError(
            "Consultation duration must be between 1 and 1440 minutes."
        )
    availability = (
        PhysicianAvailability.objects.select_related("physician")
        .prefetch_related("work_days")
        .filter(
            physician_id=physician_id,
            physician__role="physician",
            physician__is_active=True,
        )
        .first()
    )
    if availability is None:
        raise ValidationError("This doctor has no availability configured.")
    availability.full_clean()
    if not availability.work_time_start or not availability.work_time_end:
        raise ValidationError("Set this doctor's working hours first.")
    weekdays = {day.name for day in availability.work_days.all()}
    bookings = Appointment.objects.filter(
        physician_id=physician_id,
        date__gte=start_date,
        date__lt=start_date + timedelta(days=days),
    ).exclude(status="Cancelled")
    if exclude is not None:
        bookings = bookings.exclude(pk=exclude)
    occupied = {}
    for day, clock, minutes in bookings.values_list("date", "time", "duration_minutes"):
        if clock is not None:
            begin = datetime.combine(day, clock)
            occupied.setdefault(day, []).append(
                (begin, begin + timedelta(minutes=minutes or duration))
            )
    now = timezone.localtime()
    result = []
    for offset in range(days):
        day = start_date + timedelta(days=offset)
        slots = []
        if day.strftime("%A") in weekdays:
            segments = [(availability.work_time_start, availability.work_time_end)]
            if availability.lunch_start:
                segments = [
                    (availability.work_time_start, availability.lunch_start),
                    (availability.lunch_end, availability.work_time_end),
                ]
            for begin, end in segments:
                cursor = datetime.combine(day, begin)
                finish = datetime.combine(day, end)
                while cursor + timedelta(minutes=duration) <= finish:
                    slot_end = cursor + timedelta(minutes=duration)
                    if timezone.make_aware(cursor) > now and not any(
                        cursor < busy_end and slot_end > busy_start
                        for busy_start, busy_end in occupied.get(day, [])
                    ):
                        slots.append(
                            {
                                "start": cursor.strftime("%H:%M:%S"),
                                "end": slot_end.strftime("%H:%M:%S"),
                            }
                        )
                    cursor = slot_end
        result.append({"date": day.isoformat(), "slots": slots})
    return result


def validate_booking(appointment):
    errors = {}
    if not isinstance(appointment.date, date):
        errors["date"] = "Choose a date on the calendar."
    if not isinstance(appointment.time, time):
        errors["time"] = "Choose an available time on the calendar."
    elif appointment.time.microsecond:
        errors["time"] = "Choose an exact calendar time without fractional seconds."
    if errors:
        raise ValidationError(errors)
    if not appointment.physician_id:
        return  # Required-field validation supplies the error.
    duration = appointment.duration_minutes or consultation_duration()
    days = available_slots(
        appointment.physician_id,
        appointment.date,
        days=1,
        exclude=appointment.pk,
        duration=duration,
    )
    if appointment.time.strftime("%H:%M:%S") not in {
        slot["start"] for slot in days[0]["slots"]
    }:
        raise ValidationError(
            {"time": "This time is unavailable. Choose another calendar slot."}
        )
