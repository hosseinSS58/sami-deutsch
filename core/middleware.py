from django.utils import timezone

from .models import SiteVisit, AnonymousVisitor
from .utils import get_country_from_ip, detect_device_type


class SiteAnalyticsMiddleware:
    """
    ثبت ساده آمار بازدید صفحات سایت
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            self.log_visit(request, response)
        except Exception:
            # آمار نباید باعث خطا در سایت شود
            pass

        return response

    def log_visit(self, request, response):
        # فقط GET های معمولی را ثبت کن
        if request.method != "GET":
            return

        path = request.path or ""

        # مسیرهای غیر ضروری را رد کن
        if path.startswith("/admin/"):
            return
        if path.startswith("/static/") or path.startswith("/media/"):
            return
        if path.startswith("/favicon") or path == "/robots.txt":
            return

        # فقط صفحات HTML (تقریباً) - بر اساس content_type
        content_type = response.headers.get("Content-Type", "")
        if content_type and not content_type.startswith("text/html"):
            return

        ip_address = self._get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        referrer = request.META.get("HTTP_REFERER", "")[:500]
        
        # تشخیص کشور بر اساس IP
        country = get_country_from_ip(ip_address) if ip_address else ""
        
        # تشخیص نوع دستگاه
        device_type = detect_device_type(user_agent) if user_agent else ""

        # مدیریت بازدیدکنندگان ناشناس
        anonymous_visitor = None
        user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
        
        if not user:
            # اگر کاربر لاگ این نکرده، از session_key برای شناسایی استفاده کن
            # اطمینان از وجود session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            if session_key:
                anonymous_visitor, created = AnonymousVisitor.objects.get_or_create(
                    session_key=session_key,
                    defaults={
                        "first_ip": ip_address or "",
                        "first_country": country,
                        "first_user_agent": user_agent,
                    }
                )
                # به‌روزرسانی اطلاعات آخرین بازدید
                if not created:
                    anonymous_visitor.last_ip = ip_address or ""
                    anonymous_visitor.last_country = country
                    anonymous_visitor.last_user_agent = user_agent
                    anonymous_visitor.save(update_fields=["last_ip", "last_country", "last_user_agent", "last_seen"])

        SiteVisit.objects.create(
            user=user,
            anonymous_visitor=anonymous_visitor,
            path=path,
            method=request.method,
            status_code=getattr(response, "status_code", 200),
            ip_address=ip_address or "",
            country=country,
            device_type=device_type,
            user_agent=user_agent,
            referrer=referrer,
            created_at=timezone.now(),
        )

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


