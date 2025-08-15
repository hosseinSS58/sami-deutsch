from django.contrib import admin
from .models import SiteSettings, NavLink, FooterLink, HomeFeature, HomeSlider, Slide, Menu, MenuItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand & Basic", {"fields": ("brand_name", "logo", "primary_color", "meta_description", "footer_text", "show_default_nav_links")}),
        ("Hero Section", {"fields": ("hero_title", "hero_subtitle", "hero_video_url", "show_newsletter")}),
        ("Header & Navigation Colors", {"fields": ("navbar_bg_color", "navbar_text_color", "navbar_hover_color")}),
        ("Button Colors", {"fields": ("button_primary_bg", "button_primary_text", "button_secondary_bg", "button_secondary_text", "button_outline_color")}),
        ("Card & Content Colors", {"fields": ("card_bg_color", "card_border_color", "card_shadow_color")}),
        ("Text Colors", {"fields": ("text_primary_color", "text_secondary_color", "text_muted_color")}),
        ("Background Colors", {"fields": ("body_bg_color", "section_bg_color", "footer_bg_color", "footer_text_color")}),
        ("Link Colors", {"fields": ("link_color", "link_hover_color")}),
        ("Status Colors", {"fields": ("success_color", "error_color", "warning_color", "info_color")}),
        ("Typography", {"fields": ("heading_font_family", "body_font_family", "base_font_size")}),
        ("Layout & Spacing", {"fields": ("container_max_width", "section_padding", "card_border_radius")}),
        ("Custom CSS", {"fields": ("custom_css",), "classes": ("collapse",)}),
    )


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(HomeFeature)
class HomeFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    fieldsets = (("Behavior", {"fields": ("autoplay", "interval_ms", "show_arrows", "show_indicators", "pause_on_hover", "aspect_ratio")}),)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("title", "subtitle", "image", "order", "is_active")}),
        ("Overlay Position", {"fields": ("overlay_h_align", "overlay_v_align", "text_align")}),
        ("CTA", {"fields": ("cta_text", "cta_url")}),
        ("Colors", {"fields": ("text_color", "button_bg_color", "button_text_color", "caption_bg_color", "caption_bg_opacity")}),
    )


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MenuItemInline]

from django.contrib import admin

# Register your models here.
