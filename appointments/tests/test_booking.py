from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from accounts.models import Patient
from appointments.models import Appointment, PhysicianAvailability, Weekday
from appointments.scheduling import available_slots
from clinic.models import Clinic

User = get_user_model()


class CalendarBookingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.clinic = Clinic.objects.create(
            name="Synthetic Clinic", consultation_duration=30
        )
        cls.doctor = User.objects.create_user(
            username="calendar_doctor", role="physician"
        )
        cls.patient = Patient.objects.create(
            first_name="Synthetic", last_name="Patient"
        )
        cls.day = timezone.localdate() + timedelta(days=7)
        cls.availability = PhysicianAvailability.objects.create(
            physician=cls.doctor,
            work_time_start=time(9),
            work_time_end=time(17),
            lunch_start=time(12),
            lunch_end=time(13),
        )
        cls.availability.work_days.add(
            Weekday.objects.create(name=cls.day.strftime("%A"))
        )
        cls.staff = User.objects.create_user(username="calendar_booker", is_staff=True)
        group = Group.objects.create(name="Synthetic appointment bookers")
        for app, codename in [
            ("appointments", "add_appointment"),
            ("appointments", "view_appointment"),
            ("appointments", "change_appointment"),
            ("appointments", "view_physicianavailability"),
            ("accounts", "view_user"),
            ("accounts", "view_patient"),
            ("accounts", "add_patient"),
        ]:
            group.permissions.add(
                Permission.objects.get(content_type__app_label=app, codename=codename)
            )
        cls.staff.groups.add(group)
        cls.superuser = User.objects.create_superuser(username="calendar_superuser")
        cls.denied = User.objects.create_user(username="calendar_denied", is_staff=True)

    def booking(self, **kwargs):
        data = dict(
            patient=self.patient, physician=self.doctor, date=self.day, time=time(9)
        )
        return Appointment.objects.create(**(data | kwargs))

    def slots(self, **kwargs):
        return available_slots(self.doctor.pk, self.day, days=1, **kwargs)[0]["slots"]

    def post_data(self, **kwargs):
        return dict(
            physician=self.doctor.pk,
            patient=self.patient.pk,
            date=self.day.isoformat(),
            time="09:00:00",
            status="Pending",
            **kwargs
        )

    def calendar(self, **kwargs):
        return self.client.get(
            reverse("admin:appointments_appointment_calendar"),
            dict(physician=self.doctor.pk, start=self.day.isoformat()) | kwargs,
        )

    def test_hours_lunch_and_weekdays(self):
        times = {s["start"] for s in self.slots()}
        self.assertIn("09:00:00", times)
        self.assertIn("16:30:00", times)
        self.assertNotIn("12:00:00", times)
        self.assertNotIn("17:00:00", times)
        self.assertEqual(
            available_slots(self.doctor.pk, self.day + timedelta(days=1), days=1)[0][
                "slots"
            ],
            [],
        )

    def test_repeat_visits_and_pending_reserves_cancel_releases(self):
        first = self.booking()
        self.assertEqual(first.duration_minutes, 30)
        self.booking(time=time(9, 30))
        self.assertEqual(Appointment.objects.count(), 2)
        with self.assertRaises(ValidationError):
            self.booking()
        first.status = "Cancelled"
        first.save()
        replacement = self.booking()
        with self.assertRaises(ValidationError):
            first.status = "Scheduled"
            first.save()
        self.assertEqual(replacement.status, "Pending")

    def test_direct_save_rejects_unavailable_and_past_times(self):
        for changes in [
            dict(time=time(12)),
            dict(time=time(8)),
            dict(time=time(9, 15)),
            dict(time=time(17)),
            dict(date=self.day + timedelta(days=1)),
            dict(date=timezone.localdate() - timedelta(days=7)),
            dict(time=None),
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                self.booking(**changes)

    def test_duration_snapshot_and_overlaps_after_clinic_change(self):
        self.booking()
        self.clinic.consultation_duration = 20
        self.clinic.save()
        self.assertNotIn("09:20:00", {s["start"] for s in self.slots()})
        with self.assertRaises(ValidationError):
            self.booking(time=time(9, 20))
        self.assertEqual(self.booking(time=time(9, 40)).duration_minutes, 20)

    def test_inactive_patient_doctor_and_wrong_role_rejected(self):
        self.patient.is_active = False
        self.patient.save()
        with self.assertRaises(ValidationError):
            self.booking()
        self.patient.is_active = True
        self.patient.save()
        for changes in [dict(is_active=False), dict(is_active=True, role="nurse")]:
            for field, value in changes.items():
                setattr(self.doctor, field, value)
            self.doctor.save()
            with self.assertRaises(ValidationError):
                self.booking()

    def test_missing_configuration_and_invalid_lunch(self):
        self.clinic.consultation_duration = 0
        self.clinic.save()
        with self.assertRaises(ValidationError):
            self.booking()
        self.availability.lunch_end = None
        with self.assertRaises(ValidationError):
            self.availability.save()

    def test_unchanged_historical_booking_can_be_cancelled_after_hours_change(self):
        appointment = self.booking()
        self.availability.work_time_start = time(10)
        self.availability.save()
        appointment.status = "Cancelled"
        appointment.save()
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, "Cancelled")

    def test_booking_can_be_cancelled_after_doctor_deactivation(self):
        appointment = self.booking()
        self.doctor.is_active = False
        self.doctor.save()
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("admin:appointments_appointment_change", args=[appointment.pk]),
            self.post_data() | {"status": "Cancelled"},
        )
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, "Cancelled")

    def test_endpoint_permissions_and_no_patient_details(self):
        self.booking()
        self.assertEqual(self.calendar().status_code, 302)
        self.client.force_login(self.denied)
        with CaptureQueriesContext(connection) as queries:
            self.assertEqual(self.calendar().status_code, 403)
        self.assertFalse(
            any('FROM "appointments_appointment"' in q["sql"] for q in queries)
        )
        for user in [self.staff, self.superuser]:
            self.client.force_login(user)
            response = self.calendar()
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, "Synthetic")
            self.assertNotContains(response, self.patient.registration_id)
            self.assertNotContains(response, "09:00:00")
        self.assertEqual(self.calendar(physician="invalid").status_code, 400)
        self.assertEqual(self.calendar(start="9999-12-31").status_code, 400)

    def test_calendar_requires_availability_permission_even_with_add_permission(self):
        self.denied.user_permissions.add(
            *Permission.objects.filter(codename__in=["add_appointment", "view_user"])
        )
        self.client.force_login(self.denied)
        self.assertEqual(self.calendar().status_code, 403)
        self.assertEqual(
            self.client.post(
                reverse("admin:appointments_appointment_add"), self.post_data()
            ).status_code,
            403,
        )

    def test_active_patient_autocomplete_and_forged_selection(self):
        self.client.force_login(self.staff)
        inactive = Patient.objects.create(first_name="Synthetic", is_active=False)
        response = self.client.get(
            reverse("admin:autocomplete"),
            {
                "app_label": "appointments",
                "model_name": "appointment",
                "field_name": "patient",
                "term": "Synthetic",
            },
        )
        self.assertEqual(
            [r["id"] for r in response.json()["results"]], [str(self.patient.pk)]
        )
        response = self.client.post(
            reverse("admin:appointments_appointment_add"),
            self.post_data() | {"patient": inactive.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_negative_duration_and_fractional_seconds_are_rejected(self):
        with self.assertRaises(ValidationError):
            self.booking(duration_minutes=-1)
        with self.assertRaises(ValidationError):
            self.booking(time=time(9, 0, 0, 1))

    def test_admin_add_invalid_form_save_search_edit_and_patient_popup(self):
        self.client.force_login(self.staff)
        add = reverse("admin:appointments_appointment_add")
        response = self.client.get(add)
        self.assertContains(response, 'id="id_physician"')
        self.assertContains(response, 'id="add_id_patient"')
        response = self.client.post(add, self.post_data() | {"time": "12:00:00"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This time is unavailable")
        self.assertEqual(Appointment.objects.count(), 0)
        response = self.client.post(add, self.post_data())
        self.assertEqual(response.status_code, 302)
        appointment = Appointment.objects.get()
        response = self.client.get(
            reverse("admin:appointments_appointment_changelist"), {"q": "Synthetic"}
        )
        self.assertContains(response, self.patient.registration_id)
        response = self.client.get(
            reverse("admin:appointments_appointment_change", args=[appointment.pk])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse("admin:accounts_patient_add"), {"_popup": "1"}
        )
        self.assertContains(response, 'name="_popup"')
        response = self.client.post(
            reverse("admin:accounts_patient_add") + "?_popup=1",
            {
                "first_name": "Popup",
                "last_name": "Synthetic",
                "is_active": "on",
                "_popup": "1",
            },
        )
        self.assertContains(response, "django-admin-popup-response-constants")
        self.assertTrue(Patient.objects.filter(first_name="Popup").exists())

    def test_patient_add_popup_and_autocomplete_enforce_permissions(self):
        self.client.force_login(self.denied)
        self.assertEqual(
            self.client.get(
                reverse("admin:accounts_patient_add"), {"_popup": "1"}
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                reverse("admin:autocomplete"),
                {
                    "app_label": "appointments",
                    "model_name": "appointment",
                    "field_name": "patient",
                    "term": "Synthetic",
                },
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("admin:appointments_appointment_add"), self.post_data()
            ).status_code,
            403,
        )

    def test_autocomplete_excludes_inactive_and_non_doctors(self):
        self.client.force_login(self.staff)
        User.objects.create_user(
            username="calendar_inactive", role="physician", is_active=False
        )
        response = self.client.get(
            reverse("admin:autocomplete"),
            {
                "app_label": "appointments",
                "model_name": "appointment",
                "field_name": "physician",
                "term": "calendar",
            },
        )
        self.assertEqual(
            [r["id"] for r in response.json()["results"]], [str(self.doctor.pk)]
        )
