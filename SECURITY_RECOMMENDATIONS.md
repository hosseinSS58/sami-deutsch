# 🔒 پیشنهادات عملی برای بهبود امنیت سایت

این سند شامل پیشنهادات عملی و قابل اجرا برای بهبود امنیت سایت است.

---

## 🚨 اقدامات فوری (قبل از Production)

### 1. رفع مشکل CSRF در YouTubeClickView

**وضعیت فعلی:**
- JavaScript در حال ارسال CSRF token است (`X-CSRFToken`)
- اما view با `@csrf_exempt` محافظت نشده است

**راه‌حل پیشنهادی:**

```python
# در core/views.py
# حذف این خط:
# @method_decorator(csrf_exempt, name='dispatch')

class YouTubeClickView(View):
    """API endpoint برای ثبت کلیک‌های یوتیوب"""
    
    def post(self, request):
        # Django به صورت خودکار CSRF را بررسی می‌کند
        # چون JavaScript در حال ارسال token است، کار می‌کند
        # ...
```

**تغییرات لازم:**
1. حذف `@method_decorator(csrf_exempt, name='dispatch')` از `core/views.py`
2. حذف `from django.views.decorators.csrf import csrf_exempt` اگر استفاده نمی‌شود
3. تست کردن که tracking هنوز کار می‌کند

**اگر نیاز به csrf_exempt دارید (مثلاً برای external tracking):**
```python
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

@method_decorator(csrf_exempt, name='dispatch')
class YouTubeClickView(View):
    def post(self, request):
        # اضافه کردن rate limiting یا IP validation
        # برای جلوگیری از abuse
        # ...
```

---

### 2. تنظیم SECRET_KEY در Production

**اقدامات:**

1. **تولید SECRET_KEY جدید:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. **اضافه کردن به .env:**
```bash
SECRET_KEY=your-generated-secret-key-here-min-50-chars
```

3. **تغییر settings.py (اختیاری اما توصیه می‌شود):**
```python
# در sami/settings.py
SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
```

4. **مطمئن شوید .env در .gitignore است:**
```gitignore
# .gitignore
.env
*.env
```

---

### 3. تنظیم DEBUG=False در Production

**اقدامات:**

1. **در .env production:**
```bash
DEBUG=False
```

2. **بررسی error pages:**
- ✅ `templates/404.html` موجود است
- ✅ `templates/500.html` موجود است
- ✅ `templates/403.html` موجود است

3. **تست کردن:**
```python
# در settings.py موقتاً اضافه کنید برای تست:
if not DEBUG:
    # بررسی کنید که error pages نمایش داده می‌شوند
    pass
```

---

### 4. تنظیم ALLOWED_HOSTS

**در .env production:**
```bash
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**نکته:** اگر از subdomain استفاده می‌کنید، آن را هم اضافه کنید.

---

## ⚙️ تنظیمات Production (با HTTPS)

### 5. فعال کردن HTTPS Settings

**در .env production:**
```bash
# HTTPS Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS=31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# اگر از proxy استفاده می‌کنید (مثلاً Cloudflare):
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

---

## 🛡️ بهبودهای امنیتی پیشنهادی

### 6. اضافه کردن Rate Limiting برای Login

**نصب:**
```bash
pip install django-axes
```

**تنظیمات:**

1. **در settings.py:**
```python
INSTALLED_APPS = [
    # ...
    'axes',  # باید بعد از django.contrib.admin باشد
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # باید اول باشد
    'django.contrib.auth.backends.ModelBackend',
]

# تنظیمات axes
AXES_FAILURE_LIMIT = 5  # بعد از 5 تلاش ناموفق
AXES_COOLOFF_TIME = 1  # 1 ساعت block
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_LOCKOUT_TEMPLATE = 'accounts/locked_out.html'  # اختیاری
AXES_LOCKOUT_URL = '/accounts/locked/'  # اختیاری
AXES_VERBOSE = True  # برای debugging
```

2. **Migration:**
```bash
python manage.py migrate
```

3. **ایجاد template برای locked out (اختیاری):**
```html
<!-- templates/accounts/locked_out.html -->
{% extends "base.html" %}
{% block content %}
<div class="alert alert-danger">
    <h4>دسترسی موقتاً مسدود شده است</h4>
    <p>به دلیل تلاش‌های ناموفق متعدد، دسترسی شما به مدت 1 ساعت مسدود شده است.</p>
    <p>لطفاً بعداً تلاش کنید یا با پشتیبانی تماس بگیرید.</p>
</div>
{% endblock %}
```

---

### 7. تغییر Admin URL

**در .env:**
```bash
ADMIN_URL=secret-admin-panel-2024/
```

**نکته:** از یک URL غیرقابل حدس استفاده کنید، نه چیزی مثل `admin/` یا `manage/`

---

### 8. فعال کردن IP Whitelist برای Admin (اختیاری)

