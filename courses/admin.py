from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import Video, VideoImage, YouTubeLink, VideoTag
from .youtube_utils import extract_youtube_metadata, create_video_from_youtube


class VideoImageInline(admin.TabularInline):
    model = VideoImage
    extra = 1
    fields = ("image", "caption", "order", "is_active")


class YouTubeLinkInline(admin.TabularInline):
    model = YouTubeLink
    extra = 1
    fields = ("title", "youtube_url", "description", "duration_minutes", "order", "is_active")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "topic", "difficulty", "duration_minutes", "is_featured", "is_free", "created_at")
    list_editable = ("is_featured", "is_free", "difficulty")
    search_fields = ("title", "description")
    list_filter = ("level", "topic", "difficulty", "is_featured", "is_free", "created_at")
    actions = ["import_from_youtube"]
    
    fieldsets = (
        (_("اطلاعات اصلی"), {
            "fields": (
                "title", "slug", "description", "level", "topic", "difficulty", 
                "cover", "duration_minutes", "is_featured", "is_free"
            )
        }),
    )
    
    inlines = [VideoImageInline, YouTubeLinkInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags", "images", "youtube_links")
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_youtube_url'] = reverse('admin:courses_video_import_youtube')
        extra_context['has_import_youtube'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    @admin.action(description=_("وارد کردن ویدیو از لینک یوتیوب"))
    def import_from_youtube(self, request, queryset):
        """این اکشن برای bulk import نیست - از صفحه جداگانه استفاده کنید"""
        self.message_user(
            request,
            _("لطفاً از دکمه 'وارد کردن از یوتیوب' در بالای صفحه استفاده کنید."),
            messages.WARNING
        )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-youtube/",
                self.admin_site.admin_view(self.import_youtube_view),
                name="courses_video_import_youtube",
            ),
            path(
                "import-youtube/extract/",
                self.admin_site.admin_view(self.extract_youtube_metadata_view),
                name="courses_video_extract_metadata",
            ),
        ]
        return custom_urls + urls
    
    @method_decorator(require_http_methods(["GET", "POST"]))
    def import_youtube_view(self, request):
        """صفحه وارد کردن ویدیو از یوتیوب"""
        if request.method == "POST":
            youtube_url = request.POST.get("youtube_url", "").strip()
            if not youtube_url:
                messages.error(request, _("لطفاً لینک یوتیوب را وارد کنید."))
                return render(request, "admin/courses/video/import_youtube.html", {
                    **self.admin_site.each_context(request),
                    "title": _("وارد کردن ویدیو از یوتیوب"),
                })
            
            # استخراج اطلاعات اضافی از فرم
            level = request.POST.get("level", "A1")
            topic = request.POST.get("topic", "grammar")
            difficulty = request.POST.get("difficulty", "beginner")
            is_free = request.POST.get("is_free") == "on"
            is_featured = request.POST.get("is_featured") == "on"
            
            # ایجاد ویدیو
            video, youtube_link, message = create_video_from_youtube(
                youtube_url,
                level=level,
                topic=topic,
                difficulty=difficulty,
                is_free=is_free,
                is_featured=is_featured,
            )
            
            if video:
                messages.success(request, message)
                return redirect(f"/admin/courses/video/{video.id}/change/")
            else:
                messages.error(request, message)
        
        return render(request, "admin/courses/video/import_youtube.html", {
            **self.admin_site.each_context(request),
            "title": _("وارد کردن ویدیو از یوتیوب"),
            "levels": Video._meta.get_field("level").choices,
            "topics": Video._meta.get_field("topic").choices,
            "difficulties": Video._meta.get_field("difficulty").choices,
        })
    
    @method_decorator(require_http_methods(["POST"]))
    def extract_youtube_metadata_view(self, request):
        """API endpoint برای استخراج اطلاعات یوتیوب (AJAX)"""
        youtube_url = request.POST.get("youtube_url", "").strip()
        if not youtube_url:
            return JsonResponse({"success": False, "error": _("لینک یوتیوب را وارد کنید")})
        
        metadata = extract_youtube_metadata(youtube_url)
        return JsonResponse(metadata)


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
