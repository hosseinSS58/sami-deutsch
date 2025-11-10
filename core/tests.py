from django.test import TestCase
from django.urls import reverse

from core.models import ContactMessage
from tests.factories import create_post, create_product, create_video


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video = create_video(title="Grammar Basics")
        cls.product = create_product(name="Grammar Pack")
        cls.post = create_post(title="Grammar Tips")

    def test_home_page_renders_with_latest_content(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grammar Basics")
        self.assertContains(response, "Grammar Pack")
        self.assertContains(response, "Grammar Tips")


class ContactViewTests(TestCase):
    def test_contact_get(self):
        response = self.client.get(reverse("core:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/contact.html")

    def test_contact_form_submission_creates_message(self):
        payload = {
            "name": "Hossein",
            "email": "hossein@example.com",
            "message": "Please contact me.",
        }
        response = self.client.post(reverse("core:contact"), payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.name, "Hossein")
        self.assertEqual(message.email, "hossein@example.com")
