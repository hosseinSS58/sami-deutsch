# 🔒 گزارش جامع بررسی امنیتی سایت Sami Deutsch

**تاریخ بررسی:** 2024  
**نسخه Django:** 5.1.11  
**وضعیت کلی:** ⚠️ نیاز به بهبود در برخی بخش‌ها

---

## 📊 خلاصه اجرایی

این گزارش شامل بررسی کامل امنیتی سایت و ارزیابی وضعیت فعلی است. سایت از نظر امنیتی در وضعیت **متوسط** قرار دارد و برخی تنظیمات امنیتی خوب پیاده‌سازی شده‌اند، اما موارد مهمی نیاز به توجه دارند.

### آمار کلی:
- ✅ **15+ تنظیمات امنیتی** پیاده‌سازی شده
- ⚠️ **3 مشکل بحرانی** شناسایی شده
- ⚠️ **5 مشکل متوسط** شناسایی شده
- 💡 **8 پیشنهاد بهبود** ارائه شده

---

## ✅ نقاط قوت امنیتی

### 1. **محافظت در برابر CSRF**
- ✅ `CsrfViewMiddleware` فعال است
- ✅ تمام فرم‌ها از `{% csrf_token %}` استفاده می‌کنند
- ✅ CSRF cookies با `HttpOnly` و `SameSite` محافظت می‌شوند
- ⚠️ **استثنا:** یک view با `@csrf_exempt` وجود دارد (نیاز به بررسی)

### 2. **امنیت رمز عبور**
- ✅ Password validators فعال هستند:
  - UserAttributeSimilarityValidator
  - MinimumLengthValidator
  - CommonPasswordValidator
  - NumericPasswordValidator
- ✅ Password hashers بهینه شده‌اند (Argon2 اولویت دارد)
- ✅ Password reset functionality موجود است
- ✅ Password reset timeout تنظیم شده (24 ساعت)

### 3. **محافظت در برابر SQL Injection**
- ✅ استفاده از Django ORM (بدون raw SQL queries)
- ✅ تمام queries از parameterized queries استفاده می‌کنند
- ✅ User input در queries به درستی sanitize می‌شود
- ✅ هیچ استفاده‌ای از `.raw()` یا `cursor.execute()` یافت نشد

### 4. **محافظت در برابر XSS**
- ✅ Django templates به صورت پیش‌فرض HTML را escape می‌کنند
- ✅ Security headers برای XSS protection فعال شده‌اند
- ✅ `SECURE_BROWSER_XSS_FILTER = True`
- ✅ `X-Content-Type-Options: nosniff`

### 5. **Session Security**
- ✅ `SESSION_COOKIE_HTTPONLY = True`
- ✅ `SESSION_COOKIE_SAMESITE = "Lax"`
- ✅ `SESSION_SAVE_EVERY_REQUEST = True` (جلوگیری از session fixation)
- ✅ `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- ✅ Session regeneration middleware پیاده‌سازی شده

### 6. **File Upload Security**
- ✅ Validation اندازه فایل (max 2MB برای avatar)
- ✅ Validation نوع فایل (JPEG, PNG, WebP)
- ✅ بررسی معتبر بودن تصویر با PIL
- ✅ محدودیت کلی فایل‌ها (5MB)

### 7. **Logging & Monitoring**
- ✅ Security logging middleware پیاده‌سازی شده
- ✅ ثبت login/logout events
- ✅ ثبت failed login attempts
- ✅ ثبت IP address در تمام رویدادها
- ✅ فیلتر کردن اطلاعات حساس در لاگ‌ها

### 8. **Authorization & Access Control**
- ✅ استفاده از `LoginRequiredMixin` در views حساس
- ✅ بررسی دسترسی admin در `AdminDashboardView`
- ✅ Admin URL customization امکان‌پذیر است

---

## 🔴 مشکلات بحرانی (Critical)

### 1. **SECRET_KEY با Default Value**
**مکان:** `sami/settings.py:31`

**مشکل:**
```python
SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-secret-key")
```

**ریسک:**
- اگر `SECRET_KEY` در `.env` تنظیم نشود، از مقدار پیش‌فرض استفاده می‌شود
- این مقدار در کد منبع قابل مشاهده است
- در production خطرناک است

**راه‌حل:**
```python
# در production حتماً باید SECRET_KEY تنظیم شود
SECRET_KEY = env("SECRET_KEY")  # بدون default
# یا
SECRET_KEY = env("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")
```

**اقدام فوری:**
- ✅ بررسی کنید که `.env` در production حتماً `SECRET_KEY` دارد
- ✅ از `get_random_secret_key()` برای تولید استفاده کنید
- ✅ مطمئن شوید `.env` در git commit نمی‌شود

---

### 2. **DEBUG Mode در Production**
**مکان:** `sami/settings.py:34`

**مشکل:**
```python
DEBUG = env("DEBUG", default=True)
```

**ریسک:**
- اگر `DEBUG=True` در production باشد:
  - اطلاعات حساس در error pages نمایش داده می‌شود
  - Stack traces کامل قابل مشاهده است
  - اطلاعات database schema قابل دسترسی است

**راه‌حل:**
```python
DEBUG = env.bool("DEBUG", default=False)  # پیش‌فرض False
```

**اقدام فوری:**
- ✅ در `.env` production حتماً `DEBUG=False` تنظیم کنید
- ✅ Error pages سفارشی (404.html, 500.html, 403.html) را بررسی کنید

---

### 3. **CSRF Exempt در API Endpoint**
**مکان:** `core/views.py:213`

**مشکل:**
```python
@method_decorator(csrf_exempt, name='dispatch')
class YouTubeClickView(View):
```

**ریسک:**
- این endpoint بدون CSRF protection است
- امکان CSRF attack وجود دارد
- هر سایتی می‌تواند به این endpoint درخواست بفرستد

**راه‌حل‌های پیشنهادی:**

**گزینه 1: استفاده از CSRF token در JavaScript**
```python
# حذف csrf_exempt
# در JavaScript از CSRF token استفاده کنید
```

**گزینه 2: استفاده از API Key یا Token**
```python
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hashlib

