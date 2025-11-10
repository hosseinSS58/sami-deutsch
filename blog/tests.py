from django.test import TestCase
from django.urls import reverse

from tests.factories import create_category, create_post


class BlogViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = create_category("Listening")
        cls.post_listening = create_post(title="Improve Listening", category=cls.category)
        cls.post_grammar = create_post(title="Grammar Guide")

    def test_post_list_view_shows_posts(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Improve Listening")
        self.assertContains(response, "Grammar Guide")

    def test_post_list_view_supports_search(self):
        response = self.client.get(reverse("blog:list"), {"q": "Listening"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Improve Listening")
        self.assertNotContains(response, "Grammar Guide")

    def test_post_detail_increments_views(self):
        views_before = self.post_listening.views_count
        response = self.client.get(self.post_listening.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.post_listening.refresh_from_db()
        self.assertEqual(self.post_listening.views_count, views_before + 1)
