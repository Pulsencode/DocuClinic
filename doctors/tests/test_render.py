from django.test import TestCase
from django.urls import reverse

from accounts.models import Doctor, Operator, User


class ListDoctorPageRenderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(reverse("doctor_list"))

    def test_list_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "doctors/doctor_list.html")
        self.assertTemplateUsed(self.response, "authenticated_base.html")
        self.assertTemplateNotUsed(self.response, "unauthenticated_base.html")

    def test_unauthenticated_page_render(self):
        self.client.logout()
        response = self.client.get(reverse("doctor_list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/doctors/doctors/")

    def test_page_title_in_context(self):
        self.assertIn("page_title", self.response.context)
        self.assertEqual(self.response.context["page_title"], "Doctor List")


class DoctorDetailPageRenderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.doctor = Doctor.objects.create_user(
            username="test_doctor",
            password="test_doctor_pass",
            specialization="test_specialization",
            license_number="test_license",
        )
        self.response = self.client.get(
            reverse("doctor_detail", kwargs={"pk": self.doctor.id})
        )

    def test_detail_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "doctors/doctor_detail.html")
        self.assertTemplateUsed(self.response, "authenticated_base.html")
        self.assertTemplateNotUsed(self.response, "unauthenticated_base.html")

    def test_unauthenticated_page_render(self):
        self.client.logout()
        response = self.client.get(
            reverse("doctor_detail", kwargs={"pk": self.doctor.id})
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f"/accounts/login/?next=/doctors/doctors/{self.doctor.id}/"
        )

    def test_page_title_in_context(self):
        self.assertIn("page_title", self.response.context)
        self.assertEqual(self.response.context["page_title"], "Doctor Details")


class DoctorCreatePageRenderTestCase(TestCase):
    def setUp(self):
        self.user_is_staff = Operator.objects.create_user(
            username="testuser",
            password="testpassword",
            is_staff=True,  # The user is set as is_staff because it needs to pass the UserPassesTestMixin
        )
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(reverse("doctor_create"))

    def test_create_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "doctors/create_update_doctor.html")
        self.assertTemplateUsed(self.response, "authenticated_base.html")
        self.assertTemplateNotUsed(self.response, "unauthenticated_base.html")

    def test_page_title_in_context(self):
        self.assertIn("page_title", self.response.context)
        self.assertEqual(self.response.context["page_title"], "Add Doctor")

    def test_unauthenticated_page_render(self):
        self.client.logout()
        response = self.client.get(reverse("doctor_create"))
        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('doctor_create')}"
        )


class DoctorUpdatePageRenderTestCase(TestCase):
    def setUp(self):
        self.user_is_staff = Operator.objects.create_user(
            username="testuser",
            password="testpassword",
            is_staff=True,  # The user is set as is_staff because it needs to pass the UserPassesTestMixin
        )
        self.doctor = Doctor.objects.create_user(
            username="test_doctor",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(
            reverse("doctor_update", kwargs={"pk": self.doctor.id})
        )

    def test_update_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "doctors/create_update_doctor.html")
        self.assertTemplateUsed(self.response, "authenticated_base.html")
        self.assertTemplateNotUsed(self.response, "unauthenticated_base.html")

    def test_page_title_in_context(self):
        self.assertIn("page_title", self.response.context)
        self.assertEqual(self.response.context["page_title"], "Update Doctor")

    def test_unauthenticated_page_render(self):
        self.client.logout()
        response = self.client.get(
            reverse("doctor_update", kwargs={"pk": self.doctor.id})
        )
        self.assertRedirects(
            response, f"/accounts/login/?next=/doctors/doctors/{self.doctor.id}/update/"
        )
