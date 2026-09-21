from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, router, transaction
from django.db.models import F

from accounts.models import Patient, User
from medicalrecords.models import Discount


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    physician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="physician_appointments",
        limit_choices_to={"role": "physician"},
    )
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL
    )
    consultation_fee = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, editable=False)

    class Meta:
        ordering = ["date", "time"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.patient} with {self.physician} on {self.date} {self.time}"

    def needs_scheduling_validation(self):
        if self._state.adding:
            return True
        old = (
            type(self)
            .objects.filter(pk=self.pk)
            .values("physician_id", "date", "time", "status", "duration_minutes")
            .first()
        )
        return (
            old is None
            or any(
                old[field] != getattr(self, field)
                for field in ("physician_id", "date", "time", "duration_minutes")
            )
            or (old["status"] == "Cancelled" and self.status != "Cancelled")
        )

    def clean(self):
        super().clean()
        if self.duration_minutes is not None and (
            not isinstance(self.duration_minutes, int)
            or not 1 <= self.duration_minutes <= 1440
        ):
            raise ValidationError(
                "Consultation duration must be between 1 and 1440 minutes."
            )
        if (
            self.patient_id
            and (
                self._state.adding
                or not type(self)
                .objects.filter(pk=self.pk, patient_id=self.patient_id)
                .exists()
            )
            and not Patient.objects.filter(pk=self.patient_id, is_active=True).exists()
        ):
            raise ValidationError({"patient": "Choose an active patient."})
        if self.needs_scheduling_validation():
            from .scheduling import validate_booking

            validate_booking(self)

    def save(self, *args, **kwargs):
        database = kwargs.get("using") or router.db_for_write(type(self), instance=self)
        with transaction.atomic(using=database):
            # Acquire a write lock before checking slots, including on SQLite.
            # This deliberately updates no business value and serializes bookings.
            if self.physician_id:
                PhysicianAvailability.objects.using(database).filter(
                    physician_id=self.physician_id
                ).update(work_time_start=F("work_time_start"))
            if self.needs_scheduling_validation() and self.duration_minutes is None:
                from .scheduling import consultation_duration

                self.duration_minutes = consultation_duration()
                if kwargs.get("update_fields") is not None:
                    kwargs["update_fields"] = set(kwargs["update_fields"]) | {
                        "duration_minutes"
                    }
            self.full_clean()
            return super().save(*args, **kwargs)


class Weekday(models.Model):
    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    name = models.CharField(max_length=9, choices=DAY_CHOICES, unique=True)

    class Meta:
        verbose_name = "Weekday"
        verbose_name_plural = "Weekdays"

    def __str__(self):
        return self.name


class PhysicianAvailability(models.Model):
    physician = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="physician_availability",
        limit_choices_to={"role": "physician"},
    )
    work_days = models.ManyToManyField(Weekday)
    work_time_start = models.TimeField(null=True)
    work_time_end = models.TimeField(null=True)
    lunch_start = models.TimeField(null=True, blank=True)
    lunch_end = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Physician Availability"
        verbose_name_plural = "Physician Availabilities"

    def __str__(self):
        days = ", ".join(day.get_name_display() for day in self.work_days.all())
        return f"{self.physician} available on {days}"

    def clean(self):
        super().clean()
        if self.work_time_start and self.work_time_end:
            if self.work_time_start >= self.work_time_end:
                raise ValidationError({"work_time_end": "End must be after start."})
        if bool(self.lunch_start) != bool(self.lunch_end):
            raise ValidationError("Enter both lunch times, or leave both empty.")
        if self.lunch_start and self.lunch_end:
            if not (
                self.work_time_start
                and self.work_time_end
                and self.work_time_start
                <= self.lunch_start
                < self.lunch_end
                <= self.work_time_end
            ):
                raise ValidationError("Lunch must fall within working hours.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
