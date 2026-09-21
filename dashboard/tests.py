from datetime import date, datetime, time, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.db import connection
from django.db.models import QuerySet
from django.test import RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from accounts.models import Patient
from appointments.models import Appointment, PhysicianAvailability, Weekday
from clinic.models import Clinic
from dashboard.views import _last_n_months, dashboard_callback
from inventory.models import Medicine
from medicalrecords.models import Prescription

User = get_user_model()


class DashboardPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.today = timezone.localdate()
        cls.staff = User.objects.create_user(username="dashboard_staff", is_staff=True)
        cls.superadmin = User.objects.create_superuser(username="dashboard_superadmin")
        cls.physician = User.objects.create_user(
            username="dashboard_physician",
            first_name="SyntheticPhysician",
            role="physician",
        )
        cls.patient = Patient.objects.create(first_name="SyntheticPatient", is_vip=True)
        Clinic.objects.create(name="Synthetic Clinic", consultation_duration=30)
        availability = PhysicianAvailability.objects.create(
            physician=cls.physician,
            work_time_start=time(9),
            work_time_end=time(17),
        )
        availability.work_days.add(
            Weekday.objects.create(name=cls.today.strftime("%A"))
        )
        # Book this dashboard fixture before its consultation starts, regardless
        # of the wall-clock time at which the suite runs.
        with patch(
            "django.utils.timezone.now",
            return_value=timezone.make_aware(datetime.combine(cls.today, time(8))),
        ):
            cls.appointment = Appointment.objects.create(
                patient=cls.patient,
                physician=cls.physician,
                date=cls.today,
                time="10:00",
                status="Pending",
            )
        for name, quantity, days in [
            ("SyntheticOutOfStock", 0, 10),
            ("SyntheticExpired", 2, -1),
            ("SyntheticExpiresToday", 3, 0),
            ("SyntheticExpiresSoon", 4, 30),
            ("SyntheticExpiresLater", 5, 31),
        ]:
            Medicine.objects.create(
                name=name,
                generic_name=name,
                brand_name=name,
                quantity=quantity,
                expiration_date=cls.today + timedelta(days=days),
                purchase_date=cls.today,
                minimum_stock_level=3,
                maximum_stock_level=10,
                storage_location="Synthetic shelf",
            )
        for days in (-1, 0, 14, 15):
            Prescription.objects.create(
                patient=cls.patient,
                physician=cls.physician,
                diagnosis=f"SyntheticDiagnosis{days}",
                follow_up_date=cls.today + timedelta(days=days),
            )

    def grant(self, *permissions):
        for permission in permissions:
            app_label, codename = permission.split(".")
            self.staff.user_permissions.add(
                Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
            )
        self.staff = User.objects.get(pk=self.staff.pk)
        return self.staff

    def context_for(self, user):
        request = RequestFactory().get(reverse("admin:index"))
        request.user = user
        return dashboard_callback(request, {})

    def dashboard(self, user):
        self.client.force_login(user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        return response

    def test_staff_without_permissions_gets_no_data_or_domain_queries(self):
        self.staff.get_all_permissions()
        with self.assertNumQueries(0):
            context = self.context_for(self.staff)
        self.assertFalse(context["has_dashboard_data"])
        self.assertFalse(any(key.startswith("stat_") for key in context))
        response = self.dashboard(self.staff)
        self.assertContains(response, "No dashboard data is available")
        for value in (
            "SyntheticPatient",
            "SyntheticPhysician",
            "SyntheticDiagnosis",
            "SyntheticOutOfStock",
            "appointment-chart-labels",
            "apexcharts.min.js",
        ):
            self.assertNotContains(response, value)

    def test_each_domain_only_queries_its_permitted_tables(self):
        domains = [
            (
                "appointments.view_appointment",
                "stat_today_appointments",
                "appointments_appointment",
            ),
            ("accounts.view_patient", "stat_total_patients", "accounts_patient"),
            ("accounts.view_user", "stat_total_physicians", "accounts_user"),
            ("inventory.view_medicine", "stat_low_stock", "inventory_medicine"),
            (
                "medicalrecords.view_prescription",
                "stat_prescriptions_month",
                "medicalrecords_prescription",
            ),
        ]
        for permission, expected_stat, allowed_table in domains:
            with self.subTest(permission=permission):
                self.staff.user_permissions.clear()
                user = self.grant(permission)
                user.get_all_permissions()
                with CaptureQueriesContext(connection) as queries:
                    context = self.context_for(user)
                    for value in context.values():
                        if isinstance(value, QuerySet):
                            list(value)
                self.assertIn(expected_stat, context)
                sql = " ".join(query["sql"] for query in queries)
                self.assertIn(allowed_table, sql)
                for _, other_stat, other_table in domains:
                    if other_table != allowed_table:
                        self.assertNotIn(other_stat, context)
                        self.assertNotIn(other_table, sql)

    def test_appointment_access_does_not_reveal_related_names_or_prescriptions(self):
        response = self.dashboard(self.grant("appointments.view_appointment"))
        self.assertContains(response, "appointment-column-chart")
        self.assertContains(response, "appointment-status-chart")
        self.assertContains(response, "10:00")
        for value in (
            "SyntheticPatient",
            "SyntheticPhysician",
            "SyntheticDiagnosis",
            "Prescriptions This Month",
            "Follow-ups Due Today",
            "New Appointment",
        ):
            self.assertNotContains(response, value)

    def test_related_names_appear_only_with_their_own_permissions(self):
        user = self.grant("appointments.view_appointment", "accounts.view_patient")
        response = self.dashboard(user)
        self.assertContains(response, "SyntheticPatient")
        self.assertNotContains(response, "SyntheticPhysician")
        response = self.dashboard(self.grant("accounts.view_user"))
        self.assertContains(response, "SyntheticPhysician")

    def test_patient_totals_use_separate_patient_records(self):
        response = self.dashboard(self.grant("accounts.view_patient"))
        self.assertEqual(response.context["stat_total_patients"], 1)
        self.assertEqual(response.context["stat_vip_patients"], 1)
        self.assertContains(response, "Total Patients")
        self.assertNotContains(response, "appointment-chart-labels")
        self.assertNotContains(response, "SyntheticDiagnosis")

    def test_inventory_counts_and_expiry_boundaries(self):
        response = self.dashboard(self.grant("inventory.view_medicine"))
        for key, value in {
            "stat_low_stock": 3,
            "stat_expired_medicines": 1,
            "stat_expiring_soon": 3,
            "stat_out_of_stock": 1,
        }.items():
            self.assertEqual(response.context[key], value)
        self.assertContains(response, "Out of Stock")
        self.assertContains(response, "SyntheticOutOfStock")
        self.assertNotContains(response, "SyntheticExpiresLater")
        self.assertNotContains(response, "SyntheticDiagnosis")

    def test_prescription_group_permission_and_followup_boundaries(self):
        group = Group.objects.create(name="Dashboard prescription readers")
        group.permissions.add(
            Permission.objects.get(
                content_type__app_label="medicalrecords", codename="view_prescription"
            )
        )
        self.staff.groups.add(group)
        response = self.dashboard(self.staff)
        self.assertEqual(response.context["stat_follow_ups_today"], 1)
        self.assertEqual(response.context["stat_prescriptions_month"], 4)
        self.assertContains(response, "Follow-ups Due Today")
        self.assertContains(response, "SyntheticDiagnosis0")
        self.assertContains(response, "SyntheticDiagnosis14")
        self.assertNotContains(response, "SyntheticDiagnosis-1")
        self.assertNotContains(response, "SyntheticDiagnosis15")
        self.assertNotContains(response, "SyntheticPatient")
        self.assertNotContains(response, "appointment-chart-labels")

    def test_change_permission_also_allows_cards(self):
        for model, flag in [
            ("accounts.patient", "can_view_patients"),
            ("accounts.user", "can_view_users"),
            ("appointments.appointment", "can_view_appointments"),
            ("inventory.medicine", "can_view_medicines"),
            ("medicalrecords.prescription", "can_view_prescriptions"),
        ]:
            with self.subTest(model=model):
                self.staff.user_permissions.clear()
                app, name = model.split(".")
                context = self.context_for(self.grant(f"{app}.change_{name}"))
                self.assertTrue(context[flag])
                self.assertEqual(
                    sum(
                        value
                        for key, value in context.items()
                        if key.startswith("can_view_")
                    ),
                    1,
                )

    def test_quick_actions_require_add_permission(self):
        response = self.dashboard(
            self.grant("accounts.add_patient", "appointments.add_appointment")
        )
        self.assertContains(response, f'href="{reverse("admin:accounts_patient_add")}"')
        self.assertContains(
            response, f'href="{reverse("admin:appointments_appointment_add")}"'
        )
        self.assertFalse(response.context["has_dashboard_data"])
        self.assertNotContains(response, "appointment-chart-labels")

    def test_superadmin_sees_all_sections_and_correct_chart_counts(self):
        response = self.dashboard(self.superadmin)
        for title in (
            "Appointment Activity",
            "Appointment Status",
            "Total Patients",
            "Physicians",
            "Low Stock Inventory",
            "Upcoming Follow-ups",
            "Out of Stock",
            "Follow-ups Due Today",
        ):
            self.assertContains(response, title)
        self.assertEqual(response.context["appointment_chart_counts"], [0, 0, 0, 0, 1])
        self.assertEqual(response.context["status_chart_labels"], ["Pending"])
        self.assertEqual(response.context["status_chart_counts"], [1])
        self.assertContains(response, "SyntheticPatient")
        self.assertContains(response, "SyntheticPhysician")

    def test_chart_json_escapes_untrusted_status_values(self):
        value = "</script><script>alert(1)</script>"
        Appointment.objects.filter(pk=self.appointment.pk).update(status=value)
        response = self.dashboard(self.grant("appointments.view_appointment"))
        self.assertNotContains(response, value)
        self.assertContains(response, r"\u003C/script\u003E")

    def test_anonymous_inactive_and_nonstaff_callbacks_return_no_data(self):
        users = [AnonymousUser()]
        for field in ("is_active", "is_staff"):
            user = User.objects.get(pk=self.superadmin.pk)
            setattr(user, field, False)
            users.append(user)
        for user in users:
            with self.assertNumQueries(0):
                context = self.context_for(user)
            self.assertFalse(context["has_dashboard_data"])
            self.assertFalse(context["can_add_patient"])
            self.assertFalse(context["can_add_appointment"])

    def test_five_month_chart_handles_year_boundary(self):
        self.assertEqual(
            _last_n_months(date(2026, 1, 10)),
            [
                date(2025, 9, 1),
                date(2025, 10, 1),
                date(2025, 11, 1),
                date(2025, 12, 1),
                date(2026, 1, 1),
            ],
        )
