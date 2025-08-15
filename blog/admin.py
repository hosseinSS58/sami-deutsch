from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    list_editable = ("color",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ("title", "category", "is_featured", "published_at", "views_count", "has_youtube_video")
    list_filter = ("is_featured", "category", "published_at")
    list_editable = ("is_featured", "category")
    search_fields = ("translations__title", "translations__content", "translations__excerpt")
    readonly_fields = ("views_count", "published_at")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    
    # فیلدهای ترجمه شده
    fieldsets = (
        (_("ترجمه فارسی"), {
            "fields": ("title", "slug", "content", "excerpt"),
        }),
        (_("اطلاعات اصلی"), {
            "fields": ("cover", "category", "is_featured")
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
    
    # فیلدهای ترجمه شده برای زبان‌های دیگر
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.fieldsets
        
        # اگر زبان فارسی انتخاب شده، فیلدهای ترجمه فارسی را نشان بده
        if request.GET.get('language') == 'fa' or not request.GET.get('language'):
            return self.fieldsets
        
        # برای زبان‌های دیگر، فقط فیلدهای ترجمه شده را نشان بده
        return (
            (_("ترجمه"), {
                "fields": ("title", "slug", "content", "excerpt"),
            }),
        )
    
    def has_youtube_video(self, obj):
        return bool(obj.youtube_video_id)
    has_youtube_video.boolean = True
    has_youtube_video.short_description = _("ویدیو یوتیوب")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


# Register your models here.
