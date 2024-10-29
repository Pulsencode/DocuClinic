from django.test import TestCase
from django.urls import reverse


class SignUpPageRenderTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("signup"))

    def test_signup_page_renders(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_content(self):
        self.assertContains(self.response, 'name="username')
        self.assertContains(self.response, 'name="email')
        self.assertContains(self.response, 'name="phone_number')
        self.assertContains(self.response, 'name="password1')
        self.assertContains(self.response, 'name="password2')

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "registration/signup.html")
        self.assertTemplateUsed(self.response, "general_base.html")