**اگر IP ثابت دارید:**

1. **در .env:**
```bash
ADMIN_IP_WHITELIST=your.ip.address.here,another.ip.address
```

2. **در settings.py:**
```python
ADMIN_IP_WHITELIST = env.list("ADMIN_IP_WHITELIST", default=[])
```

3. **در MIDDLEWARE (uncomment):**
```python
MIDDLEWARE = [
    # ...
    "sami.security_middleware.IPWhitelistMiddleware",  # uncomment این خط
]
```

**نکته:** اگر IP شما تغییر می‌کند (مثلاً dynamic IP)، این را فعال نکنید.

---

### 9. اضافه کردن Content Security Policy (CSP)

**نصب:**
```bash
pip install django-csp
```

**تنظیمات:**

1. **در settings.py:**
```python
INSTALLED_APPS = [
    # ...
    'csp',
]

MIDDLEWARE = [
    # ...
    'csp.middleware.CSPMiddleware',  # بعد از SecurityMiddleware
]

# CSP Settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",  # اگر inline scripts دارید
    "https://www.youtube.com",
    "https://cdn.jsdelivr.net",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",  # اگر inline styles دارید
    "https://cdn.jsdelivr.net",
)
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https://cdn.jsdelivr.net")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'self'", "https://www.youtube.com")
```

**نکته:** CSP ممکن است برخی scripts را block کند. بعد از اضافه کردن، سایت را کامل تست کنید.

---

### 10. بهبود Security Headers

**در sami/security_middleware.py:**

```python
class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Headers موجود
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = getattr(settings, "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")
        
        # Headers جدید
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # HSTS (اگر HTTPS دارید)
        if request.is_secure():
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        # Remove server information
        if "Server" in response:
            del response["Server"]
        if "X-Powered-By" in response:
            del response["X-Powered-By"]
        
        return response
```

---

## 📊 Monitoring و Logging

### 11. بررسی لاگ‌های امنیتی

**فایل‌های لاگ:**
- `logs/django.log` - لاگ‌های عمومی
- `logs/security.log` - رویدادهای امنیتی

**چیزهایی که باید مانیتور کنید:**
- Failed login attempts (در security.log)
- Unusual IP addresses
- Error rates
- Admin access attempts

**پیشنهاد:** استفاده از Sentry برای error tracking:
```bash
pip install sentry-sdk
```

```python
# در settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn="your-sentry-dsn",
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False  # برای حفظ حریم خصوصی
    )
```

---

## 🔐 بهبودهای پیشرفته (اختیاری)

### 12. Two-Factor Authentication (2FA)

**نصب:**
```bash
pip install django-otp django-otp[qr]
```

**تنظیمات:**
```python
INSTALLED_APPS = [
    # ...
    'django_otp',
    'django_otp.plugins.otp_totp',
]

MIDDLEWARE = [
    # ...
    'django_otp.middleware.OTPMiddleware',
]

# فقط برای admin users
OTP_TOTP_ISSUER = "Sami Deutsch"
```

---

### 13. Dependency Security Scanning

**نصب:**
```bash
pip install safety pip-audit
```

**استفاده:**
```bash
# بررسی vulnerabilities
safety check
pip-audit
```

**پیشنهاد:** اضافه کردن به CI/CD pipeline

---

## 📝 چک‌لیست نهایی

قبل از production، این موارد را بررسی کنید:

- [ ] SECRET_KEY در .env تنظیم شده و قوی است
- [ ] DEBUG=False در production
- [ ] ALLOWED_HOSTS فقط domain واقعی
- [ ] HTTPS settings فعال شده‌اند
- [ ] CSRF exempt از YouTubeClickView حذف شده
- [ ] Error pages (404, 500, 403) تست شده‌اند
- [ ] .env در .gitignore است
- [ ] Database password قوی است
- [ ] Rate limiting برای login اضافه شده (اختیاری)
- [ ] Admin URL تغییر کرده (اختیاری)
- [ ] IP whitelist برای admin فعال شده (اگر IP ثابت دارید)
- [ ] CSP headers اضافه شده (اختیاری)
- [ ] Logging و monitoring تنظیم شده
- [ ] Backup strategy تعریف شده

---

## 🎯 اولویت‌بندی

### فوری (قبل از Production):
1. ✅ رفع CSRF exempt
2. ✅ تنظیم SECRET_KEY
3. ✅ تنظیم DEBUG=False
4. ✅ تنظیم ALLOWED_HOSTS

### مهم (در Production):
5. ✅ فعال کردن HTTPS settings
6. ✅ اضافه کردن rate limiting
7. ✅ تغییر Admin URL

### پیشنهادی (بهبودهای آینده):
8. 💡 CSP headers
9. 💡 2FA
10. 💡 Monitoring tools

---

**نکته:** این پیشنهادات را به تدریج اعمال کنید و بعد از هر تغییر، سایت را کامل تست کنید.
