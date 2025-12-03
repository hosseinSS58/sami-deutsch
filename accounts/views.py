from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from .models import Profile
from .forms import SignUpForm, CustomAuthForm, ProfileEditForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy("accounts:profile")


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد مدیریت برای مدیران سایت"""
    template_name = "accounts/admin_dashboard.html"
    
    def dispatch(self, request, *args, **kwargs):
        # بررسی دسترسی: فقط کاربرانی که user_category آنها admin است می‌توانند وارد شوند
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.user_category != Profile.UserCategory.ADMIN:
            from django.shortcuts import redirect
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models
        from courses.models import Video
        from blog.models import Post
        from shop.models import Product, Order
        from siteconfig.models import HomePageSection, Slide
        from core.models import SiteVisit
        
        # آمار کلی
        total_users = User.objects.count()
        total_admins = User.objects.filter(profile__user_category=Profile.UserCategory.ADMIN).count()
        total_regular_users = User.objects.filter(profile__user_category=Profile.UserCategory.USER).count()
        
        total_videos = Video.objects.count()
        featured_videos = Video.objects.filter(is_featured=True).count()
        free_videos = Video.objects.filter(is_free=True).count()
        
        total_posts = Post.objects.count()
        featured_posts = Post.objects.filter(is_featured=True).count()
        total_post_views = Post.objects.aggregate(total=Sum("views_count"))["total"] or 0
        
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        
        total_orders = Order.objects.count()
        paid_orders = Order.objects.filter(status=Order.Status.PAID).count()
        total_revenue = Order.objects.filter(status=Order.Status.PAID).aggregate(
            total=Sum("total_amount")
        )["total"] or 0
        
        # آمار هفته گذشته
        week_ago = timezone.now() - timedelta(days=7)
        recent_users = User.objects.filter(date_joined__gte=week_ago).count()
        recent_videos = Video.objects.filter(created_at__gte=week_ago).count()
        recent_posts = Post.objects.filter(published_at__gte=week_ago).count()
        recent_orders = Order.objects.filter(created_at__gte=week_ago).count()
        
        # آخرین فعالیت‌ها با pagination
        videos_qs = Video.objects.order_by("-created_at")
        posts_qs = Post.objects.order_by("-published_at")
        orders_qs = Order.objects.order_by("-created_at")
        users_qs = User.objects.order_by("-date_joined")
        
        # Pagination برای ویدیوها
        videos_paginator = Paginator(videos_qs, 10)
        videos_page = self.request.GET.get('videos_page', 1)
        try:
            latest_videos = videos_paginator.page(videos_page)
        except (PageNotAnInteger, EmptyPage):
            latest_videos = videos_paginator.page(1)
        
        # Pagination برای مقالات
        posts_paginator = Paginator(posts_qs, 10)
        posts_page = self.request.GET.get('posts_page', 1)
        try:
            latest_posts = posts_paginator.page(posts_page)
        except (PageNotAnInteger, EmptyPage):
            latest_posts = posts_paginator.page(1)
        
        # Pagination برای سفارشات
        orders_paginator = Paginator(orders_qs, 10)
        orders_page = self.request.GET.get('orders_page', 1)
        try:
            latest_orders = orders_paginator.page(orders_page)
        except (PageNotAnInteger, EmptyPage):
            latest_orders = orders_paginator.page(1)
        
        # Pagination برای کاربران
        users_paginator = Paginator(users_qs, 10)
        users_page = self.request.GET.get('users_page', 1)
        try:
            latest_users = users_paginator.page(users_page)
        except (PageNotAnInteger, EmptyPage):
            latest_users = users_paginator.page(1)
        
        # تعداد بخش‌های صفحه هوم
        home_sections_count = HomePageSection.objects.filter(is_active=True).count()
        active_slides_count = Slide.objects.filter(is_active=True).count()

        # آمار بازدید سایت (۷ روز گذشته)
        visits_7_days_qs = SiteVisit.objects.filter(created_at__gte=week_ago)
        visits_total_7_days = visits_7_days_qs.count()

        visits_by_day = (
            visits_7_days_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        top_pages = (
            visits_7_days_qs.values("path")
            .annotate(count=Count("id"))
            .order_by("-count")[:1]  # فقط اولین صفحه برای خلاصه داشبورد
        )

        top_referrers = (
            visits_7_days_qs.exclude(referrer="")
            .values("referrer")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        mobile_visits = visits_7_days_qs.filter(user_agent__icontains="mobile").count()
        desktop_visits = visits_7_days_qs.count() - mobile_visits
        
        context.update({
            # آمار کاربران
            "total_users": total_users,
            "total_admins": total_admins,
            "total_regular_users": total_regular_users,
            "recent_users": recent_users,
            
            # آمار ویدیوها
            "total_videos": total_videos,
            "featured_videos": featured_videos,
            "free_videos": free_videos,
            "recent_videos": recent_videos,
            
            # آمار مقالات
            "total_posts": total_posts,
            "featured_posts": featured_posts,
            "total_post_views": total_post_views,
            "recent_posts": recent_posts,
            
            # آمار محصولات
            "total_products": total_products,
            "active_products": active_products,
            
            # آمار سفارشات
            "total_orders": total_orders,
            "paid_orders": paid_orders,
            "total_revenue": total_revenue,
            "recent_orders": recent_orders,
            
            # آخرین فعالیت‌ها با pagination
            "latest_videos": latest_videos,
            "latest_posts": latest_posts,
            "latest_orders": latest_orders,
            "latest_users": latest_users,
            "videos_paginator": videos_paginator,
            "posts_paginator": posts_paginator,
            "orders_paginator": orders_paginator,
            "users_paginator": users_paginator,
            
            # تنظیمات صفحه هوم
            "home_sections_count": home_sections_count,
            "active_slides_count": active_slides_count,

            # آمار بازدید سایت
            "visits_total_7_days": visits_total_7_days,
            "visits_by_day": list(visits_by_day),
            "top_pages": list(top_pages),
            "top_referrers": list(top_referrers),
            "mobile_visits": mobile_visits,
            "desktop_visits": desktop_visits,
        })
        
        return context


class AnalyticsDetailView(LoginRequiredMixin, TemplateView):
    """صفحه آمار بازدیدها با جزئیات کامل"""
    template_name = "accounts/analytics_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        # بررسی دسترسی: فقط کاربرانی که user_category آنها admin است می‌توانند وارد شوند
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.user_category != Profile.UserCategory.ADMIN:
            from django.shortcuts import redirect
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models
        from core.models import SiteVisit, YouTubeClick
        from courses.models import Video
        from blog.models import Post
        
        # دریافت بازه زمانی از query parameter (پیش‌فرض: 30 روز)
        days = int(self.request.GET.get("days", 30))
        days = min(max(days, 1), 365)  # محدود کردن بین 1 تا 365 روز
        
        date_from = timezone.now() - timedelta(days=days)
        
        # آمار بازدیدها
        visits_qs = SiteVisit.objects.filter(created_at__gte=date_from)
        total_visits = visits_qs.count()
        unique_visitors = visits_qs.values("ip_address").distinct().count()
        logged_in_visits = visits_qs.exclude(user=None).count()
        anonymous_visits = total_visits - logged_in_visits
        
        # آمار بازدیدکنندگان ناشناس
        from core.models import AnonymousVisitor
        anonymous_visitors_qs = AnonymousVisitor.objects.filter(last_seen__gte=date_from)
        total_anonymous_visitors = anonymous_visitors_qs.count()
        # محاسبه تعداد بازدیدهای بازدیدکنندگان ناشناس
        total_anonymous_visitor_visits = SiteVisit.objects.filter(
            anonymous_visitor__isnull=False,
            anonymous_visitor__last_seen__gte=date_from,
            created_at__gte=date_from
        ).count()
        
        # بازدیدها به تفکیک روز
        visits_by_day = (
            visits_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"), unique_ips=Count("ip_address", distinct=True))
            .order_by("day")
        )
        
        # محبوب‌ترین صفحات با pagination
        top_pages_qs = (
            visits_qs.values("path")
            .annotate(
                count=Count("id"),
                unique_visitors=Count("ip_address", distinct=True)
            )
            .order_by("-count")
        )
        top_pages_paginator = Paginator(list(top_pages_qs), 20)
        top_pages_page = self.request.GET.get('top_pages_page', 1)
        try:
            top_pages = top_pages_paginator.page(top_pages_page)
        except (PageNotAnInteger, EmptyPage):
            top_pages = top_pages_paginator.page(1)
        
        # منابع ورودی (Referrers) با pagination
        top_referrers_qs = (
            visits_qs.exclude(referrer="")
            .values("referrer")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        top_referrers_paginator = Paginator(list(top_referrers_qs), 20)
        top_referrers_page = self.request.GET.get('top_referrers_page', 1)
        try:
            top_referrers = top_referrers_paginator.page(top_referrers_page)
        except (PageNotAnInteger, EmptyPage):
            top_referrers = top_referrers_paginator.page(1)
        
        # بازدیدها به تفکیک دستگاه (بر اساس تعداد بازدیدکننده، نه تعداد بازدید)
        # برای سادگی، بازدیدکننده را بر اساس IP در نظر می‌گیریم
        mobile_visits = (
            visits_qs.filter(device_type="mobile")
            .values("ip_address")
            .distinct()
            .count()
        )
        tablet_visits = (
            visits_qs.filter(device_type="tablet")
            .values("ip_address")
            .distinct()
            .count()
        )
        desktop_visits = (
            visits_qs.filter(device_type="desktop")
            .values("ip_address")
            .distinct()
            .count()
        )
        unknown_device_visits = (
            visits_qs.filter(device_type__in=["", "unknown"])
            .values("ip_address")
            .distinct()
            .count()
        )
        
        # بازدیدکنندگان ناشناس به تفکیک دستگاه (Distinct بر اساس AnonymousVisitor)
        anonymous_mobile_visits = (
            visits_qs.filter(anonymous_visitor__isnull=False, device_type="mobile")
            .values("anonymous_visitor_id")
            .distinct()
            .count()
        )
        anonymous_tablet_visits = (
            visits_qs.filter(anonymous_visitor__isnull=False, device_type="tablet")
            .values("anonymous_visitor_id")
            .distinct()
            .count()
        )
        anonymous_desktop_visits = (
            visits_qs.filter(anonymous_visitor__isnull=False, device_type="desktop")
            .values("anonymous_visitor_id")
            .distinct()
            .count()
        )
        
        # بازدیدکنندگان لاگین شده به تفکیک دستگاه (Distinct بر اساس کاربر)
        logged_mobile_visits = (
            visits_qs.exclude(user=None)
            .filter(device_type="mobile")
            .values("user_id")
            .distinct()
            .count()
        )
        logged_tablet_visits = (
            visits_qs.exclude(user=None)
            .filter(device_type="tablet")
            .values("user_id")
            .distinct()
            .count()
        )
        logged_desktop_visits = (
            visits_qs.exclude(user=None)
            .filter(device_type="desktop")
            .values("user_id")
            .distinct()
            .count()
        )
        
        # بازدیدها به تفکیک کد وضعیت
        status_code_stats = (
            visits_qs.values("status_code")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        
        # بازدیدها به تفکیک کشور
        top_countries_qs = (
            visits_qs.exclude(country="")
            .values("country")
            .annotate(
                count=Count("id"),
                unique_ips=Count("ip_address", distinct=True)
            )
            .order_by("-count")
        )
        top_countries_paginator = Paginator(list(top_countries_qs), 20)
        top_countries_page = self.request.GET.get('top_countries_page', 1)
        try:
            top_countries = top_countries_paginator.page(top_countries_page)
        except (PageNotAnInteger, EmptyPage):
            top_countries = top_countries_paginator.page(1)
        
        # آمار کلیک‌های یوتیوب
        youtube_clicks_qs = YouTubeClick.objects.filter(created_at__gte=date_from)
        total_youtube_clicks = youtube_clicks_qs.count()
        unique_youtube_clickers = youtube_clicks_qs.values("ip_address").distinct().count()
        logged_in_youtube_clicks = youtube_clicks_qs.exclude(user=None).count()
        
        # کلیک‌های یوتیوب به تفکیک روز
        youtube_clicks_by_day = (
            youtube_clicks_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        
        # محبوب‌ترین ویدیوهای یوتیوب (بر اساس کلیک) با pagination
        top_youtube_videos_qs = (
            youtube_clicks_qs.exclude(youtube_id="")
            .values("youtube_id", "source_title", "source_type")
            .annotate(
                count=Count("id"),
                unique_clickers=Count("ip_address", distinct=True)
            )
            .order_by("-count")
        )
        top_youtube_videos_paginator = Paginator(list(top_youtube_videos_qs), 20)
        top_youtube_videos_page = self.request.GET.get('top_youtube_videos_page', 1)
        try:
            top_youtube_videos = top_youtube_videos_paginator.page(top_youtube_videos_page)
        except (PageNotAnInteger, EmptyPage):
            top_youtube_videos = top_youtube_videos_paginator.page(1)
        
        # کلیک‌های یوتیوب به تفکیک منبع (ویدیو / مقاله)
        youtube_clicks_by_source = (
            youtube_clicks_qs.values("source_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        
        # کاربرانی که بیشترین کلیک روی یوتیوب داشته‌اند
        top_youtube_users = (
            youtube_clicks_qs.exclude(user=None)
            .values("user__id", "user__username", "user__email")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # مراجعانی که بیشترین کلیک روی یوتیوب داشته‌اند
        top_youtube_referrers = (
            youtube_clicks_qs.exclude(referrer="")
            .values("referrer")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # آخرین کلیک‌های یوتیوب با pagination
        latest_youtube_clicks_qs = youtube_clicks_qs.select_related("user").order_by("-created_at")
        youtube_clicks_paginator = Paginator(latest_youtube_clicks_qs, 25)
        youtube_clicks_page = self.request.GET.get('youtube_clicks_page', 1)
        try:
            latest_youtube_clicks = youtube_clicks_paginator.page(youtube_clicks_page)
        except (PageNotAnInteger, EmptyPage):
            latest_youtube_clicks = youtube_clicks_paginator.page(1)
        
        # لیست بازدیدکنندگان ناشناس با pagination
        anonymous_visitors_list_qs = AnonymousVisitor.objects.filter(last_seen__gte=date_from).order_by("-last_seen")
        anonymous_visitors_list_paginator = Paginator(anonymous_visitors_list_qs, 20)
        anonymous_visitors_list_page = self.request.GET.get('anonymous_visitors_list_page', 1)
        try:
            anonymous_visitors_list = anonymous_visitors_list_paginator.page(anonymous_visitors_list_page)
        except (PageNotAnInteger, EmptyPage):
            anonymous_visitors_list = anonymous_visitors_list_paginator.page(1)
        
        context.update({
            "days": days,
            "date_from": date_from,
            
            # آمار کلی بازدیدها
            "total_visits": total_visits,
            "unique_visitors": unique_visitors,
            "logged_in_visits": logged_in_visits,
            "anonymous_visits": anonymous_visits,
            "total_anonymous_visitors": total_anonymous_visitors,
            "total_anonymous_visitor_visits": total_anonymous_visitor_visits,
            
            # آمار تفصیلی بازدیدها
            "visits_by_day": list(visits_by_day),
            "top_pages": top_pages,
            "top_referrers": top_referrers,
            "top_pages_paginator": top_pages_paginator,
            "top_referrers_paginator": top_referrers_paginator,
            "top_countries": top_countries,
            "top_countries_paginator": top_countries_paginator,
            "mobile_visits": mobile_visits,
            "tablet_visits": tablet_visits,
            "desktop_visits": desktop_visits,
            "unknown_device_visits": unknown_device_visits,
            "anonymous_mobile_visits": anonymous_mobile_visits,
            "anonymous_tablet_visits": anonymous_tablet_visits,
            "anonymous_desktop_visits": anonymous_desktop_visits,
            "logged_mobile_visits": logged_mobile_visits,
            "logged_tablet_visits": logged_tablet_visits,
            "logged_desktop_visits": logged_desktop_visits,
            "status_code_stats": list(status_code_stats),
            
            # آمار کلیک‌های یوتیوب
            "total_youtube_clicks": total_youtube_clicks,
            "unique_youtube_clickers": unique_youtube_clickers,
            "logged_in_youtube_clicks": logged_in_youtube_clicks,
            
            # آمار تفصیلی کلیک‌های یوتیوب
            "youtube_clicks_by_day": list(youtube_clicks_by_day),
            "top_youtube_videos": top_youtube_videos,
            "top_youtube_videos_paginator": top_youtube_videos_paginator,
            "youtube_clicks_by_source": list(youtube_clicks_by_source),
            "top_youtube_users": list(top_youtube_users),
            "top_youtube_referrers": list(top_youtube_referrers),
            "latest_youtube_clicks": latest_youtube_clicks,
            "youtube_clicks_paginator": youtube_clicks_paginator,
            
            # بازدیدکنندگان ناشناس
            "anonymous_visitors_list": anonymous_visitors_list,
            "anonymous_visitors_list_paginator": anonymous_visitors_list_paginator,
        })
        
        return context


class AnalyticsUserDetailView(LoginRequiredMixin, TemplateView):
    """آمار تفصیلی برای یک کاربر مشخص"""
    template_name = "accounts/user_analytics.html"

    def dispatch(self, request, *args, **kwargs):
        # فقط مدیران سایت
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.user_category != Profile.UserCategory.ADMIN:
            from django.shortcuts import redirect
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from django.shortcuts import get_object_or_404
        from core.models import SiteVisit, YouTubeClick

        user_id = self.kwargs.get("user_id")
        target_user = get_object_or_404(User, id=user_id)

        # بازه زمانی (پیش‌فرض: 30 روز)
        days = int(self.request.GET.get("days", 30))
        days = min(max(days, 1), 365)
        date_from = timezone.now() - timedelta(days=days)

        # بازدیدهای این کاربر
        visits_qs = SiteVisit.objects.filter(user=target_user, created_at__gte=date_from)
        total_visits = visits_qs.count()
        unique_ips = visits_qs.values("ip_address").distinct().count()

        # بازدیدها به تفکیک روز
        visits_by_day = (
            visits_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # مسیرهای پربازدید این کاربر با pagination
        top_pages_qs = (
            visits_qs.values("path")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        user_top_pages_paginator = Paginator(list(top_pages_qs), 20)
        user_top_pages_page = self.request.GET.get('user_top_pages_page', 1)
        try:
            top_pages = user_top_pages_paginator.page(user_top_pages_page)
        except (PageNotAnInteger, EmptyPage):
            top_pages = user_top_pages_paginator.page(1)

        # IP ها و دستگاه‌ها
        recent_ips = (
            visits_qs.exclude(ip_address="")
            .values("ip_address", "country")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        recent_user_agents = (
            visits_qs.exclude(user_agent="")
            .values("user_agent", "device_type")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # بازدیدها به تفکیک کشور
        user_top_countries = (
            visits_qs.exclude(country="")
            .values("country")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # بازدیدها به تفکیک نوع دستگاه
        user_device_types = (
            visits_qs.exclude(device_type="")
            .values("device_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # آمار کلیک‌های یوتیوب برای این کاربر
        yt_qs = YouTubeClick.objects.filter(user=target_user, created_at__gte=date_from)
        total_youtube_clicks = yt_qs.count()

        youtube_clicks_by_day = (
            yt_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # ویدیوهای یوتیوبی که بیشتر کلیک شده‌اند با pagination
        youtube_top_videos_qs = (
            yt_qs.exclude(youtube_id="")
            .values("youtube_id", "source_title", "source_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        user_youtube_top_videos_paginator = Paginator(list(youtube_top_videos_qs), 20)
        user_youtube_top_videos_page = self.request.GET.get('user_youtube_top_videos_page', 1)
        try:
            youtube_top_videos = user_youtube_top_videos_paginator.page(user_youtube_top_videos_page)
        except (PageNotAnInteger, EmptyPage):
            youtube_top_videos = user_youtube_top_videos_paginator.page(1)

        # آخرین بازدیدها با pagination
        latest_visits_qs = visits_qs.order_by("-created_at")
        user_visits_paginator = Paginator(latest_visits_qs, 25)
        user_visits_page = self.request.GET.get('user_visits_page', 1)
        try:
            latest_visits = user_visits_paginator.page(user_visits_page)
        except (PageNotAnInteger, EmptyPage):
            latest_visits = user_visits_paginator.page(1)
        
        # آخرین کلیک‌های یوتیوب با pagination
        latest_youtube_clicks_qs = yt_qs.order_by("-created_at")
        user_youtube_clicks_paginator = Paginator(latest_youtube_clicks_qs, 25)
        user_youtube_clicks_page = self.request.GET.get('user_youtube_clicks_page', 1)
        try:
            latest_youtube_clicks = user_youtube_clicks_paginator.page(user_youtube_clicks_page)
        except (PageNotAnInteger, EmptyPage):
            latest_youtube_clicks = user_youtube_clicks_paginator.page(1)

        context.update(
            {
                "target_user": target_user,
                "profile": getattr(target_user, "profile", None),
                "days": days,
                "date_from": date_from,
                # بازدیدها
                "total_visits": total_visits,
                "unique_ips": unique_ips,
                "visits_by_day": list(visits_by_day),
                "top_pages": top_pages,
                "user_top_pages_paginator": user_top_pages_paginator,
                "recent_ips": list(recent_ips),
                "recent_user_agents": list(recent_user_agents),
                "user_top_countries": list(user_top_countries),
                "user_device_types": list(user_device_types),
                "latest_visits": latest_visits,
                "user_visits_paginator": user_visits_paginator,
                # کلیک‌های یوتیوب
                "total_youtube_clicks": total_youtube_clicks,
                "youtube_clicks_by_day": list(youtube_clicks_by_day),
                "youtube_top_videos": youtube_top_videos,
                "user_youtube_top_videos_paginator": user_youtube_top_videos_paginator,
                "latest_youtube_clicks": latest_youtube_clicks,
                "user_youtube_clicks_paginator": user_youtube_clicks_paginator,
            }
        )

        return context


class AnalyticsAnonymousVisitorsView(LoginRequiredMixin, TemplateView):
    """لیست بازدیدکنندگان ناشناس"""
    template_name = "accounts/anonymous_visitors.html"
    
    def dispatch(self, request, *args, **kwargs):
        # فقط مدیران سایت
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.user_category != Profile.UserCategory.ADMIN:
            from django.shortcuts import redirect
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from core.models import AnonymousVisitor
        
        # بازه زمانی (پیش‌فرض: 30 روز)
        days = int(self.request.GET.get("days", 30))
        days = min(max(days, 1), 365)
        date_from = timezone.now() - timedelta(days=days)
        
        # فیلتر بازدیدکنندگان ناشناس بر اساس بازه زمانی
        visitors_qs = AnonymousVisitor.objects.filter(last_seen__gte=date_from).order_by("-last_seen")
        
        # Pagination
        visitors_paginator = Paginator(visitors_qs, 25)
        visitors_page = self.request.GET.get('visitors_page', 1)
        try:
            visitors = visitors_paginator.page(visitors_page)
        except (PageNotAnInteger, EmptyPage):
            visitors = visitors_paginator.page(1)
        
        # آمار کلی
        total_anonymous_visitors = AnonymousVisitor.objects.filter(last_seen__gte=date_from).count()
        total_anonymous_visits = AnonymousVisitor.objects.filter(last_seen__gte=date_from).aggregate(
            total=Count("site_visits")
        )["total"] or 0
        
        context.update({
            "days": days,
            "date_from": date_from,
            "visitors": visitors,
            "visitors_paginator": visitors_paginator,
            "total_anonymous_visitors": total_anonymous_visitors,
            "total_anonymous_visits": total_anonymous_visits,
        })
        
        return context


class AnalyticsAnonymousVisitorDetailView(LoginRequiredMixin, TemplateView):
    """جزئیات یک بازدیدکننده ناشناس"""
    template_name = "accounts/anonymous_visitor_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        # فقط مدیران سایت
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.user_category != Profile.UserCategory.ADMIN:
            from django.shortcuts import redirect
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from django.shortcuts import get_object_or_404
        from core.models import AnonymousVisitor, SiteVisit, YouTubeClick
        
        visitor_id = self.kwargs.get("visitor_id")
        visitor = get_object_or_404(AnonymousVisitor, id=visitor_id)
        
        # بازه زمانی (پیش‌فرض: 30 روز)
        days = int(self.request.GET.get("days", 30))
        days = min(max(days, 1), 365)
        date_from = timezone.now() - timedelta(days=days)
        
        # بازدیدهای این بازدیدکننده ناشناس
        visits_qs = SiteVisit.objects.filter(anonymous_visitor=visitor, created_at__gte=date_from)
        total_visits = visits_qs.count()
        unique_ips = visits_qs.values("ip_address").distinct().count()
        
        # بازدیدها به تفکیک روز
        visits_by_day = (
            visits_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        
        # مسیرهای پربازدید با pagination
        top_pages_qs = (
            visits_qs.values("path")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        visitor_top_pages_paginator = Paginator(list(top_pages_qs), 20)
        visitor_top_pages_page = self.request.GET.get('visitor_top_pages_page', 1)
        try:
            top_pages = visitor_top_pages_paginator.page(visitor_top_pages_page)
        except (PageNotAnInteger, EmptyPage):
            top_pages = visitor_top_pages_paginator.page(1)
        
        # IP ها و دستگاه‌ها
        recent_ips = (
            visits_qs.exclude(ip_address="")
            .values("ip_address", "country")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        recent_user_agents = (
            visits_qs.exclude(user_agent="")
            .values("user_agent", "device_type")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # بازدیدها به تفکیک کشور
        visitor_top_countries = (
            visits_qs.exclude(country="")
            .values("country")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # بازدیدها به تفکیک نوع دستگاه
        visitor_device_types = (
            visits_qs.exclude(device_type="")
            .values("device_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        
        # آمار کلیک‌های یوتیوب برای این بازدیدکننده ناشناس
        yt_qs = YouTubeClick.objects.filter(anonymous_visitor=visitor, created_at__gte=date_from)
        total_youtube_clicks = yt_qs.count()
        
        youtube_clicks_by_day = (
            yt_qs.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        
        # ویدیوهای یوتیوبی که بیشتر کلیک شده‌اند با pagination
        youtube_top_videos_qs = (
            yt_qs.exclude(youtube_id="")
            .values("youtube_id", "source_title", "source_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        visitor_youtube_top_videos_paginator = Paginator(list(youtube_top_videos_qs), 20)
        visitor_youtube_top_videos_page = self.request.GET.get('visitor_youtube_top_videos_page', 1)
        try:
            youtube_top_videos = visitor_youtube_top_videos_paginator.page(visitor_youtube_top_videos_page)
        except (PageNotAnInteger, EmptyPage):
            youtube_top_videos = visitor_youtube_top_videos_paginator.page(1)
        
        # آخرین بازدیدها با pagination
        latest_visits_qs = visits_qs.order_by("-created_at")
        visitor_visits_paginator = Paginator(latest_visits_qs, 25)
        visitor_visits_page = self.request.GET.get('visitor_visits_page', 1)
        try:
            latest_visits = visitor_visits_paginator.page(visitor_visits_page)
        except (PageNotAnInteger, EmptyPage):
            latest_visits = visitor_visits_paginator.page(1)
        
        # آخرین کلیک‌های یوتیوب با pagination
        latest_youtube_clicks_qs = yt_qs.order_by("-created_at")
        visitor_youtube_clicks_paginator = Paginator(latest_youtube_clicks_qs, 25)
        visitor_youtube_clicks_page = self.request.GET.get('visitor_youtube_clicks_page', 1)
        try:
            latest_youtube_clicks = visitor_youtube_clicks_paginator.page(visitor_youtube_clicks_page)
        except (PageNotAnInteger, EmptyPage):
            latest_youtube_clicks = visitor_youtube_clicks_paginator.page(1)
        
        context.update({
            "visitor": visitor,
            "days": days,
            "date_from": date_from,
            # بازدیدها
            "total_visits": total_visits,
            "unique_ips": unique_ips,
            "visits_by_day": list(visits_by_day),
            "top_pages": top_pages,
            "visitor_top_pages_paginator": visitor_top_pages_paginator,
            "recent_ips": list(recent_ips),
            "recent_user_agents": list(recent_user_agents),
            "visitor_top_countries": list(visitor_top_countries),
            "visitor_device_types": list(visitor_device_types),
            "latest_visits": latest_visits,
            "visitor_visits_paginator": visitor_visits_paginator,
            # کلیک‌های یوتیوب
            "total_youtube_clicks": total_youtube_clicks,
            "youtube_clicks_by_day": list(youtube_clicks_by_day),
            "youtube_top_videos": youtube_top_videos,
            "visitor_youtube_top_videos_paginator": visitor_youtube_top_videos_paginator,
            "latest_youtube_clicks": latest_youtube_clicks,
            "visitor_youtube_clicks_paginator": visitor_youtube_clicks_paginator,
        })
        
        return context


# Create your views here.
