# 📝 راهنمای ایجاد فایل .env در هاست

فایل `.env` در `.gitignore` است و در repository نیست. باید در سرور (هاست) ایجاد شود.

---

## 🔍 محل فایل .env

فایل `.env` باید در **ریشه پروژه** (همان مسیری که `manage.py` است) قرار بگیرد.

**مسیر درست:**
```
/home/username/public_html/.env
# یا
/home/username/sami_deutsch/.env
```

---

## 🛠️ روش‌های ایجاد فایل .env در هاست

### روش 1: از طریق cPanel File Manager

1. **ورود به cPanel**
   - وارد cPanel شوید
   - به بخش **File Manager** بروید

2. **رفتن به مسیر پروژه**
   - به مسیر `public_html` یا مسیری که پروژه Django شماست بروید
   - مطمئن شوید که `manage.py` در این مسیر است

3. **ایجاد فایل جدید**
   - روی دکمه **+ File** کلیک کنید
   - نام فایل را `.env` بگذارید (با نقطه در ابتدا)
   - روی **Create New File** کلیک کنید

4. **ویرایش فایل**
   - روی فایل `.env` کلیک راست کنید
   - **Edit** را انتخاب کنید
   - محتوای زیر را کپی کنید و تنظیمات را تغییر دهید

---

### روش 2: از طریق Terminal/SSH

```bash
# رفتن به مسیر پروژه
cd ~/public_html
# یا
cd /home/username/public_html

# ایجاد فایل .env
nano .env
# یا
vi .env

# کپی کردن محتوا (در nano: Ctrl+Shift+V)
# ذخیره و خروج (در nano: Ctrl+X, سپس Y, سپس Enter)
```

---

### روش 3: از طریق Python App در cPanel

1. به **Python App** در cPanel بروید
2. **Terminal** را باز کنید
3. دستورات بالا را اجرا کنید

---

## 📋 محتوای فایل .env برای Production

فایل `.env` را با محتوای زیر ایجاد کنید و مقادیر را تغییر دهید:

```env
# ============================================
# CRITICAL SETTINGS - باید حتماً تنظیم شوند
# ============================================

# SECRET_KEY: حتماً یک کلید قوی و منحصر به فرد تولید کنید
SECRET_KEY=your-generated-secret-key-min-50-characters-here

# DEBUG: در production باید False باشد
DEBUG=False

# ALLOWED_HOSTS: فقط domain واقعی سایت شما
ALLOWED_HOSTS=samideutsch.ir,www.samideutsch.ir

# ============================================
# DATABASE SETTINGS
# ============================================

# برای MySQL/MariaDB:
DATABASE_URL=mysql://username_dbuser:password@localhost:3306/username_dbname

# یا برای PostgreSQL:
# DATABASE_URL=postgresql://username_dbuser:password@localhost:5432/username_dbname

# ============================================
# SECURITY SETTINGS (با HTTPS)
# ============================================

SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://samideutsch.ir,https://www.samideutsch.ir

# اگر از proxy استفاده می‌کنید (مثلاً Cloudflare):
# SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

# ============================================
# EMAIL SETTINGS (اختیاری)
# ============================================

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@samideutsch.ir
ADMIN_EMAIL=admin@samideutsch.ir
ADMIN_NAME=Admin

# ============================================
# STATIC & MEDIA FILES
# ============================================

STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=/home/username/public_html/staticfiles
MEDIA_ROOT=/home/username/public_html/media

# ============================================
# TIME ZONE
# ============================================

TIME_ZONE=Asia/Tehran

# ============================================
# ADMIN SETTINGS (اختیاری - برای امنیت بیشتر)
# ============================================

# تغییر URL admin (برای امنیت بیشتر)
ADMIN_URL=secret-admin-panel-2024/

# IP Whitelist برای admin (اگر IP ثابت دارید)
# ADMIN_IP_WHITELIST=your.ip.address.here

# ============================================
# OTHER SETTINGS
# ============================================

# Search (اگر از MeiliSearch استفاده می‌کنید)
MEILI_URL=http://127.0.0.1:7700
MEILI_API_KEY=

# Payments (اگر استفاده می‌کنید)
PAYMENT_HOST=samideutsch.ir
PAYMENT_USES_HTTPS=True
```

---

## 🔑 تولید SECRET_KEY

برای تولید `SECRET_KEY` قوی:

### روش 1: از طریق Terminal در هاست
```bash
cd ~/public_html
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### روش 2: از طریق Python App
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### روش 3: از طریق Python محلی
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ✅ بررسی صحت فایل .env

بعد از ایجاد فایل، بررسی کنید:

```bash
# بررسی وجود فایل
ls -la ~/public_html/.env

# بررسی محتوا (بدون نمایش کامل)
head -5 ~/public_html/.env

# بررسی دسترسی‌های فایل (باید 600 یا 644 باشد)
chmod 600 ~/public_html/.env
```

---

## 🔒 امنیت فایل .env

1. **دسترسی فایل:**
   ```bash
   chmod 600 .env  # فقط owner می‌تواند بخواند/بنویسد
   ```

2. **مطمئن شوید که در .gitignore است:**
   - فایل `.env` نباید در Git commit شود
   - بررسی کنید که در `.gitignore` است

3. **Backup:**
   - از فایل `.env` backup بگیرید
   - اما آن را در مکان امن نگه دارید

---

## 🐛 عیب‌یابی

### مشکل: فایل .env پیدا نمی‌شود

**بررسی کنید:**
1. آیا فایل در مسیر درست است؟ (همان مسیر `manage.py`)
2. آیا نام فایل دقیقاً `.env` است؟ (با نقطه در ابتدا)
3. آیا فایل hidden است؟ در File Manager گزینه "Show Hidden Files" را فعال کنید

### مشکل: تنظیمات اعمال نمی‌شوند

**بررسی کنید:**
1. آیا فایل `.env` در مسیر درست است؟
2. آیا syntax درست است؟ (بدون space قبل و بعد =)
3. آیا مقادیر درست هستند؟
4. آیا Django restart شده است؟

### مشکل: خطا در production

**بررسی کنید:**
1. آیا `SECRET_KEY` تنظیم شده است؟
2. آیا `DEBUG=False` است؟
3. آیا `ALLOWED_HOSTS` شامل domain واقعی است؟

---

## 📝 مثال کامل برای Production

```env
# تولید شده در: 2024
# برای: samideutsch.ir

SECRET_KEY=django-insecure-REPLACE-WITH-REAL-SECRET-KEY-MIN-50-CHARS-12345678901234567890
DEBUG=False
ALLOWED_HOSTS=samideutsch.ir,www.samideutsch.ir

DATABASE_URL=mysql://username_sami_user:STRONG_PASSWORD_HERE@localhost:3306/username_samideutsch

SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://samideutsch.ir,https://www.samideutsch.ir

STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=/home/username/public_html/staticfiles
MEDIA_ROOT=/home/username/public_html/media

TIME_ZONE=Asia/Tehran
ADMIN_URL=secret-admin-2024/
```

---

## 🎯 چک‌لیست

- [ ] فایل `.env` در مسیر ریشه پروژه ایجاد شد
- [ ] `SECRET_KEY` تولید و تنظیم شد
- [ ] `DEBUG=False` تنظیم شد
- [ ] `ALLOWED_HOSTS` شامل domain واقعی است
- [ ] `DATABASE_URL` صحیح است
- [ ] دسترسی فایل `600` است
- [ ] Django restart شده است

---

**نکته مهم:** بعد از ایجاد یا تغییر `.env`، حتماً Django را restart کنید!


