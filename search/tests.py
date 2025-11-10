from django.test import TestCase
from django.urls import reverse

from courses.models import VideoTag
from tests.factories import create_post, create_product, create_video


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video = create_video(title="Listening Practice", level="A2")
        cls.video.description = "تمرین شنیداری برای سطح A2"
        cls.video.save()
        cls.product = create_product(name="Listening Pack", price=150000)
        cls.product.description = "پکیج کامل تمرین‌های شنیداری"
        cls.product.save()
        cls.post = create_post(title="Listening Strategies")
        cls.post.content = "بهترین راهکارهای تقویت مهارت شنیداری."
        cls.post.save()
        tag = VideoTag.objects.create(name="Listening", color="#0d6efd")
        cls.video.tags.add(tag)

    def test_search_view_returns_results(self):
        response = self.client.get(reverse("search:search"), {"q": "Listening"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.context["total_results"], 0)
        self.assertContains(response, "Listening")

    def test_suggestion_view_returns_json(self):
        response = self.client.get(reverse("search:suggest"), {"q": "Listening"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("suggestions", data)
        self.assertTrue(any("Listening" in suggestion for suggestion in data["suggestions"]))
