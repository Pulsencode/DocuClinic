from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class ListDoctorPageRenderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(reverse("doctor_list"))

    def test_signup_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "doctors/doctor_list.html")
        self.assertTemplateUsed(self.response, "authenticated_base.html")

    def test_unauthenticated_page_render(self):
        self.client.logout()
        response = self.client.get(reverse("doctor_list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/doctors/doctors/")
