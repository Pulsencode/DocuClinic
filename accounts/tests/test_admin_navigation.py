from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.urls import reverse

User = get_user_model()


class AdminNavigationTests(TestCase):
    model_links = {
        "clinic.clinic": "Clinic Settings",
        "accounts.patient": "Patients",
        "accounts.user": "All Users",
        "appointments.appointment": "Appointments",
        "appointments.physicianavailability": "Physician Availability",
        "appointments.weekday": "Weekdays",
        "medicalrecords.prescription": "Prescriptions",
        "medicalrecords.prescriptionmedicine": "Prescription Medicines",
        "medicalrecords.discount": "Discounts",
        "inventory.medicine": "Medicines",
        "inventory.routeofadministration": "Routes of Administration",
        "inventory.medicinesupplier": "Suppliers",
    }

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username="navigation_staff", role="receptionist", is_staff=True
        )
        cls.superadmin = User.objects.create_superuser(username="navigation_superadmin")

    def navigation(self, user):
        request = RequestFactory().get(reverse("admin:index"))
        request.user = user
        return admin.site.get_sidebar_list(request)

    def visible_titles(self, user):
        return {
            item["title"]
            for group in self.navigation(user)
            for item in group["items"]
            if item["has_permission"]
        }

    def permission(self, model_label, action="view"):
        app_label, model_name = model_label.split(".")
        return Permission.objects.get(
            content_type__app_label=app_label, codename=f"{action}_{model_name}"
        )

    def test_superadmin_sees_every_configured_option(self):
        self.assertEqual(
            self.visible_titles(self.superadmin),
            {"Dashboard", *self.model_links.values()},
        )

    def test_staff_without_model_permissions_only_sees_dashboard(self):
        self.assertEqual(self.visible_titles(self.staff), {"Dashboard"})

    def test_each_view_or_change_permission_shows_only_its_model_link(self):
        for model_label, title in self.model_links.items():
            for action in ("view", "change"):
                with self.subTest(model=model_label, action=action):
                    self.staff.user_permissions.set(
                        [self.permission(model_label, action)]
                    )
                    # Django caches permissions on the user object during a request.
                    user = User.objects.get(pk=self.staff.pk)
                    self.assertEqual(self.visible_titles(user), {"Dashboard", title})

    def test_group_permissions_are_respected(self):
        group = Group.objects.create(name="Patient viewers")
        group.permissions.add(self.permission("accounts.patient"))
        self.staff.groups.add(group)
        self.assertEqual(self.visible_titles(self.staff), {"Dashboard", "Patients"})

    def test_add_or_delete_permission_does_not_grant_list_access(self):
        self.staff.user_permissions.set(
            [
                self.permission("accounts.patient", action)
                for action in ("add", "delete")
            ]
        )
        self.assertEqual(self.visible_titles(self.staff), {"Dashboard"})

    def test_supplier_directory_permission_does_not_grant_pricing_list_access(self):
        self.staff.user_permissions.add(self.permission("inventory.supplier"))
        self.assertEqual(self.visible_titles(self.staff), {"Dashboard"})

    def test_anonymous_inactive_and_nonstaff_users_have_no_navigation_access(self):
        self.assertEqual(self.visible_titles(AnonymousUser()), set())
        for field in ("is_active", "is_staff"):
            with self.subTest(field=field):
                user = User.objects.get(pk=self.superadmin.pk)
                setattr(user, field, False)
                self.assertEqual(self.visible_titles(user), set())

    def test_hidden_links_are_not_rendered_in_sidebar_html(self):
        self.staff.user_permissions.add(self.permission("accounts.patient"))
        html = render_to_string(
            "unfold/helpers/app_list.html",
            {"sidebar_navigation": self.navigation(self.staff)},
        )
        self.assertIn(f'href="{reverse("admin:accounts_patient_changelist")}"', html)
        self.assertNotIn(f'href="{reverse("admin:accounts_user_changelist")}"', html)
        self.assertNotIn(
            f'href="{reverse("admin:inventory_medicine_changelist")}"', html
        )

    def test_direct_patient_list_access_still_requires_permission(self):
        self.client.force_login(self.staff)
        url = reverse("admin:accounts_patient_changelist")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.staff.user_permissions.add(self.permission("accounts.patient"))
        self.assertEqual(self.client.get(url).status_code, 200)
