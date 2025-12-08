# 🔒 گزارش بررسی امنیتی settings.py

**تاریخ بررسی:** 2024  
**فایل:** `sami/settings.py`

---

## 📊 خلاصه اجرایی

این گزارش شامل بررسی کامل فایل `settings.py` از نظر امنیتی است. برخی تنظیمات خوب هستند اما **3 مشکل بحرانی** و **5 مشکل متوسط** شناسایی شده است.

---

## 🔴 مشکلات بحرانی (Critical)

### 1. **SECRET_KEY با Default Value**
**خط:** 31

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
# گزینه 1: بدون default (بهتر است)
SECRET_KEY = env("SECRET_KEY")

# گزینه 2: با validation
SECRET_KEY = env("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")

# گزینه 3: فقط در development default داشته باشد
if DEBUG:
    SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-secret-key")
else:
    SECRET_KEY = env("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
```

---

### 2. **DEBUG با Default=True**
**خط:** 34

**مشکل:**
```python
DEBUG = env("DEBUG", default=True)
```

**ریسک:**
- اگر `DEBUG` در `.env` تنظیم نشود، به صورت پیش‌فرض `True` است
- در production خطرناک است - اطلاعات حساس نمایش داده می‌شود

**راه‌حل:**
```python
# گزینه 1: پیش‌فرض False (بهتر است)
DEBUG = env.bool("DEBUG", default=False)

# گزینه 2: با validation
DEBUG = env.bool("DEBUG", default=False)
if DEBUG and not env("ALLOWED_HOSTS"):
    import warnings
    warnings.warn("DEBUG=True without ALLOWED_HOSTS is dangerous!")
```

---

### 3. **ALLOWED_HOSTS شامل IP محلی**
**خط:** 36

**مشکل:**
```python
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "192.168.1.104"])
```

**ریسک:**
- IP محلی (`192.168.1.104`) در default است
- در production باید فقط domain واقعی باشد
- این IP ممکن است تغییر کند

**راه‌حل:**
```python
# گزینه 1: فقط localhost در development
if DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
else:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
    if not ALLOWED_HOSTS:
        raise ValueError("ALLOWED_HOSTS must be set in production")

# گزینه 2: بدون IP محلی در default
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
```

---

## 🟡 مشکلات متوسط (Medium Priority)

### 4. **Email Backend بدون تنظیمات**
**خط:** 205-208

**مشکل:**
```python
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
```

**ریسک:**
- در production باید SMTP backend استفاده شود
- تنظیمات EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS وجود ندارد

**راه‌حل:**
```python
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)

# اضافه کردن تنظیمات SMTP
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@samideutsch.ir")
```

---

### 5. **Database URL بدون Validation**
**خط:** 108-113

**مشکل:**
```python
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}
```

**ریسک:**
- در production نباید از SQLite استفاده شود
- بهتر است validation اضافه شود

**راه‌حل:**
```python
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}" if DEBUG else None,
    )
}

# Validation برای production
if not DEBUG:
    db_url = DATABASES["default"]["NAME"] if "NAME" in DATABASES["default"] else None
    if not db_url or "sqlite" in str(db_url).lower():
        raise ValueError("SQLite database is not allowed in production")
```

---

### 6. **Logging بدون Email Configuration**
**خط:** 315-319

**مشکل:**
```python
"mail_admins": {
    "level": "ERROR",
    "filters": ["require_debug_false"],
    "class": "django.utils.log.AdminEmailHandler",
},
```

**ریسک:**
- `ADMINS` تنظیم نشده است
- Email backend ممکن است کار نکند

**راه‌حل:**
```python
# اضافه کردن در settings.py
ADMINS = [
    ("Admin Name", "admin@example.com"),
]

# یا از env:
ADMINS = [
    (env("ADMIN_NAME", default="Admin"), env("ADMIN_EMAIL", default="admin@example.com")),
]
```

---

### 7. **Media Files در DEBUG Mode Serve می‌شوند**
**خط:** 152-153

**مشکل:**
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

**ریسک:**
- در `urls.py` ممکن است media files در production serve شوند
- باید از web server (nginx/apache) استفاده شود

**نکته:** بررسی کنید که در `urls.py`:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### 8. **Password Validators بدون Minimum Length**
**خط:** 119-132

**وضعیت:** خوب است اما می‌تواند بهتر شود.

**بهبود:**
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,  # اضافه کردن minimum length
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
```

---

## 🟢 بهبودهای پیشنهادی (Low Priority)

### 9. **CORS Settings (اگر API دارید)**
اگر API دارید، باید CORS تنظیم شود:
```python
INSTALLED_APPS = [
    # ...
    "corsheaders",  # اگر نیاز دارید
]

MIDDLEWARE = [
    # ...
    "corsheaders.middleware.CorsMiddleware",  # باید قبل CommonMiddleware باشد
]

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
```

---

### 10. **Cache Configuration**
اضافه کردن cache configuration:
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"),
    }
}
```

---

### 11. **File Upload Permissions**
اضافه کردن تنظیمات permissions:
```python
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
```

---

### 12. **Session Engine**
اگر از Redis استفاده می‌کنید:
```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

---

## 📋 چک‌لیست اقدامات

### فوری (Critical):
- [ ] رفع SECRET_KEY default value
- [ ] رفع DEBUG default=True
- [ ] رفع ALLOWED_HOSTS شامل IP محلی

### مهم (Medium):
- [ ] اضافه کردن Email settings
- [ ] اضافه کردن Database validation
- [ ] اضافه کردن ADMINS برای logging
- [ ] بررسی Media files serving

### پیشنهادی (Low):
- [ ] اضافه کردن CORS اگر نیاز است
- [ ] اضافه کردن Cache configuration
- [ ] اضافه کردن File permissions

---

## 🎯 اولویت‌بندی

### امروز:
1. رفع SECRET_KEY
2. رفع DEBUG
3. رفع ALLOWED_HOSTS

### این هفته:
4. اضافه کردن Email settings
5. اضافه کردن Database validation
6. اضافه کردن ADMINS

---

## 📝 کدهای پیشنهادی برای رفع مشکلات

### رفع مشکلات بحرانی:
```python
# در settings.py

# 1. SECRET_KEY
SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY and not DEBUG:
    raise ValueError("SECRET_KEY must be set in production")

# 2. DEBUG
DEBUG = env.bool("DEBUG", default=False)

# 3. ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
else:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
    if not ALLOWED_HOSTS:
        raise ValueError("ALLOWED_HOSTS must be set in production")
```

---

**نمره امنیتی settings.py:** 7/10  
**بعد از رفع مشکلات بحرانی:** 9/10
