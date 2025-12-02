from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from courses.models import Video
from blog.models import Post
from shop.models import Product
from siteconfig.models import HomePageSection, HomeSlider, Slide


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # دریافت تنظیمات اسلایدر
        slider_settings = HomeSlider.load()
        home_slides = Slide.objects.filter(is_active=True).order_by("order", "id")
        ctx["home_slider_settings"] = slider_settings
        ctx["home_slides"] = home_slides
        
        # دریافت بخش‌های فعال صفحه هوم
        sections = HomePageSection.objects.filter(is_active=True).order_by("order", "id")
        
        # اگر اسلایدر موقعیت سفارشی دارد، آن را به لیست sections اضافه کن
        if slider_settings.position == "custom" and home_slides.exists():
            # یک section مجازی برای اسلایدر بساز
            from types import SimpleNamespace
            slider_section = SimpleNamespace(
                id=999999,  # عدد بزرگ برای اینکه همیشه آخر بیاید
                section_type="slider",
                title="",
                subtitle="",
                order=slider_settings.custom_order,
                is_active=True,
            )
            # sections را به لیست تبدیل کن، اسلایدر را اضافه کن، و دوباره مرتب کن
            sections_list = list(sections)
            sections_list.append(slider_section)
            sections = sorted(sections_list, key=lambda s: (s.order, s.id))
        
        # پردازش هر بخش و دریافت داده‌های مربوطه (بخش‌های داینامیک)
        section_data = []
        for section in sections:
            data = {
                "section": section,
                "items": [],
            }
            
            if section.section_type == "videos":
                # اگر انتخاب دستی فعال است و ویدیوهایی انتخاب شده‌اند، همان‌ها را نمایش بده
                if section.use_manual_items and section.manual_videos.exists():
                    data["items"] = list(
                        section.manual_videos.all().prefetch_related("youtube_links")[: section.item_count]
                    )
                else:
                    queryset = Video.objects.prefetch_related("youtube_links")
                    
                    # اعمال فیلترهای ویژگی‌ها
                    if section.video_filter_featured:
                        queryset = queryset.filter(is_featured=True)
                    if section.video_filter_is_free:
                        queryset = queryset.filter(is_free=True)
                    if section.video_filter_has_youtube:
                        # فیلتر ویدیوهایی که لینک یوتیوب فعال دارند
                        queryset = queryset.filter(youtube_links__is_active=True).distinct()
                    
                    # اعمال فیلترهای سطح و موضوع
                    if section.video_filter_level:
                        queryset = queryset.filter(level=section.video_filter_level)
                    if section.video_filter_topic:
                        queryset = queryset.filter(topic=section.video_filter_topic)
                    if section.video_filter_difficulty:
                        queryset = queryset.filter(difficulty=section.video_filter_difficulty)
                    
                    # اعمال فیلترهای مدت زمان
                    if section.video_filter_duration_min:
                        queryset = queryset.filter(duration_minutes__gte=section.video_filter_duration_min)
                    if section.video_filter_duration_max:
                        queryset = queryset.filter(duration_minutes__lte=section.video_filter_duration_max)
                    
                    # مرتب‌سازی
                    order_by = section.video_order_by if section.video_order_by else "-created_at"
                    queryset = queryset.order_by(order_by)
                    
                    data["items"] = list(queryset[: section.item_count])
                
            elif section.section_type == "products":
                queryset = Product.objects.all()
                
                # اعمال فیلترها
                if section.product_filter_active:
                    queryset = queryset.filter(is_active=True)
                if section.product_filter_featured:
                    queryset = queryset.filter(is_featured=True)
                
                data["items"] = list(queryset.order_by("-created_at")[:section.item_count])
                
            elif section.section_type == "posts":
                queryset = Post.objects.all()
                
                # اعمال فیلترها
                if section.post_filter_featured:
                    queryset = queryset.filter(is_featured=True)
                
                data["items"] = list(queryset.order_by("-published_at")[:section.item_count])
            
            elif section.section_type == "slider":
                # اسلایدر در موقعیت سفارشی
                data["items"] = list(home_slides)
                data["slider"] = slider_settings
            
            section_data.append(data)
        
        ctx["home_sections"] = section_data
        
        # برای سازگاری با کد قدیمی (اگر بخشی از تمپلیت هنوز از این استفاده می‌کند)
        # سعی می‌کنیم بخش‌های قدیمی را هم پیدا کنیم
        videos_section = next((s for s in sections if s.section_type == "videos"), None)
        if videos_section:
            # اگر انتخاب دستی فعال است و ویدیوهایی انتخاب شده‌اند، همان‌ها را برای latest_videos هم استفاده کن
            if videos_section.use_manual_items and videos_section.manual_videos.exists():
                ctx["latest_videos"] = list(
                    videos_section.manual_videos.all().prefetch_related("youtube_links")[: videos_section.item_count]
                )
            else:
                queryset = Video.objects.prefetch_related("youtube_links")
                
                # اعمال فیلترهای ویژگی‌ها
                if videos_section.video_filter_featured:
                    queryset = queryset.filter(is_featured=True)
                if videos_section.video_filter_is_free:
                    queryset = queryset.filter(is_free=True)
                if videos_section.video_filter_has_youtube:
                    queryset = queryset.filter(youtube_links__is_active=True).distinct()
                
                # اعمال فیلترهای سطح و موضوع
                if videos_section.video_filter_level:
                    queryset = queryset.filter(level=videos_section.video_filter_level)
                if videos_section.video_filter_topic:
                    queryset = queryset.filter(topic=videos_section.video_filter_topic)
                if videos_section.video_filter_difficulty:
                    queryset = queryset.filter(difficulty=videos_section.video_filter_difficulty)
                
                # اعمال فیلترهای مدت زمان
                if videos_section.video_filter_duration_min:
                    queryset = queryset.filter(duration_minutes__gte=videos_section.video_filter_duration_min)
                if videos_section.video_filter_duration_max:
                    queryset = queryset.filter(duration_minutes__lte=videos_section.video_filter_duration_max)
                
                # مرتب‌سازی
                order_by = videos_section.video_order_by if videos_section.video_order_by else "-created_at"
                queryset = queryset.order_by(order_by)
                
                ctx["latest_videos"] = list(queryset[: videos_section.item_count])
        else:
            ctx["latest_videos"] = []
        
        products_section = next((s for s in sections if s.section_type == "products"), None)
        if products_section:
            queryset = Product.objects.all()
            if products_section.product_filter_active:
                queryset = queryset.filter(is_active=True)
            if products_section.product_filter_featured:
                queryset = queryset.filter(is_featured=True)
            ctx["latest_products"] = list(queryset.order_by("-created_at")[:products_section.item_count])
        else:
            ctx["latest_products"] = []
        
        posts_section = next((s for s in sections if s.section_type == "posts"), None)
        if posts_section:
            queryset = Post.objects.all()
            if posts_section.post_filter_featured:
                queryset = queryset.filter(is_featured=True)
            ctx["latest_posts"] = list(queryset.order_by("-published_at")[:posts_section.item_count])
        else:
            ctx["latest_posts"] = []
        
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("پیام شما با موفقیت ارسال شد!"))
        return super().form_valid(form)


# Create your views here.
