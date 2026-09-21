from concurrent.futures import ThreadPoolExecutor
from datetime import time, timedelta
from threading import Barrier

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import OperationalError, connections
from django.test import TransactionTestCase
from django.utils import timezone

from accounts.models import Patient
from appointments.models import Appointment, PhysicianAvailability, Weekday
from clinic.models import Clinic


class ConcurrentBookingTests(TransactionTestCase):
    def test_competing_bookings_never_both_succeed(self):
        Clinic.objects.create(name="Synthetic", consultation_duration=30)
        doctor = get_user_model().objects.create(
            username="concurrent_doctor", role="physician"
        )
        patient = Patient.objects.create(first_name="Synthetic")
        day = timezone.localdate() + timedelta(days=7)
        availability = PhysicianAvailability.objects.create(
            physician=doctor, work_time_start=time(9), work_time_end=time(17)
        )
        availability.work_days.add(Weekday.objects.create(name=day.strftime("%A")))
        barrier = Barrier(2)

        def book():
            try:
                barrier.wait(timeout=10)
                Appointment.objects.create(
                    physician_id=doctor.pk,
                    patient_id=patient.pk,
                    date=day,
                    time=time(9),
                )
                return "saved"
            except ValidationError:
                return "unavailable"
            except OperationalError as error:
                if "locked" not in str(error).lower():
                    raise
                return "retry"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: book(), range(2)))
        self.assertEqual(outcomes.count("saved"), 1)
        self.assertEqual(Appointment.objects.count(), 1)