@method_decorator(csrf_exempt, name='dispatch')
class YouTubeClickView(View):
    def post(self, request):
        # بررسی API key یا token
        api_key = request.headers.get('X-API-Key')
        if not self.validate_api_key(api_key):
            return JsonResponse({"error": "Unauthorized"}, status=401)
        # ...
```

**گزینه 3: استفاده از Django REST Framework**
- استفاده از DRF با authentication مناسب

**اقدام فوری:**
- ⚠️ تصمیم بگیرید که آیا این endpoint باید public باشد یا نه
- اگر public است، از API key یا rate limiting استفاده کنید
- اگر فقط برای سایت خودتان است، CSRF exempt را حذف کنید

---

## 🟡 مشکلات متوسط (Medium Priority)

### 4. **HTTPS Settings در Production**
**مکان:** `sami/settings.py:221-227`

**وضعیت فعلی:**
```python
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
```

**مشکل:**
- در production با HTTPS باید این تنظیمات `True` باشند
- در حال حاضر پیش‌فرض `False` است

**راه‌حل:**
```python
# در .env production:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**اقدام:**
- ✅ در production با HTTPS حتماً این تنظیمات را فعال کنید

---

### 5. **ALLOWED_HOSTS Configuration**
**مکان:** `sami/settings.py:36`

**وضعیت فعلی:**
```python
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "192.168.1.104"])
```

**مشکل:**
- در production باید فقط domain واقعی سایت باشد
- IP address محلی نباید در production باشد

**راه‌حل:**
```python
# در .env production:
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**اقدام:**
- ✅ در production فقط domain واقعی را اضافه کنید

---

### 6. **Rate Limiting برای Login**
**مشکل:**
- هیچ rate limiting برای login attempts وجود ندارد
- امکان brute force attack وجود دارد

**راه‌حل:**
استفاده از `django-ratelimit` یا `django-axes`:

```python
# نصب: pip install django-axes

# در settings.py:
INSTALLED_APPS = [
    # ...
    'axes',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # باید اول باشد
    'django.contrib.auth.backends.ModelBackend',
]

# تنظیمات axes:
AXES_FAILURE_LIMIT = 5  # بعد از 5 تلاش ناموفق
AXES_COOLOFF_TIME = 1  # 1 ساعت block
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
```

**اقدام:**
- 💡 پیشنهاد می‌شود `django-axes` را اضافه کنید

---

### 7. **Content Security Policy (CSP)**
**مشکل:**
- هیچ CSP header تنظیم نشده است
- امکان XSS attack از طریق inline scripts وجود دارد

**راه‌حل:**
استفاده از `django-csp`:

```python
# نصب: pip install django-csp

