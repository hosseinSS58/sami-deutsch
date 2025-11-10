from django.test import TestCase
from django.urls import reverse

from tests.factories import create_video


class VideoViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video_a1 = create_video(title="A1 Basics", level="A1")
        cls.video_b2 = create_video(title="B2 Mastery", level="B2")

    def test_video_list_renders_all_videos(self):
        response = self.client.get(reverse("videos:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1 Basics")
        self.assertContains(response, "B2 Mastery")

    def test_video_list_can_filter_by_level(self):
        response = self.client.get(reverse("videos:list"), {"level": "B2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "B2 Mastery")
        self.assertNotContains(response, "A1 Basics")

    def test_video_detail_renders(self):
        response = self.client.get(self.video_a1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.video_a1.title)

    def test_total_duration_formatted(self):
        self.assertEqual(self.video_a1.total_duration_formatted, "15 دقیقه")
