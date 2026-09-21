from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from accounts.models import Patient
from appointments.models import Appointment, PhysicianAvailability, Weekday
from clinic.models import Clinic


class AppointmentCalendarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user(username="calendar_viewer", is_staff=True)
        cls.denied = User.objects.create_user(username="calendar_denied", is_staff=True)
        cls.superuser = User.objects.create_superuser(username="calendar_superadmin")
        cls.physician = User.objects.create_user(
            username="synthetic_doctor", first_name="PrivateDoctor", role="physician"
        )
        cls.patient = Patient.objects.create(
            first_name="PrivatePatient", last_name="Calendar"
        )
        cls.day = timezone.localdate() + timedelta(days=7)
        Clinic.objects.create(name="Synthetic clinic", consultation_duration=30)
        availability = PhysicianAvailability.objects.create(
            physician=cls.physician, work_time_start=time(8), work_time_end=time(18)
        )
        availability.work_days.add(Weekday.objects.create(name=cls.day.strftime("%A")))
        cls.appointment = Appointment.objects.create(
            patient=cls.patient,
            physician=cls.physician,
            date=cls.day,
            time=time(9, 30),
            status="Scheduled",
        )
        cls.events_url = reverse("admin:appointments_appointment_events")
        cls.page_url = reverse("admin:appointments_appointment_changelist")

    def grant(self, *codenames):
        self.staff.user_permissions.set(
            Permission.objects.filter(codename__in=codenames)
        )
        self.client.force_login(self.staff)

    def events(self, **kwargs):
        return self.client.get(
            self.events_url,
            {
                "start": self.day.isoformat(),
                "end": (self.day + timedelta(days=7)).isoformat(),
                **kwargs,
            },
        )

    def test_calendar_is_default_and_standard_form_fallback_works(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.page_url)
        self.assertContains(response, 'id="appointment-schedule"')
        self.assertNotContains(response, 'id="result_list"')
        self.assertEqual(response.context["calendar_config"]["view"], "week")
        self.assertContains(response, "appointment-calendar-config")
        self.assertContains(response, "View/Edit Details")
        self.assertContains(
            self.client.get(
                reverse(
                    "admin:appointments_appointment_change", args=[self.appointment.pk]
                )
            ),
            'id="id_patient"',
        )
        self.assertContains(
            self.client.get(reverse("admin:appointments_appointment_add")),
            'id="id_physician"',
        )

    def test_permissions_for_page_and_feed(self):
        self.assertEqual(self.client.get(self.page_url).status_code, 302)
        self.assertEqual(self.events().status_code, 302)
        self.client.force_login(self.denied)
        for url in [self.page_url, self.events_url]:
            with CaptureQueriesContext(connection) as captured:
                response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertFalse(
                any('FROM "appointments_appointment"' in q["sql"] for q in captured)
            )

    def test_appointment_only_permission_excludes_related_data_and_queries(self):
        self.grant("view_appointment")
        for url in [self.page_url, self.events_url]:
            with CaptureQueriesContext(connection) as captured:
                response = self.client.get(
                    url,
                    (
                        {
                            "start": self.day.isoformat(),
                            "end": (self.day + timedelta(days=1)).isoformat(),
                        }
                        if url == self.events_url
                        else {}
                    ),
                )
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, "PrivatePatient")
            self.assertNotContains(response, "PrivateDoctor")
            self.assertFalse(
                any(
                    '"accounts_patient"' in q["sql"]
                    or 'JOIN "accounts_user"' in q["sql"]
                    for q in captured
                )
            )
        event = self.events().json()["events"][0]
        self.assertEqual(event["patient"], "Patient details restricted")
        self.assertEqual(event["physician"], "Physician details restricted")
        self.assertEqual(self.events(q="PrivatePatient").status_code, 403)
        self.assertEqual(self.events(physician=self.physician.pk).status_code, 403)

    def test_allowed_group_and_superuser_receive_details_and_existing_edit_url(self):
        group = Group.objects.create(name="Calendar readers")
        group.permissions.set(
            Permission.objects.filter(
                codename__in=["view_appointment", "view_patient", "view_user"]
            )
        )
        self.staff.groups.add(group)
        for user in [self.staff, self.superuser]:
            self.client.force_login(user)
            event = self.events().json()["events"][0]
            self.assertEqual(event["patient"], "PrivatePatient Calendar")
            self.assertEqual(event["physician"], "PrivateDoctor")
            self.assertEqual(event["date"], self.day.isoformat())
            self.assertEqual(event["time"], "09:30:00")
            self.assertEqual(event["duration"], 30)
            self.assertEqual(event["reason"], "Not recorded")
            self.assertEqual(
                event["url"],
                reverse(
                    "admin:appointments_appointment_change", args=[self.appointment.pk]
                ),
            )

    def test_separate_related_permissions(self):
        self.grant("change_appointment", "change_patient")
        event = self.events().json()["events"][0]
        self.assertEqual(event["patient"], "PrivatePatient Calendar")
        self.assertEqual(event["physician"], "Physician details restricted")
        self.grant("view_appointment", "view_user")
        event = self.events().json()["events"][0]
        self.assertEqual(event["patient"], "Patient details restricted")
        self.assertEqual(event["physician"], "PrivateDoctor")

    def test_date_range_filters_and_empty_states(self):
        self.client.force_login(self.superuser)
        self.assertEqual(self.events(status="Cancelled").json()["events"], [])
        self.assertEqual(
            len(
                self.events(
                    status="Scheduled", q="PrivatePatient", physician=self.physician.pk
                ).json()["events"]
            ),
            1,
        )
        self.assertEqual(
            self.events(start=(self.day + timedelta(days=2)).isoformat()).json()[
                "events"
            ],
            [],
        )
        for overrides in [
            dict(start="not-a-date"),
            dict(end=self.day.isoformat()),
            dict(end=(self.day + timedelta(days=43)).isoformat()),
            dict(status="bad"),
            dict(physician="bad"),
        ]:
            with self.subTest(overrides=overrides):
                self.assertEqual(self.events(**overrides).status_code, 400)

    def test_legacy_unscheduled_records_remain_accessible(self):
        # Simulate a pre-validation row with no time; the calendar does not alter it.
        Appointment.objects.filter(pk=self.appointment.pk).update(time=None)
        self.client.force_login(self.superuser)
        self.assertEqual(self.events().json(), {"events": [], "unscheduled": 1})
        response = self.client.get(reverse("admin:appointments_appointment_table"))
        self.assertContains(response, "PrivatePatient")
        self.assertContains(response, "Calendar view")
        self.assertContains(
            self.client.get(self.page_url, {"q": "PrivatePatient"}), "PrivatePatient"
        )

    def test_calendar_does_not_modify_rows_and_retains_cancelled_events(self):
        self.appointment.status = "Cancelled"
        self.appointment.save()
        before = list(Appointment.objects.values())
        self.client.force_login(self.superuser)
        self.assertEqual(self.events().json()["events"][0]["status"], "Cancelled")
        self.client.get(self.page_url, {"view": "month", "date": self.day.isoformat()})
        self.assertEqual(list(Appointment.objects.values()), before)

    def test_config_is_escaped_and_invalid_state_falls_back(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            self.page_url, {"view": "</script><script>alert(1)</script>", "date": "bad"}
        )
        self.assertEqual(response.context["calendar_config"]["view"], "week")
        self.assertNotContains(response, "alert(1)")

    def test_add_link_requires_add_and_related_permissions(self):
        self.grant("view_appointment", "view_patient", "view_user")
        self.assertNotContains(self.client.get(self.page_url), "New appointment")
        self.grant(
            "view_appointment",
            "add_appointment",
            "view_patient",
            "view_user",
            "view_physicianavailability",
        )
        self.assertContains(self.client.get(self.page_url), "New appointment")

    def test_bounded_queries_do_not_grow_with_event_count(self):
        self.client.force_login(self.superuser)
        with CaptureQueriesContext(connection) as initial:
            self.events()
        Appointment.objects.create(
            patient=self.patient, physician=self.physician, date=self.day, time=time(10)
        )
        with CaptureQueriesContext(connection) as additional:
            self.events()
        self.assertEqual(len(initial), len(additional))
