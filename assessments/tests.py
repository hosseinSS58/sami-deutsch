import time

from django.test import TestCase
from django.urls import reverse

from assessments.models import Submission
from tests.factories import create_assessment_with_question, create_user


class AssessmentFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.assessment, cls.question, cls.correct_choice = create_assessment_with_question()

    def test_intro_redirects_when_single_assessment(self):
        response = self.client.get(reverse("assessments:intro"))
        self.assertRedirects(response, reverse("assessments:take"))

    def test_take_view_renders_question(self):
        session = self.client.session
        session["assessment_id"] = self.assessment.id
        session["adaptive"] = False
        session.save()
        response = self.client.get(reverse("assessments:take"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)

    def test_take_view_submission_creates_submission(self):
        # Prime session and fetch page to build form
        session = self.client.session
        session["assessment_id"] = self.assessment.id
        session["assessment_start"] = int(time.time()) - 30
        session["adaptive"] = False
        session.save()
        self.client.get(reverse("assessments:take"))
        payload = {
            "full_name": "Hossein",
            "email": "hossein@example.com",
            f"q_{self.question.id}": str(self.correct_choice.id),
        }
        response = self.client.post(reverse("assessments:take"), payload)
        self.assertRedirects(response, reverse("assessments:result"))
        self.assertTrue(Submission.objects.filter(assessment=self.assessment).exists())

    def test_result_view_shows_latest_submission(self):
        session = self.client.session
        session.save()
        submission = Submission.objects.create(
            assessment=self.assessment,
            user_identifier=session.session_key,
            full_name="Hossein",
            email="hossein@example.com",
            score=8,
            total_weight=10,
            ratio=0.8,
            duration_seconds=120,
            recommended_level="B2",
        )
        session["recommended_level"] = "B2"
        session.save()
        response = self.client.get(reverse("assessments:result"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "B2")

    def test_authenticated_user_skips_identity(self):
        user, password = create_user()
        self.client.login(username=user.username, password=password)
        session = self.client.session
        session["assessment_id"] = self.assessment.id
        session["assessment_start"] = int(time.time()) - 10
        session["adaptive"] = False
        session.save()
        response = self.client.get(reverse("assessments:take"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)
        # submit without providing name/email manually
        payload = {
            f"q_{self.question.id}": str(self.correct_choice.id),
        }
        post_resp = self.client.post(reverse("assessments:take"), payload)
        self.assertRedirects(post_resp, reverse("assessments:result"))

    def test_result_shows_hint_for_incorrect(self):
        # Prepare a submission with an incorrect answer and hint text
        self.question.hint_text = "Tip: review verb conjugation."
        self.question.save(update_fields=["hint_text"])
        session = self.client.session
        session["assessment_id"] = self.assessment.id
        session["assessment_start"] = int(time.time()) - 10
        session["adaptive"] = False
        session.save()
        self.client.get(reverse("assessments:take"))
        payload = {
            "full_name": "User",
            "email": "user@example.com",
            f"q_{self.question.id}": "-1",  # invalid to mark incorrect
        }
        self.client.post(reverse("assessments:take"), payload)
        resp = self.client.get(reverse("assessments:result"))
        self.assertContains(resp, "نکات آموزشی")
        self.assertContains(resp, "review verb conjugation")
