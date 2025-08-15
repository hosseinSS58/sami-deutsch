from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import Video, VideoImage, YouTubeLink, VideoTag


class VideoImageInline(admin.TabularInline):
    model = VideoImage
    extra = 1
    fields = ("image", "caption", "order", "is_active")


class YouTubeLinkInline(admin.TabularInline):
    model = YouTubeLink
    extra = 1
    fields = ("title", "youtube_url", "description", "duration_minutes", "order", "is_active")


@admin.register(Video)
class VideoAdmin(TranslatableAdmin):
    list_display = ("__str__", "level", "topic", "difficulty", "duration_minutes", "is_featured", "is_free", "created_at")
    list_editable = ("is_featured", "is_free", "difficulty")
    search_fields = ("translations__title", "translations__description")
    list_filter = ("level", "topic", "difficulty", "is_featured", "is_free", "created_at")
    
    fieldsets = (
        (_("اطلاعات اصلی"), {
            "fields": (
                "level", "topic", "difficulty", "cover", "duration_minutes",
                "is_featured", "is_free"
            )
        }),
        (_("ترجمه"), {
            "fields": ("title", "slug", "description")
        }),
    )
    
    inlines = [VideoImageInline, YouTubeLinkInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags", "images", "youtube_links")


@admin.register(VideoTag)
class VideoTagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "videos_count")
    list_editable = ("color",)
    search_fields = ("name",)
    
    def videos_count(self, obj):
        return obj.videos.count()
    videos_count.short_description = _("تعداد ویدیوها")


# Backward compatibility
CourseAdmin = VideoAdmin
