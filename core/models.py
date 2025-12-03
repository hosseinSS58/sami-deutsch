from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام"))
    email = models.EmailField(verbose_name=_("ایمیل"))
    message = models.TextField(verbose_name=_("پیام"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("پیام تماس")
        verbose_name_plural = _("پیام‌های تماس")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"


class AnonymousVisitor(models.Model):
    """
    بازدیدکنندگان ناشناس (کاربرانی که لاگ این نکرده‌اند)
    """
    session_key = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
        verbose_name=_("کلید نشست"),
        help_text=_("شناسه منحصر به فرد نشست Django")
    )
    first_seen = models.DateTimeField(auto_now_add=True, verbose_name=_("اولین بازدید"))
    last_seen = models.DateTimeField(auto_now=True, verbose_name=_("آخرین بازدید"))
    first_ip = models.CharField(max_length=45, blank=True, verbose_name=_("اولین آی‌پی"))
    last_ip = models.CharField(max_length=45, blank=True, verbose_name=_("آخرین آی‌پی"))
    first_country = models.CharField(max_length=2, blank=True, verbose_name=_("اولین کشور"))
    last_country = models.CharField(max_length=2, blank=True, verbose_name=_("آخرین کشور"))
    first_user_agent = models.TextField(blank=True, verbose_name=_("اولین مرورگر / دستگاه"))
    last_user_agent = models.TextField(blank=True, verbose_name=_("آخرین مرورگر / دستگاه"))
    
    class Meta:
        verbose_name = _("بازدیدکننده ناشناس")
        verbose_name_plural = _("بازدیدکنندگان ناشناس")
        ordering = ["-last_seen"]
        indexes = [
            models.Index(fields=["session_key"]),
            models.Index(fields=["last_seen"]),
        ]
    
    def __str__(self) -> str:
        return f"Anonymous Visitor - {self.session_key[:8]}... ({self.first_ip})"
    
    @property
    def total_visits(self):
        """تعداد کل بازدیدهای این بازدیدکننده ناشناس"""
        return self.site_visits.count()
    
    @property
    def total_youtube_clicks(self):
        """تعداد کل کلیک‌های یوتیوب این بازدیدکننده ناشناس"""
        return self.youtube_clicks.count()


class SiteVisit(models.Model):
    """
    آمار بازدید صفحات سایت
    """

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_visits",
        verbose_name=_("کاربر"),
    )
    anonymous_visitor = models.ForeignKey(
        "AnonymousVisitor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_visits",
        verbose_name=_("بازدیدکننده ناشناس"),
    )
    path = models.CharField(max_length=512, verbose_name=_("آدرس صفحه"))
    method = models.CharField(max_length=10, verbose_name=_("متد درخواست"))
    status_code = models.PositiveIntegerField(default=200, verbose_name=_("کد وضعیت"))
    ip_address = models.CharField(max_length=45, blank=True, verbose_name=_("آی‌پی"))
    country = models.CharField(max_length=2, blank=True, verbose_name=_("کشور"))
    device_type = models.CharField(max_length=20, blank=True, verbose_name=_("نوع دستگاه"))
    user_agent = models.TextField(blank=True, verbose_name=_("مرورگر / دستگاه"))
    referrer = models.TextField(blank=True, verbose_name=_("صفحه ارجاع‌دهنده"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("زمان بازدید"))

    class Meta:
        verbose_name = _("بازدید صفحه")
        verbose_name_plural = _("بازدیدهای سایت")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["path"]),
            models.Index(fields=["anonymous_visitor"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self) -> str:
        return f"{self.path} - {self.created_at:%Y-%m-%d %H:%M}"


class YouTubeClick(models.Model):
    """
    ثبت کلیک‌های کاربران روی لینک‌های یوتیوب
    """
    
    class ClickSource(models.TextChoices):
        VIDEO = "video", _("ویدیو")
        POST = "post", _("مقاله")
        OTHER = "other", _("سایر")
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="youtube_clicks",
        verbose_name=_("کاربر"),
    )
    anonymous_visitor = models.ForeignKey(
        "AnonymousVisitor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="youtube_clicks",
        verbose_name=_("بازدیدکننده ناشناس"),
    )
    youtube_url = models.URLField(verbose_name=_("لینک یوتیوب"))
    youtube_id = models.CharField(max_length=20, blank=True, verbose_name=_("شناسه ویدیو یوتیوب"))
    source_type = models.CharField(
        max_length=10,
        choices=ClickSource.choices,
        default=ClickSource.OTHER,
        verbose_name=_("نوع منبع"),
    )
    source_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("شناسه منبع"))
    source_title = models.CharField(max_length=255, blank=True, verbose_name=_("عنوان منبع"))
    ip_address = models.CharField(max_length=45, blank=True, verbose_name=_("آی‌پی"))
    country = models.CharField(max_length=2, blank=True, verbose_name=_("کشور"))
    user_agent = models.TextField(blank=True, verbose_name=_("مرورگر / دستگاه"))
    referrer = models.TextField(blank=True, verbose_name=_("صفحه ارجاع‌دهنده"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("زمان کلیک"))
    
    class Meta:
        verbose_name = _("کلیک یوتیوب")
        verbose_name_plural = _("کلیک‌های یوتیوب")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["youtube_id"]),
            models.Index(fields=["source_type", "source_id"]),
            models.Index(fields=["country"]),
        ]
    
    def __str__(self) -> str:
        return f"{self.youtube_id or 'Unknown'} - {self.created_at:%Y-%m-%d %H:%M}"

