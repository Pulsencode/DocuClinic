import secrets

from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AdminPasswordResetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.old_password = secrets.token_urlsafe(24)
        cls.new_password = secrets.token_urlsafe(24)
        cls.superadmin = User.objects.create_superuser(
            username="test_superadmin", password=secrets.token_urlsafe(24), role="admin"
        )
        cls.target = User.objects.create_user(
            username="test_physician",
            password=cls.old_password,
            role="physician",
            is_staff=True,
        )
        cls.editor = User.objects.create_user(
            username="test_editor",
            password=secrets.token_urlsafe(24),
            role="admin",
            is_staff=True,
        )
        cls.editor.user_permissions.add(
            Permission.objects.get(
                codename="change_user", content_type__app_label="accounts"
            )
        )

    def setUp(self):
        self.reset_url = reverse(
            "admin:auth_user_password_change", args=[self.target.pk]
        )
        self.change_url = reverse("admin:accounts_user_change", args=[self.target.pk])
        self.client.force_login(self.superadmin)

    def password_data(self, password=None):
        password = self.new_password if password is None else password
        return {"password1": password, "password2": password}

    def test_superadmin_sees_reset_link_and_unfold_form(self):
        response = self.client.get(self.change_url)
        self.assertContains(response, f'href="{self.reset_url}"')
        self.assertContains(response, "Reset password")
        response = self.client.get(self.reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/auth/user/change_password.html")
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
        self.assertNotContains(response, 'name="old_password"')
        self.assertTrue(
            response.context["form"].fields["password1"].widget.attrs["class"]
        )

    def test_reset_changes_login_and_logs_action_without_passwords(self):
        response = self.client.post(self.reset_url, self.password_data())
        self.assertRedirects(response, self.change_url)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password(self.new_password))
        self.assertNotEqual(self.target.password, self.new_password)
        self.assertIsNone(
            authenticate(username=self.target.username, password=self.old_password)
        )
        self.assertEqual(
            authenticate(username=self.target.username, password=self.new_password),
            self.target,
        )
        entry = LogEntry.objects.get(object_id=str(self.target.pk), action_flag=CHANGE)
        self.assertEqual(entry.user_id, self.superadmin.pk)
        self.assertNotIn(self.old_password, entry.change_message)
        self.assertNotIn(self.new_password, entry.change_message)
        self.assertNotIn(self.target.password, entry.change_message)

    def test_weak_mismatched_and_empty_passwords_are_rejected(self):
        attempts = [
            self.password_data("123"),
            {"password1": self.new_password, "password2": secrets.token_urlsafe(24)},
            self.password_data(""),
        ]
        for index, data in enumerate(attempts):
            with self.subTest(attempt=index):
                response = self.client.post(self.reset_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.target.refresh_from_db()
                self.assertTrue(self.target.check_password(self.old_password))
        self.assertFalse(LogEntry.objects.exists())

    def test_user_editor_cannot_access_or_submit_reset(self):
        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(self.reset_url).status_code, 403)
        self.assertEqual(
            self.client.post(self.reset_url, self.password_data()).status_code, 403
        )
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password(self.old_password))
        response = self.client.get(self.change_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f'href="{self.reset_url}"')
        self.assertContains(response, "Only a superadmin")

    def test_staff_without_user_permissions_cannot_reset(self):
        self.client.force_login(self.target)
        self.assertEqual(self.client.get(self.reset_url).status_code, 403)
        self.assertEqual(
            self.client.post(self.reset_url, self.password_data()).status_code, 403
        )

    def test_anonymous_requests_require_login(self):
        self.client.logout()
        login_url = reverse("admin:login")
        for response in (
            self.client.get(self.reset_url),
            self.client.post(self.reset_url, self.password_data()),
        ):
            self.assertRedirects(response, f"{login_url}?next={self.reset_url}")

    def test_user_editor_cannot_promote_self_or_submit_password_on_edit_form(self):
        self.client.force_login(self.editor)
        url = reverse("admin:accounts_user_change", args=[self.editor.pk])
        response = self.client.post(
            url,
            {
                "username": self.editor.username,
                "role": "admin",
                "is_active": "on",
                "is_staff": "on",
                "is_superuser": "on",
                "user_permissions": list(
                    Permission.objects.values_list("pk", flat=True)
                ),
                "password": self.new_password,
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302)
        previous_hash = self.editor.password
        self.editor.refresh_from_db()
        self.assertFalse(self.editor.is_superuser)
        self.assertEqual(self.editor.user_permissions.count(), 1)
        self.assertEqual(self.editor.password, previous_hash)
        self.assertEqual(
            self.client.post(self.reset_url, self.password_data()).status_code, 403
        )

    def test_user_editor_cannot_edit_superadmin(self):
        self.client.force_login(self.editor)
        url = reverse("admin:accounts_user_change", args=[self.superadmin.pk])
        self.assertEqual(
            self.client.post(url, {"username": "changed"}).status_code, 403
        )
        self.superadmin.refresh_from_db()
        self.assertEqual(self.superadmin.username, "test_superadmin")

    def test_reset_invalidates_target_session_but_preserves_superadmin_session(self):
        target_client = Client()
        target_client.force_login(self.target)
        self.client.post(self.reset_url, self.password_data())
        self.assertEqual(
            target_client.get(reverse("admin:password_change")).status_code, 302
        )
        self.assertNotIn("_auth_user_id", target_client.session)
        self.assertEqual(self.client.get(self.change_url).status_code, 200)

    def test_superadmin_can_set_password_for_unusable_password_account(self):
        self.target.set_unusable_password()
        self.target.save()
        response = self.client.post(self.reset_url, self.password_data())
        self.assertRedirects(response, self.change_url)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password(self.new_password))

    def test_reset_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.superadmin)
        response = client.post(self.reset_url, self.password_data())
        self.assertEqual(response.status_code, 403)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password(self.old_password))

    def test_superadmin_can_reset_own_password_and_stay_logged_in(self):
        url = reverse("admin:auth_user_password_change", args=[self.superadmin.pk])
        response = self.client.post(url, self.password_data())
        self.assertRedirects(
            response, reverse("admin:accounts_user_change", args=[self.superadmin.pk])
        )
        self.superadmin.refresh_from_db()
        self.assertTrue(self.superadmin.check_password(self.new_password))
        self.assertEqual(self.client.get(self.change_url).status_code, 200)

    def test_superadmin_can_reset_another_superadmin(self):
        self.target.is_superuser = True
        self.target.save()
        response = self.client.post(self.reset_url, self.password_data())
        self.assertRedirects(response, self.change_url)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password(self.new_password))

    def test_superadmin_can_still_create_users(self):
        url = reverse("admin:accounts_user_add")
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(
            url,
            {
                "username": "test_new_staff",
                "role": "nurse",
                "is_active": "on",
                "is_staff": "on",
                **self.password_data(),
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="test_new_staff")
        self.assertTrue(user.check_password(self.new_password))
