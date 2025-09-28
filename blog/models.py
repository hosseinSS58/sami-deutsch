from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام"))
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name=_("اسلاگ"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    color = models.CharField(max_length=7, default="#007bff", verbose_name=_("رنگ"))
    
    class Meta:
        verbose_name = _("دسته‌بندی")
        verbose_name_plural = _("دسته‌بندی‌ها")
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name=_("عنوان"), default="")
    slug = models.SlugField(max_length=270, unique=True, allow_unicode=True, default="")
    content = models.TextField(verbose_name=_("محتوا"), default="")
    excerpt = models.TextField(max_length=500, blank=True, null=True, verbose_name=_("خلاصه"))
    cover = models.ImageField(upload_to="blog/covers/", blank=True, null=True, verbose_name=_("عکس کاور"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("دسته‌بندی"))
    youtube_video_id = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("شناسه ویدیو یوتیوب"))
    is_featured = models.BooleanField(default=False, verbose_name=_("ویژه"))
    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ انتشار"))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_("تعداد بازدید"))
    
    class Meta:
        verbose_name = _("مقاله")
        verbose_name_plural = _("مقالات")
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def slug_current(self) -> str:
        return self.slug
    
    @property
    def youtube_embed_url(self):
        """Return YouTube embed URL for the video"""
        if self.youtube_video_id:
            return f"https://www.youtube.com/embed/{self.youtube_video_id}"
        return None
    
    @property
    def youtube_watch_url(self):
        """Return YouTube watch URL for the video"""
        if self.youtube_video_id:
            return f"https://www.youtube.com/watch?v={self.youtube_video_id}"
        return None
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_excerpt_display(self):
        """Return excerpt or first 200 characters of content"""
        if self.excerpt:
            return self.excerpt
        content = self.content or ""
        return content[:200] + "..." if len(content) > 200 else content
