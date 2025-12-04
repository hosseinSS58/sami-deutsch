from django.db import DatabaseError
from .models import SiteSettings, NavLink, FooterLink, HomeFeature, HomeSlider, Slide, Menu, SocialLink


def site_settings(request):
    settings_obj = SiteSettings.load()
    try:
        slider = HomeSlider.load()
        slides_qs = Slide.objects.filter(is_active=True).order_by("order")
    except DatabaseError:
        slider = None
        slides_qs = []
    return {
        "site_settings": settings_obj,
        "nav_links": NavLink.objects.filter(is_active=True).order_by("order"),
        "header_menu": Menu.objects.filter(location=Menu.Location.HEADER).prefetch_related("items__children").first(),
        "footer_links": FooterLink.objects.filter(is_active=True).order_by("order"),
        "home_features": HomeFeature.objects.filter(is_active=True).order_by("order"),
        "home_slider": slider,
        "slides": slides_qs,
        "header_social_links": SocialLink.objects.filter(
            location=SocialLink.Location.HEADER,
            is_active=True,
        ).order_by("order", "id"),
        "footer_social_links": SocialLink.objects.filter(
            location=SocialLink.Location.FOOTER,
            is_active=True,
        ).order_by("order", "id"),
    }


