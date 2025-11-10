from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignUpForm
from accounts.models import Profile
from tests.factories import create_user


class SignUpFormTests(TestCase):
    def test_email_must_be_unique(self):
        create_user(username="existing", email="existing@example.com")
        form = SignUpForm(
            data={
                "username": "newuser",
                "email": "existing@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class SignUpViewTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        payload = {
            "username": "hossein",
            "email": "hossein@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Hossein",
            "last_name": "G",
            "newsletter_opt_in": "on",
        }
        response = self.client.post(reverse("accounts:signup"), payload)
        self.assertRedirects(response, reverse("accounts:login"))
        user = get_user_model().objects.get(username="hossein")
        self.assertTrue(Profile.objects.filter(user=user).exists())


class ProfileEditViewTests(TestCase):
    def setUp(self):
        self.user, self.password = create_user(username="profile_user")
        self.client.login(username=self.user.username, password=self.password)

    def test_profile_edit_get(self):
        response = self.client.get(reverse("accounts:profile_edit"))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_updates_information(self):
        payload = {
            "phone": "021-123456",
            "level": "B1",
            "bio": "Learning German enthusiast.",
            "website": "https://example.com",
            "newsletter_opt_in": "on",
        }
        response = self.client.post(reverse("accounts:profile_edit"), payload)
        self.assertRedirects(response, reverse("accounts:profile"))
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone, "021-123456")
        self.assertEqual(profile.level, "B1")
        self.assertTrue(profile.newsletter_opt_in)
        self.assertEqual(profile.website, "https://example.com")
