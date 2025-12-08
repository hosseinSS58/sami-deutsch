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

    @property
    def safe_css(self):
        """
        Return sanitized CSS to prevent XSS attacks
        Removes dangerous CSS patterns that could execute JavaScript
        """
        if not self.custom_css:
            return ''
        
        css = self.custom_css
        
        # Remove dangerous CSS patterns that could execute JavaScript
        import re
        
        # Block javascript: URLs
        css = re.sub(r'javascript\s*:', '', css, flags=re.IGNORECASE)
        
        # Block expression() (IE-specific but dangerous)
        css = re.sub(r'expression\s*\([^)]*\)', '', css, flags=re.IGNORECASE)
        
        # Block -moz-binding (Firefox-specific, can execute code)
        css = re.sub(r'-moz-binding\s*:[^;]*;?', '', css, flags=re.IGNORECASE)
        
        # Block @import with javascript
        css = re.sub(r'@import\s+.*javascript.*', '', css, flags=re.IGNORECASE)
        
        # Block data: URLs in url() that contain javascript
        css = re.sub(r'url\s*\(\s*["\']?data:.*javascript.*["\']?\s*\)', '', css, flags=re.IGNORECASE)
        
        return css.strip()

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
    class Position(models.TextChoices):
        TOP = "top", _("بالای صفحه (قبل از Hero)")
        AFTER_HERO = "after_hero", _("بعد از Hero Section")
        AFTER_STATS = "after_stats", _("بعد از Stats Section")
        CUSTOM = "custom", _("موقعیت سفارشی (بر اساس order)")
    
    autoplay = models.BooleanField(default=True)
    interval_ms = models.PositiveIntegerField(default=5000)
    show_arrows = models.BooleanField(default=True)
    show_indicators = models.BooleanField(default=True)
    pause_on_hover = models.BooleanField(default=True)

    # سایزبندی
    use_custom_size = models.BooleanField(
        default=False,
        verbose_name=_("سایزبندی دستی"),
        help_text=_("اگر فعال باشد از ارتفاع‌های ثابت به‌جای نسبت تصویر استفاده می‌شود"),
    )
    height_desktop = models.PositiveIntegerField(
        default=480,
        verbose_name=_("ارتفاع دسکتاپ (px)"),
        help_text=_("مثلاً 480 یا 600"),
    )
    height_mobile = models.PositiveIntegerField(
        default=260,
        verbose_name=_("ارتفاع موبایل (px)"),
        help_text=_("مثلاً 220 یا 280"),
    )
    max_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("حداکثر عرض (px)"),
        help_text=_("اختیاری؛ اگر پر شود، اسلایدر در مرکز با این حداکثر عرض نمایش داده می‌شود"),
    )
    aspect_ratio = models.CharField(
        max_length=10,
        default="21/9",
        verbose_name=_("نسبت تصویر (در صورت غیرفعال بودن سایزبندی دستی)"),
        help_text=_("مثل 16/9 یا 21/9"),
    )
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.TOP,
        verbose_name=_("موقعیت اسلایدر"),
        help_text=_("جای قرار گرفتن اسلایدر در صفحه هوم")
    )
    custom_order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("ترتیب سفارشی"),
        help_text=_("فقط وقتی موقعیت 'سفارشی' انتخاب شده باشد استفاده می‌شود")
    )

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


