from django.contrib import admin

from .models import ContactMessage, SiteVisit, YouTubeClick, AnonymousVisitor


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(AnonymousVisitor)
class AnonymousVisitorAdmin(admin.ModelAdmin):
    list_display = ("session_key", "first_ip", "last_ip", "first_country", "last_country", "first_seen", "last_seen", "total_visits_display", "total_youtube_clicks_display")
    list_filter = ("first_seen", "last_seen", "first_country", "last_country")
    search_fields = ("session_key", "first_ip", "last_ip", "first_country", "last_country", "first_user_agent", "last_user_agent")
    readonly_fields = (
        "session_key",
        "first_seen",
        "last_seen",
        "first_ip",
        "last_ip",
        "first_country",
        "last_country",
        "first_user_agent",
        "last_user_agent",
    )
    
    def total_visits_display(self, obj):
        return obj.total_visits
    total_visits_display.short_description = "تعداد بازدیدها"
    
    def total_youtube_clicks_display(self, obj):
        return obj.total_youtube_clicks
    total_youtube_clicks_display.short_description = "تعداد کلیک‌های یوتیوب"


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ("path", "created_at", "status_code", "user", "anonymous_visitor", "ip_address", "country")
    list_filter = ("status_code", "created_at", "country")
    search_fields = ("path", "ip_address", "user_agent", "referrer", "country")
    readonly_fields = (
        "user",
        "anonymous_visitor",
        "path",
        "method",
        "status_code",
        "ip_address",
        "country",
        "user_agent",
        "referrer",
        "created_at",
    )


@admin.register(YouTubeClick)
class YouTubeClickAdmin(admin.ModelAdmin):
    list_display = ("youtube_id", "source_type", "source_title", "user", "anonymous_visitor", "ip_address", "country", "created_at")
    list_filter = ("source_type", "created_at", "country")
    search_fields = ("youtube_url", "youtube_id", "source_title", "ip_address", "country")
    readonly_fields = (
        "user",
        "anonymous_visitor",
        "youtube_url",
        "youtube_id",
        "source_type",
        "source_id",
        "source_title",
        "ip_address",
        "country",
        "user_agent",
        "referrer",
        "created_at",
    )

