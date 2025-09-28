from django.db import models
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse, parse_qs


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("عنوان"), default="")
    description = models.TextField(blank=True, verbose_name=_("توضیحات"), default="")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, default="")
    level = models.CharField(
        max_length=2,
        choices=[
            ("A1", "A1"),
            ("A2", "A2"),
            ("B1", "B1"),
            ("B2", "B2"),
            ("C1", "C1"),
        ],
        verbose_name=_("سطح"),
    )
    topic = models.CharField(
        max_length=50,
        choices=[
            ("grammar", _("گرامر")),
            ("speaking", _("مکالمه")),
            ("vocab", _("واژگان")),
            ("listening", _("شنیداری")),
            ("reading", _("خواندن")),
            ("writing", _("نوشتن")),
            ("culture", _("فرهنگ")),
            ("pronunciation", _("تلفظ")),
        ],
        verbose_name=_("موضوع"),
    )
    cover = models.ImageField(upload_to="videos/covers/", blank=True, null=True, verbose_name=_("تصویر کاور"))
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name=_("مدت زمان (دقیقه)"))
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", _("مبتدی")),
            ("intermediate", _("متوسط")),
            ("advanced", _("پیشرفته")),
        ],
        default="beginner",
        verbose_name=_("سطح دشواری"),
    )
    is_featured = models.BooleanField(default=False, verbose_name=_("ویژه"))
    is_free = models.BooleanField(default=True, verbose_name=_("رایگان"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("ویدیو")
        verbose_name_plural = _("ویدیوها")
        ordering = ["-is_featured", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("videos:detail", kwargs={"slug": self.slug})

    @property
    def slug_current(self) -> str:
        return self.slug

    @property
    def total_duration_formatted(self):
        """Return formatted duration string"""
        if self.duration_minutes == 0:
            return "زمان نامشخص"
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours} ساعت و {minutes} دقیقه"
        return f"{minutes} دقیقه"


class VideoImage(models.Model):
    """تصاویر اضافی برای ویدیو"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="images", verbose_name=_("ویدیو"))
    image = models.ImageField(upload_to="videos/images/", verbose_name=_("تصویر"))
    caption = models.CharField(max_length=200, blank=True, verbose_name=_("توضیح تصویر"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("ترتیب"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("تصویر ویدیو")
        verbose_name_plural = _("تصاویر ویدیو")

    def __str__(self) -> str:
        return f"{self.video.title} - {self.caption or 'تصویر'}"


class YouTubeLink(models.Model):
    """لینک‌های یوتیوب"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="youtube_links", verbose_name=_("ویدیو"))
    title = models.CharField(max_length=200, verbose_name=_("عنوان"))
    youtube_url = models.URLField(verbose_name=_("لینک یوتیوب"))
    description = models.TextField(blank=True, verbose_name=_("توضیحات"))
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name=_("مدت زمان (دقیقه)"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("ترتیب"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("لینک یوتیوب")
        verbose_name_plural = _("لینک‌های یوتیوب")

    def __str__(self) -> str:
        return f"{self.video.title} - {self.title}"

    def _extract_youtube_id(self) -> str | None:
        if not self.youtube_url:
            return None
        try:
            parsed = urlparse(self.youtube_url)
            if parsed.netloc in {"youtu.be"}:
                return parsed.path.lstrip("/") or None
            if "youtube.com" in parsed.netloc:
                if parsed.path.startswith("/watch"):
                    q = parse_qs(parsed.query)
                    vid = q.get("v", [None])[0]
                    return vid
                if parsed.path.startswith("/embed/"):
                    return parsed.path.split("/embed/")[-1]
                if parsed.path.startswith("/shorts/"):
                    return parsed.path.split("/shorts/")[-1]
        except Exception:
            return None
        return None

    @property
    def youtube_id(self) -> str | None:
        return self._extract_youtube_id()

    @property
    def youtube_thumbnail_url(self) -> str | None:
        vid = self._extract_youtube_id()
        if not vid:
            return None
        return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

    @property
    def youtube_embed_url(self) -> str | None:
        vid = self._extract_youtube_id()
        if not vid:
            return None
        return f"https://www.youtube.com/embed/{vid}"


class VideoTag(models.Model):
    """تگ‌های ویدیو برای دسته‌بندی بهتر"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_("نام تگ"))
    color = models.CharField(max_length=7, default="#0d6efd", verbose_name=_("رنگ تگ"))
    videos = models.ManyToManyField(Video, related_name="tags", blank=True, verbose_name=_("ویدیوها"))

    class Meta:
        verbose_name = _("تگ ویدیو")
        verbose_name_plural = _("تگ‌های ویدیو")

    def __str__(self) -> str:
        return self.name


# Backward compatibility - keep Course as alias for Video
Course = Video