class HomePageSection(models.Model):
    """مدل برای مدیریت بخش‌های صفحه هوم از ادمین"""
    
    class SectionType(models.TextChoices):
        VIDEOS = "videos", _("ویدیوها")
        PRODUCTS = "products", _("محصولات")
        POSTS = "posts", _("مقالات")
        SLIDER = "slider", _("اسلایدر")
    
    # اطلاعات اصلی
    section_type = models.CharField(
        max_length=20,
        choices=SectionType.choices,
        verbose_name=_("نوع بخش"),
        help_text=_("نوع محتوایی که در این بخش نمایش داده می‌شود")
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("عنوان بخش"),
        help_text=_("مثلاً: ویدیوهای جدید، پکیج‌های آموزشی")
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name=_("زیرعنوان"),
        help_text=_("توضیح کوتاه برای بخش")
    )
    
    # تنظیمات نمایش
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("ترتیب نمایش"),
        help_text=_("بخش‌ها بر اساس این عدد مرتب می‌شوند")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال"),
        help_text=_("اگر غیرفعال باشد، این بخش نمایش داده نمی‌شود")
    )
    
    # تعداد و حالت انتخاب
    item_count = models.PositiveSmallIntegerField(
        default=6,
        verbose_name=_("تعداد آیتم‌ها"),
        help_text=_("تعداد آیتم‌هایی که در این بخش نمایش داده می‌شود")
    )
    use_manual_items = models.BooleanField(
        default=False,
        verbose_name=_("انتخاب دستی آیتم‌ها"),
        help_text=_("اگر فعال باشد، به‌جای فیلتر، آیتم‌ها را به‌صورت دستی انتخاب می‌کنید")
    )
    # فقط برای بخش ویدیوها استفاده می‌شود
    manual_videos = models.ManyToManyField(
        "courses.Video",
        blank=True,
        related_name="home_manual_sections",
        verbose_name=_("ویدیوهای انتخاب‌شده دستی"),
        help_text=_("اگر این فیلد خالی نباشد و 'انتخاب دستی' فعال باشد، فقط همین ویدیوها نمایش داده می‌شوند")
    )
    
    # فیلترهای ویدیو - ویژگی‌های اصلی
    video_filter_featured = models.BooleanField(
        default=False,
        verbose_name=_("فقط ویدیوهای ویژه"),
        help_text=_("اگر فعال باشد، فقط ویدیوهای ویژه نمایش داده می‌شوند")
    )
    video_filter_is_free = models.BooleanField(
        default=False,
        verbose_name=_("فقط ویدیوهای رایگان"),
        help_text=_("اگر فعال باشد، فقط ویدیوهای رایگان نمایش داده می‌شوند")
    )
    video_filter_has_youtube = models.BooleanField(
        default=False,
        verbose_name=_("فقط ویدیوهای دارای لینک یوتیوب"),
        help_text=_("اگر فعال باشد، فقط ویدیوهایی که لینک یوتیوب دارند نمایش داده می‌شوند")
    )
    
    # فیلترهای ویدیو - سطح و موضوع
    video_filter_level = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[("A1", "A1"), ("A2", "A2"), ("B1", "B1"), ("B2", "B2"), ("C1", "C1")],
        verbose_name=_("فیلتر بر اساس سطح"),
        help_text=_("اگر انتخاب شود، فقط ویدیوهای این سطح نمایش داده می‌شوند")
    )
    video_filter_topic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
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
        verbose_name=_("فیلتر بر اساس موضوع"),
        help_text=_("اگر انتخاب شود، فقط ویدیوهای این موضوع نمایش داده می‌شوند")
    )
    video_filter_difficulty = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ("beginner", _("مبتدی")),
            ("intermediate", _("متوسط")),
            ("advanced", _("پیشرفته")),
        ],
        verbose_name=_("فیلتر بر اساس سطح دشواری"),
        help_text=_("اگر انتخاب شود، فقط ویدیوهای این سطح دشواری نمایش داده می‌شوند")
    )
    
    # فیلترهای ویدیو - مدت زمان
    video_filter_duration_min = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("حداقل مدت زمان (دقیقه)"),
        help_text=_("فقط ویدیوهایی که حداقل این مدت زمان را دارند نمایش داده می‌شوند")
    )
    video_filter_duration_max = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("حداکثر مدت زمان (دقیقه)"),
        help_text=_("فقط ویدیوهایی که حداکثر این مدت زمان را دارند نمایش داده می‌شوند")
    )
    
    # فیلترهای ویدیو - مرتب‌سازی
    video_order_by = models.CharField(
        max_length=30,
        blank=True,
        default="-created_at",
        choices=[
            ("-created_at", _("جدیدترین (پیش‌فرض)")),
            ("created_at", _("قدیمی‌ترین")),
            ("-duration_minutes", _("طولانی‌ترین")),
            ("duration_minutes", _("کوتاه‌ترین")),
            ("title", _("عنوان (الفبایی)")),
            ("-title", _("عنوان (الفبایی معکوس)")),
            ("-is_featured", _("ویژه اول")),
        ],
        verbose_name=_("مرتب‌سازی بر اساس"),
        help_text=_("نحوه مرتب‌سازی ویدیوها در این بخش")
    )
    
    # فیلترهای محصول
    product_filter_featured = models.BooleanField(
        default=False,
        verbose_name=_("فقط محصولات ویژه"),
        help_text=_("اگر فعال باشد، فقط محصولات ویژه نمایش داده می‌شوند")
    )
    product_filter_active = models.BooleanField(
        default=True,
        verbose_name=_("فقط محصولات فعال"),
        help_text=_("فقط محصولات فعال نمایش داده می‌شوند")
    )
    
    # فیلترهای پست
    post_filter_featured = models.BooleanField(
        default=False,
        verbose_name=_("فقط مقالات ویژه"),
        help_text=_("اگر فعال باشد، فقط مقالات ویژه نمایش داده می‌شوند")
    )
    
    # لینک "همه"
    show_view_all_button = models.BooleanField(
        default=True,
        verbose_name=_("نمایش دکمه 'همه'"),
        help_text=_("اگر فعال باشد، دکمه 'همه' نمایش داده می‌شود")
    )
    view_all_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name=_("متن دکمه 'همه'"),
        help_text=_("مثلاً: همه ویدیوها، همه پکیج‌ها. اگر خالی باشد، به صورت خودکار تنظیم می‌شود")
    )
    view_all_button_url = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name=_("لینک دکمه 'همه'"),
        help_text=_("مثلاً: /videos/، /shop/. اگر خالی باشد، به صورت خودکار تنظیم می‌شود")
    )
    view_all_button_icon = models.CharField(
        max_length=50,
        blank=True,
        default="fas fa-arrow-left",
        verbose_name=_("آیکون دکمه 'همه'")
    )
    
    # آیکون بخش (اختیاری)
    section_icon = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name=_("آیکون بخش"),
        help_text=_("آیکون FontAwesome برای بخش (اختیاری)")
    )
    
    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("بخش صفحه هوم")
        verbose_name_plural = _("بخش‌های صفحه هوم")
    
    def __str__(self) -> str:
        status = "✓" if self.is_active else "✗"
        return f"{status} {self.get_section_type_display()}: {self.title}"
    
    def get_view_all_url(self):
        """برگرداندن URL دکمه 'همه' به صورت خودکار اگر تنظیم نشده باشد"""
        if self.view_all_button_url:
            return self.view_all_button_url
        
        url_map = {
            "videos": "/videos/",
            "products": "/shop/",
            "posts": "/blog/",
        }
        return url_map.get(self.section_type, "#")
    
    def get_view_all_text(self):
        """برگرداندن متن دکمه 'همه' به صورت خودکار اگر تنظیم نشده باشد"""
        if self.view_all_button_text:
            return self.view_all_button_text
        
        text_map = {
            "videos": "همه ویدیوها",
            "products": "همه پکیج‌ها",
            "posts": "همه مقالات",
        }
        return text_map.get(self.section_type, "مشاهده همه")


class SocialLink(models.Model):
    """
    لینک‌های شبکه‌های اجتماعی که از ادمین قابل مدیریت هستند.
    می‌توان برای هر بخشِ سایت (مثل صفحه تماس) لینک‌های جدا تعریف کرد.
    """

    class Location(models.TextChoices):
        CONTACT = "contact", _("صفحه تماس")
        HEADER = "header", _("هدر")
        FOOTER = "footer", _("فوتر")

    title = models.CharField(max_length=50, verbose_name=_("عنوان"))
    url = models.CharField(max_length=300, verbose_name=_("لینک"))
    icon_class = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name=_("کلاس آیکون (FontAwesome)"),
        help_text=_("مثلاً: fab fa-instagram، fab fa-telegram، fab fa-whatsapp"),
    )
    location = models.CharField(
        max_length=20,
        choices=Location.choices,
        default=Location.CONTACT,
        verbose_name=_("محل نمایش"),
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("ترتیب"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("لینک شبکه اجتماعی")
        verbose_name_plural = _("لینک‌های شبکه اجتماعی")

    def __str__(self) -> str:
        return f"{self.title} ({self.get_location_display()})"
