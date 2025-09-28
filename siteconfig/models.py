from django.db import models
from django.utils.translation import gettext_lazy as _


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    brand_name = models.CharField(max_length=50, default="Sami")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#0d6efd")
    meta_description = models.CharField(max_length=200, blank=True, default="")
    footer_text = models.TextField(blank=True, default="")
    show_default_nav_links = models.BooleanField(default=True)

    # Home hero
    hero_title = models.CharField(max_length=120, blank=True, default="آموزش زبان آلمانی", verbose_name=_("عنوان اصلی هیرو"))
    hero_subtitle = models.CharField(max_length=200, blank=True, default="از پایه تا پیشرفته", verbose_name=_("زیرعنوان هیرو"))
    hero_description = models.TextField(blank=True, default="با بهترین روش‌های آموزشی، زبان آلمانی را به صورت خودخوان و کاربردی یاد بگیرید. از سطح A1 تا C1، با ویدیوهای آموزشی، مقالات تخصصی و آزمون‌های استاندارد.", verbose_name=_("توضیحات هیرو"))
    hero_primary_button_text = models.CharField(max_length=50, blank=True, default="شروع یادگیری", verbose_name=_("متن دکمه اصلی"))
    hero_primary_button_url = models.CharField(max_length=200, blank=True, default="/videos/", verbose_name=_("لینک دکمه اصلی"))
    hero_secondary_button_text = models.CharField(max_length=50, blank=True, default="تعیین سطح", verbose_name=_("متن دکمه ثانویه"))
    hero_secondary_button_url = models.CharField(max_length=200, blank=True, default="/assessments/", verbose_name=_("لینک دکمه ثانویه"))
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True, verbose_name=_("تصویر هیرو"))
    hero_icon = models.CharField(max_length=50, blank=True, default="fas fa-graduation-cap", verbose_name=_("آیکون هیرو"))
    hero_icon_size = models.CharField(max_length=20, blank=True, default="fa-8x", verbose_name=_("اندازه آیکون"))
    hero_icon_color = models.CharField(max_length=7, blank=True, default="#0d6efd", verbose_name=_("رنگ آیکون"))
    hero_bg_color = models.CharField(max_length=7, blank=True, default="#f8f9fa", verbose_name=_("رنگ پس‌زمینه هیرو"))
    hero_text_color = models.CharField(max_length=7, blank=True, default="#0f172a", verbose_name=_("رنگ متن هیرو"))
    hero_subtitle_color = models.CharField(max_length=7, blank=True, default="#6c757d", verbose_name=_("رنگ زیرعنوان"))
    hero_description_color = models.CharField(max_length=7, blank=True, default="#6c757d", verbose_name=_("رنگ توضیحات"))
    show_hero_floating_elements = models.BooleanField(default=True, verbose_name=_("نمایش عناصر شناور"))
    show_hero_stats = models.BooleanField(default=True, verbose_name=_("نمایش آمار"))
    show_hero_newsletter = models.BooleanField(default=True, verbose_name=_("نمایش خبرنامه"))
    hero_video_url = models.URLField(blank=True, default="https://www.youtube.com/embed/hHW1oY26kxQ", verbose_name=_("لینک ویدیو هیرو"))
    show_hero_video = models.BooleanField(default=False, verbose_name=_("نمایش ویدیو هیرو"))
    
    # Hero Stats
    hero_stats_videos_title = models.CharField(max_length=50, blank=True, default="ویدیوی آموزشی", verbose_name=_("عنوان آمار ویدیوها"))
    hero_stats_videos_count = models.PositiveIntegerField(default=100, verbose_name=_("تعداد ویدیوها"))
    hero_stats_videos_icon = models.CharField(max_length=50, blank=True, default="fas fa-video", verbose_name=_("آیکون ویدیوها"))
    hero_stats_videos_color = models.CharField(max_length=7, blank=True, default="#0d6efd", verbose_name=_("رنگ آمار ویدیوها"))
    
    hero_stats_posts_title = models.CharField(max_length=50, blank=True, default="مقاله تخصصی", verbose_name=_("عنوان آمار مقالات"))
    hero_stats_posts_count = models.PositiveIntegerField(default=50, verbose_name=_("تعداد مقالات"))
    hero_stats_posts_icon = models.CharField(max_length=50, blank=True, default="fas fa-newspaper", verbose_name=_("آیکون مقالات"))
    hero_stats_posts_color = models.CharField(max_length=7, blank=True, default="#198754", verbose_name=_("رنگ آمار مقالات"))
    
    hero_stats_products_title = models.CharField(max_length=50, blank=True, default="پکیج آموزشی", verbose_name=_("عنوان آمار محصولات"))
    hero_stats_products_count = models.PositiveIntegerField(default=25, verbose_name=_("تعداد محصولات"))
    hero_stats_products_icon = models.CharField(max_length=50, blank=True, default="fas fa-shopping-bag", verbose_name=_("آیکون محصولات"))
    hero_stats_products_color = models.CharField(max_length=7, blank=True, default="#ffc107", verbose_name=_("رنگ آمار محصولات"))
    
    hero_stats_students_title = models.CharField(max_length=50, blank=True, default="دانشجو", verbose_name=_("عنوان آمار دانشجویان"))
    hero_stats_students_count = models.PositiveIntegerField(default=1000, verbose_name=_("تعداد دانشجویان"))
    hero_stats_students_icon = models.CharField(max_length=50, blank=True, default="fas fa-users", verbose_name=_("آیکون دانشجویان"))
    hero_stats_students_color = models.CharField(max_length=7, blank=True, default="#0dcaf0", verbose_name=_("رنگ آمار دانشجویان"))
    
    # Hero Floating Elements
    hero_floating_element_1_title = models.CharField(max_length=50, blank=True, default="ویدیوهای آموزشی", verbose_name=_("عنوان عنصر شناور 1"))
    hero_floating_element_1_icon = models.CharField(max_length=50, blank=True, default="fas fa-video", verbose_name=_("آیکون عنصر شناور 1"))
    hero_floating_element_1_color = models.CharField(max_length=7, blank=True, default="#198754", verbose_name=_("رنگ عنصر شناور 1"))
    
    hero_floating_element_2_title = models.CharField(max_length=50, blank=True, default="مقالات تخصصی", verbose_name=_("عنوان عنصر شناور 2"))
    hero_floating_element_2_icon = models.CharField(max_length=50, blank=True, default="fas fa-book", verbose_name=_("آیکون عنصر شناور 2"))
    hero_floating_element_2_color = models.CharField(max_length=7, blank=True, default="#0dcaf0", verbose_name=_("رنگ عنصر شناور 2"))
    
    hero_floating_element_3_title = models.CharField(max_length=50, blank=True, default="آزمون‌های استاندارد", verbose_name=_("عنوان عنصر شناور 3"))
    hero_floating_element_3_icon = models.CharField(max_length=50, blank=True, default="fas fa-trophy", verbose_name=_("آیکون عنصر شناور 3"))
    hero_floating_element_3_color = models.CharField(max_length=7, blank=True, default="#ffc107", verbose_name=_("رنگ عنصر شناور 3"))
    show_newsletter = models.BooleanField(default=True)

    # Color Scheme - Header & Navigation
    navbar_bg_color = models.CharField(max_length=7, default="#0d6efd", verbose_name=_("رنگ پس‌زمینه منو"))
    navbar_text_color = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ متن منو"))
    navbar_hover_color = models.CharField(max_length=7, default="#0b5ed7", verbose_name=_("رنگ هاور منو"))
    
    # Color Scheme - Buttons
    button_primary_bg = models.CharField(max_length=7, default="#0d6efd", verbose_name=_("رنگ پس‌زمینه دکمه اصلی"))
    button_primary_text = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ متن دکمه اصلی"))
    button_secondary_bg = models.CharField(max_length=7, default="#6c757d", verbose_name=_("رنگ پس‌زمینه دکمه ثانویه"))
    button_secondary_text = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ متن دکمه ثانویه"))
    button_outline_color = models.CharField(max_length=7, default="#0d6efd", verbose_name=_("رنگ حاشیه دکمه outline"))
    
    # Color Scheme - Cards & Content
    card_bg_color = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ پس‌زمینه کارت‌ها"))
    card_border_color = models.CharField(max_length=7, default="#dee2e6", verbose_name=_("رنگ حاشیه کارت‌ها"))
    card_shadow_color = models.CharField(max_length=7, default="rgba(0,0,0,0.1)", verbose_name=_("رنگ سایه کارت‌ها"))
    
    # Color Scheme - Text
    text_primary_color = models.CharField(max_length=7, default="#0f172a", verbose_name=_("رنگ متن اصلی"))
    text_secondary_color = models.CharField(max_length=7, default="#6c757d", verbose_name=_("رنگ متن ثانویه"))
    text_muted_color = models.CharField(max_length=7, default="#adb5bd", verbose_name=_("رنگ متن کمرنگ"))
    
    # Color Scheme - Backgrounds
    body_bg_color = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ پس‌زمینه صفحه"))
    section_bg_color = models.CharField(max_length=7, default="#f8f9fa", verbose_name=_("رنگ پس‌زمینه بخش‌ها"))
    footer_bg_color = models.CharField(max_length=7, default="#212529", verbose_name=_("رنگ پس‌زمینه فوتر"))
    footer_text_color = models.CharField(max_length=7, default="#ffffff", verbose_name=_("رنگ متن فوتر"))
    
    # Color Scheme - Links
    link_color = models.CharField(max_length=7, default="#0d6efd", verbose_name=_("رنگ لینک‌ها"))
    link_hover_color = models.CharField(max_length=7, default="#0a58ca", verbose_name=_("رنگ هاور لینک‌ها"))
    
    # Color Scheme - Success/Error/Warning
    success_color = models.CharField(max_length=7, default="#198754", verbose_name=_("رنگ موفقیت"))
    error_color = models.CharField(max_length=7, default="#dc3545", verbose_name=_("رنگ خطا"))
    warning_color = models.CharField(max_length=7, default="#ffc107", verbose_name=_("رنگ هشدار"))
    info_color = models.CharField(max_length=7, default="#0dcaf0", verbose_name=_("رنگ اطلاعات"))
    
    # Typography
    heading_font_family = models.CharField(max_length=100, default="Vazirmatn", verbose_name=_("فونت عناوین"))
    body_font_family = models.CharField(max_length=100, default="Vazirmatn", verbose_name=_("فونت متن"))
    base_font_size = models.CharField(max_length=10, default="16px", verbose_name=_("اندازه فونت پایه"))
    
    # Spacing & Layout
    container_max_width = models.CharField(max_length=20, default="1200px", verbose_name=_("حداکثر عرض کانتینر"))
    section_padding = models.CharField(max_length=20, default="4rem", verbose_name=_("فاصله بخش‌ها"))
    card_border_radius = models.CharField(max_length=20, default="0.375rem", verbose_name=_("گردی گوشه کارت‌ها"))
    
    # Custom CSS
    custom_css = models.TextField(blank=True, verbose_name=_("CSS سفارشی"), help_text=_("کدهای CSS اضافی برای شخصی‌سازی بیشتر"))

    def __str__(self) -> str:
        return "Site settings"