# در settings.py:
MIDDLEWARE = [
    # ...
    'csp.middleware.CSPMiddleware',
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://www.youtube.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
```

**اقدام:**
- 💡 پیشنهاد می‌شود CSP را اضافه کنید (با احتیاط - ممکن است برخی scripts را block کند)

---

### 8. **Admin Security**
**وضعیت:**
- Admin URL customization امکان‌پذیر است اما پیش‌فرض `/admin/` است
- IP whitelist middleware موجود است اما غیرفعال است
- SecureAdminSite تعریف شده اما استفاده نشده

**بهبودهای پیشنهادی:**

**1. تغییر Admin URL:**
```python
# در .env:
ADMIN_URL=secret-admin-panel-2024/
```

**2. فعال کردن IP Whitelist (اختیاری):**
```python
# در settings.py:
ADMIN_IP_WHITELIST = env.list("ADMIN_IP_WHITELIST", default=[])

# در MIDDLEWARE:
"sami.security_middleware.IPWhitelistMiddleware",  # uncomment
```

**3. استفاده از SecureAdminSite:**
```python
# در sami/admin_security.py:
admin_site = SecureAdminSite(name="secure_admin")

# در urls.py:
from sami.admin_security import admin_site
urlpatterns = [
    path(settings.ADMIN_URL, admin_site.urls),
    # ...
]
```

**اقدام:**
- 💡 پیشنهاد می‌شود Admin URL را تغییر دهید
- 💡 اگر IP ثابت دارید، IP whitelist را فعال کنید

---

## 🟢 بهبودهای پیشنهادی (Low Priority)

### 9. **Two-Factor Authentication (2FA)**
**پیشنهاد:**
- اضافه کردن 2FA برای admin users
- استفاده از `django-otp` یا `django-two-factor-auth`

### 10. **Security Headers اضافی**
**پیشنهاد:**
```python
# در SecurityHeadersMiddleware:
response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
```

### 11. **Input Validation اضافی**
**وضعیت:**
- ✅ Form validation خوب است
- 💡 پیشنهاد: اضافه کردن validation برای URL fields

### 12. **Database Security**
**پیشنهاد:**
- استفاده از connection pooling
- تنظیم timeout برای database connections
- Backup encryption

### 13. **Email Security**
**پیشنهاد:**
- استفاده از TLS/SSL برای email
- تنظیم `EMAIL_USE_TLS = True`
- استفاده از App Password برای Gmail

### 14. **Monitoring & Alerting**
**پیشنهاد:**
- اضافه کردن monitoring برای:
  - Failed login attempts
  - Unusual traffic patterns
  - Error rates
- استفاده از Sentry یا similar tools

### 15. **Dependency Security**
**پیشنهاد:**
- استفاده از `safety` یا `pip-audit` برای بررسی vulnerabilities
- به‌روزرسانی منظم dependencies
- استفاده از `django-upgrade` برای به‌روزرسانی Django

### 16. **API Security (اگر API دارید)**
**پیشنهاد:**
- استفاده از Django REST Framework
- اضافه کردن authentication (Token, JWT)
- Rate limiting برای API endpoints

---

## 📋 چک‌لیست Production Deployment

قبل از deploy به production، این موارد را بررسی کنید:

### Environment Variables (.env)
```bash
# Critical - باید تنظیم شوند:
SECRET_KEY=your-super-secret-key-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security - برای HTTPS:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database:
DATABASE_URL=postgresql://user:password@localhost/dbname

# Email (اگر استفاده می‌کنید):
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Admin (اختیاری):
ADMIN_URL=secret-admin-url/
ADMIN_IP_WHITELIST=your.ip.address.here
```

### Security Checklist
- [ ] `SECRET_KEY` قوی و منحصر به فرد تولید شده
- [ ] `DEBUG=False` در production
- [ ] `ALLOWED_HOSTS` فقط domain واقعی
- [ ] HTTPS فعال و تنظیمات SSL درست است
- [ ] `.env` در `.gitignore` است و commit نمی‌شود
- [ ] Database password قوی است
- [ ] Error pages سفارشی (404, 500, 403) تست شده‌اند
- [ ] Media files فقط در DEBUG mode serve نمی‌شوند
- [ ] Logging تنظیم شده و لاگ‌ها بررسی می‌شوند
- [ ] Backup strategy تعریف شده است

---

## 🎯 اولویت‌بندی اقدامات

### فوری (قبل از Production):
1. ✅ تنظیم `SECRET_KEY` در `.env`
2. ✅ تنظیم `DEBUG=False` در production
3. ✅ بررسی و حل مشکل `csrf_exempt` در `YouTubeClickView`
4. ✅ تنظیم `ALLOWED_HOSTS` فقط domain واقعی

### مهم (در Production):
5. ✅ فعال کردن HTTPS settings
6. ✅ اضافه کردن rate limiting برای login
7. ✅ تغییر Admin URL
8. ✅ تست error pages

### پیشنهادی (بهبودهای آینده):
9. 💡 اضافه کردن CSP headers
10. 💡 اضافه کردن 2FA برای admin
11. 💡 اضافه کردن monitoring و alerting
12. 💡 به‌روزرسانی منظم dependencies

---

## 📚 منابع و مستندات

- [Django Security Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/5.1/topics/security/)

---

## 📝 نتیجه‌گیری

سایت شما از نظر امنیتی در وضعیت **متوسط به خوب** قرار دارد. بسیاری از تنظیمات امنیتی پایه پیاده‌سازی شده‌اند، اما **3 مشکل بحرانی** وجود دارد که باید قبل از production حل شوند.

**نمره امنیتی فعلی: 7/10**

با رعایت موارد بحرانی و متوسط، می‌توانید به **9/10** برسید.

---

**تهیه شده توسط:** Security Audit System  
**تاریخ:** 2024


