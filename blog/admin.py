from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    list_editable = ("color",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "published_at", "views_count", "has_youtube_video")
    list_filter = ("is_featured", "category", "published_at")
    list_editable = ("is_featured", "category")
    search_fields = ("title", "content", "excerpt")
    readonly_fields = ("views_count", "published_at")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    prepopulated_fields = {"slug": ("title",)}
    
    fieldsets = (
        (_("اطلاعات اصلی"), {
            "fields": ("title", "slug", "content", "excerpt", "cover", "category", "is_featured")
        }),
        (_("محتوای یوتیوب"), {
            "fields": ("youtube_video_id",),
            "description": _("شناسه ویدیو یوتیوب را وارد کنید (مثال: dQw4w9WgXcQ)")
        }),
        (_("آمار"), {
            "fields": ("views_count", "published_at"),
            "classes": ("collapse",)
        }),
    )
    
    def has_youtube_video(self, obj):
        return bool(obj.youtube_video_id)
    has_youtube_video.boolean = True
    has_youtube_video.short_description = _("ویدیو یوتیوب")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


# Register your models here.