class NavLink(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("لینک ناوبری")
        verbose_name_plural = _("لینک‌های ناوبری")

    def __str__(self) -> str:
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("لینک فوتر")
        verbose_name_plural = _("لینک‌های فوتر")

    def __str__(self) -> str:
        return self.title


class HomeFeature(models.Model):
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=120, blank=True, default="")
    icon = models.CharField(max_length=50, blank=True, default="fa-solid fa-star")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("ویژگی صفحه اصلی")
        verbose_name_plural = _("ویژگی‌های صفحه اصلی")

    def __str__(self) -> str:
        return self.title


class HomeSlider(SingletonModel):
    autoplay = models.BooleanField(default=True)
    interval_ms = models.PositiveIntegerField(default=5000)
    show_arrows = models.BooleanField(default=True)
    show_indicators = models.BooleanField(default=True)
    pause_on_hover = models.BooleanField(default=True)
    aspect_ratio = models.CharField(max_length=10, default="21x9", help_text="مثل 16x9 یا 21x9")

    def __str__(self) -> str:
        return "Home slider"


class Slide(models.Model):
    ALIGN_CHOICES = [("start", "Start"), ("center", "Center"), ("end", "End")]
    VALIGN_CHOICES = [("top", "Top"), ("center", "Center"), ("bottom", "Bottom")]
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True, default="")
    image = models.ImageField(upload_to="slides/")
    cta_text = models.CharField(max_length=50, blank=True, default="")
    cta_url = models.CharField(max_length=200, blank=True, default="")
    text_align = models.CharField(max_length=10, choices=ALIGN_CHOICES, default="start")
    overlay_h_align = models.CharField(max_length=10, choices=ALIGN_CHOICES, default="center")
    overlay_v_align = models.CharField(max_length=10, choices=VALIGN_CHOICES, default="bottom")
    text_color = models.CharField(max_length=7, default="#ffffff")
    button_bg_color = models.CharField(max_length=7, default="#0d6efd")
    button_text_color = models.CharField(max_length=7, default="#ffffff")
    caption_bg_color = models.CharField(max_length=7, default="#000000")
    caption_bg_opacity = models.PositiveSmallIntegerField(default=40, help_text="0-100 درصد")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("اسلاید")
        verbose_name_plural = _("اسلایدها")

    def __str__(self) -> str:
        return self.title


class Menu(models.Model):
    class Location(models.TextChoices):
        HEADER = "header", _("هدر")
        FOOTER = "footer", _("فوتر")

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=10, choices=Location.choices, default=Location.HEADER)

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    title = models.CharField(max_length=80)
    url = models.CharField(max_length=300)
    icon_class = models.CharField(max_length=50, blank=True, default="")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("آیتم منو")
        verbose_name_plural = _("آیتم‌های منو")

    def __str__(self) -> str:
        return self.title

from django.db import models

# Create your models here.
