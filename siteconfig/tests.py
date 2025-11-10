from django.test import RequestFactory, TestCase

from siteconfig.context_processors import site_settings
from siteconfig.models import NavLink, SiteSettings
from tests.factories import ensure_site_settings


class SiteSettingsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_load_returns_singleton_instance(self):
        settings_a = SiteSettings.load()
        settings_b = SiteSettings.load()
        self.assertEqual(settings_a.pk, 1)
        self.assertEqual(settings_a, settings_b)

    def test_context_processor_exposes_expected_keys(self):
        settings_obj = ensure_site_settings()
        NavLink.objects.create(title="Home", url="/", order=1, is_active=True)
        request = self.factory.get("/")
        context = site_settings(request)
        self.assertIn("site_settings", context)
        self.assertEqual(context["site_settings"], settings_obj)
        self.assertTrue(context["nav_links"].exists())
