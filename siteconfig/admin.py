from django.contrib import admin
from .models import (
    SiteSettings,
    NavLink,
    FooterLink,
    HomeFeature,
    HomeSlider,
    Slide,
    Menu,
    MenuItem,
    HomePageSection,
    SocialLink,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand & Basic", {"fields": ("brand_name", "logo", "primary_color", "meta_description", "footer_text", "show_default_nav_links")}),
        ("Hero Section - Main Content", {
            "fields": (
                "hero_title", 
                "hero_subtitle", 
                "hero_description",
                "hero_primary_button_text",
                "hero_primary_button_url",
                "hero_secondary_button_text",
                "hero_secondary_button_url",
                "hero_image",
                "hero_icon",
                "hero_icon_size",
                "hero_icon_color"
            )
        }),
        ("Hero Section - Colors", {
            "fields": (
                "hero_bg_color",
                "hero_text_color",
                "hero_subtitle_color",
                "hero_description_color"
            )
        }),
        ("Hero Section - Stats", {
            "fields": (
                "show_hero_stats",
                "hero_stats_videos_title",
                "hero_stats_videos_count",
                "hero_stats_videos_icon",
                "hero_stats_videos_color",
                "hero_stats_posts_title",
                "hero_stats_posts_count",
                "hero_stats_posts_icon",
                "hero_stats_posts_color",
                "hero_stats_products_title",
                "hero_stats_products_count",
                "hero_stats_products_icon",
                "hero_stats_products_color",
                "hero_stats_students_title",
                "hero_stats_students_count",
                "hero_stats_students_icon",
                "hero_stats_students_color"
            )
        }),
        ("Hero Section - Floating Elements", {
            "fields": (
                "show_hero_floating_elements",
                "hero_floating_element_1_title",
                "hero_floating_element_1_icon",
                "hero_floating_element_1_color",
                "hero_floating_element_2_title",
                "hero_floating_element_2_icon",
                "hero_floating_element_2_color",
                "hero_floating_element_3_title",
                "hero_floating_element_3_icon",
                "hero_floating_element_3_color"
            )
        }),
        ("Hero Section - Video & Newsletter", {
            "fields": (
                "show_hero_video",
                "hero_video_url",
                "show_hero_newsletter",
                "show_newsletter"
            )
        }),
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
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()


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
    fieldsets = (
        ("موقعیت", {
            "fields": ("position", "custom_order"),
        }),
        ("تنظیمات نمایش", {
            "fields": ("use_custom_size", "height_desktop", "height_mobile", "max_width", "aspect_ratio", "show_arrows", "show_indicators"),
        }),
        ("تنظیمات Autoplay", {
            "fields": ("autoplay", "interval_ms", "pause_on_hover"),
        }),
    )


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


@admin.register(HomePageSection)
class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "section_type", "order", "item_count", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("section_type", "is_active", "video_filter_featured", "video_filter_is_free", "product_filter_featured", "post_filter_featured")
    search_fields = ("title", "subtitle")
    
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": (
                "section_type",
                "title",
                "subtitle",
                "section_icon",
                "order",
                "is_active",
            )
        }),
        ("تنظیمات نمایش", {
            "fields": (
                "item_count",
                "use_manual_items",
                "manual_videos",
            )
        }),
        ("فیلترهای ویدیو - ویژگی‌ها", {
            "fields": (
                "video_filter_featured",
                "video_filter_is_free",
                "video_filter_has_youtube",
            ),
            "classes": ("collapse",),
        }),
        ("فیلترهای ویدیو - سطح و موضوع", {
            "fields": (
                "video_filter_level",
                "video_filter_topic",
                "video_filter_difficulty",
            ),
            "classes": ("collapse",),
        }),
        ("فیلترهای ویدیو - مدت زمان", {
            "fields": (
                "video_filter_duration_min",
                "video_filter_duration_max",
            ),
            "classes": ("collapse",),
        }),
        ("فیلترهای ویدیو - مرتب‌سازی", {
            "fields": (
                "video_order_by",
            ),
            "classes": ("collapse",),
        }),
        ("فیلترهای محصول", {
            "fields": (
                "product_filter_featured",
                "product_filter_active",
            ),
            "classes": ("collapse",),
        }),
        ("فیلترهای مقاله", {
            "fields": (
                "post_filter_featured",
            ),
            "classes": ("collapse",),
        }),
        ("دکمه 'همه'", {
            "fields": (
                "show_view_all_button",
                "view_all_button_text",
                "view_all_button_url",
                "view_all_button_icon",
            )
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        """نمایش فیلترها بر اساس نوع بخش"""
        fieldsets = list(super().get_fieldsets(request, obj))
        
        # اگر در حال ایجاد بخش جدید هستیم، همه فیلترها را نشان بده
        # اگر در حال ویرایش هستیم، فقط فیلترهای مربوط به نوع بخش را نشان بده
        if obj and obj.section_type:
            if obj.section_type == "videos":
                # حذف فیلترهای محصول و پست
                fieldsets = [fs for fs in fieldsets if "فیلترهای محصول" not in fs[0] and "فیلترهای مقاله" not in fs[0]]
            elif obj.section_type == "products":
                # حذف فیلترهای ویدیو و پست
                fieldsets = [fs for fs in fieldsets if "فیلترهای ویدیو" not in fs[0] and "فیلترهای مقاله" not in fs[0]]
            elif obj.section_type == "posts":
                # حذف فیلترهای ویدیو و محصول
                fieldsets = [fs for fs in fieldsets if "فیلترهای ویدیو" not in fs[0] and "فیلترهای محصول" not in fs[0]]
        
        return fieldsets


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("location", "is_active")
    search_fields = ("title", "url", "icon_class")
