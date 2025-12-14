# 🔧 راه‌حل: استفاده از Subdirectory برای Python App در cPanel

اگر cPanel اجازه استفاده از `public_html` را نمی‌دهد، باید از subdirectory استفاده کنید.

---

## 🎯 راه‌حل: ایجاد پوشه جداگانه

### مرحله 1: ایجاد پوشه جدید

```bash
# در Terminal cPanel
cd ~/public_html
mkdir django_app
```

---

### مرحله 2: انتقال فایل‌ها به پوشه جدید

**گزینه A: اگر فایل‌ها از GitHub clone شده:**

```bash
cd ~/public_html

# اگر از GitHub clone کرده‌اید و همه چیز در public_html است:
# ایجاد پوشه جدید
mkdir django_app

# انتقال فایل‌ها (به جز .htaccess و فایل‌های دیگر)
mv manage.py passenger_wsgi.py requirements.txt django_app/
mv sami accounts courses blog shop search assessments core siteconfig django_app/
mv templates static django_app/

# اگر media و staticfiles دارید:
# mv media staticfiles django_app/  # فقط اگر می‌خواهید
```

**گزینه B: اگر می‌خواهید دوباره از GitHub clone کنید:**

```bash
cd ~/public_html
mkdir django_app
cd django_app
git clone https://github.com/hosseinSS58/sami-deutsch.git .
# نقطه (.) در انتها یعنی clone در همین پوشه
```

---

### مرحله 3: ایجاد فایل `.htaccess` در `public_html`

برای اینکه سایت در root domain اجرا شود، باید `.htaccess` ایجاد کنید:

```bash
cd ~/public_html
nano .htaccess
```

**محتوای `.htaccess`:**

```apache
# Redirect all requests to django_app
RewriteEngine On
RewriteCond %{REQUEST_URI} !^/django_app/
RewriteRule ^(.*)$ /django_app/$1 [L]

# یا اگر می‌خواهید همه چیز به passenger_wsgi.py برود:
# PassengerEnabled On
# PassengerAppRoot /home/username/public_html/django_app
# PassengerBaseURI /
```

**نکته:** این روش ممکن است با Passenger تداخل داشته باشد. بهتر است از روش زیر استفاده کنید.

---

### مرحله 4: تنظیمات Python App

در cPanel:

| فیلد | مقدار |
|------|-------|
| **Python version** | `Python 3.10` |
| **Application root** | `/home/username/public_html/django_app` |
| **Application URL** | `/` |
| **Application startup file** | `passenger_wsgi.py` |
| **Application Entry point** | `application` |
| **Passenger log file** | `/home/username/logs/passenger.log` |

**نکته:** `username` را با username cPanel خود جایگزین کنید.

---

## 🔄 روش بهتر: استفاده از Symbolic Link

اگر می‌خواهید فایل‌ها در `public_html` بمانند اما Python App در subdirectory باشد:

```bash
# ایجاد پوشه برای Python App
cd ~
mkdir python_apps
cd python_apps
mkdir sami_deutsch

# ایجاد symbolic link به فایل‌های اصلی
cd sami_deutsch
ln -s ~/public_html/manage.py .
ln -s ~/public_html/passenger_wsgi.py .
ln -s ~/public_html/requirements.txt .
ln -s ~/public_html/sami .
ln -s ~/public_html/accounts .
# و بقیه پوشه‌ها...
```

سپس در Python App:
- **Application root:** `/home/username/python_apps/sami_deutsch`

---

## ✅ روش توصیه شده: ساختار ساده

### ساختار پیشنهادی:

```
~/public_html/
├── .htaccess (برای redirect)
├── index.html (اختیاری - برای تست)
└── django_app/
    ├── manage.py
    ├── passenger_wsgi.py
    ├── requirements.txt
    ├── .env
    ├── sami/
    ├── accounts/
    ├── templates/
    ├── static/
    └── ...
```

### تنظیمات Python App:

- **Application root:** `/home/username/public_html/django_app`
- **Application URL:** `/` (یا `/django_app` اگر می‌خواهید در subdirectory اجرا شود)

---

## 🔧 تنظیمات `.htaccess` برای Root Domain

اگر می‌خواهید سایت در `yourdomain.com` اجرا شود (نه `yourdomain.com/django_app`):

```bash
cd ~/public_html
nano .htaccess
```

**محتوای `.htaccess`:**

```apache
# Enable Passenger
PassengerEnabled On
PassengerAppRoot /home/username/public_html/django_app
PassengerBaseURI /
PassengerPython /home/username/virtualenv/public_html/3.10/bin/python

# Redirect all to django_app
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /django_app/$1 [L]
```

**نکته:** این تنظیمات ممکن است با Passenger تداخل داشته باشد. بهتر است از Passenger به صورت مستقیم استفاده کنید.

---

## 🎯 روش نهایی: استفاده مستقیم از Passenger

اگر cPanel از Passenger پشتیبانی می‌کند:

1. فایل‌ها را در `public_html/django_app` قرار دهید
2. در Python App:
   - **Application root:** `/home/username/public_html/django_app`
   - **Application URL:** `/`
3. Passenger به صورت خودکار درخواست‌ها را به `django_app` هدایت می‌کند

---

## 📝 چک‌لیست

- [ ] پوشه `django_app` در `public_html` ایجاد شده
- [ ] فایل‌های پروژه به `django_app` منتقل شده
- [ ] `passenger_wsgi.py` در `django_app` موجود است
- [ ] Python App با Application root صحیح ایجاد شده
- [ ] Virtual environment فعال است
- [ ] Dependencies نصب شده

---

## 🐛 مشکلات احتمالی

### مشکل: "Application not found"

**راه‌حل:**
- مطمئن شوید که `passenger_wsgi.py` در Application root است
- مسیر را دوباره بررسی کنید

### مشکل: "Static files not loading"

**راه‌حل:**
- مطمئن شوید که `STATIC_ROOT` و `MEDIA_ROOT` در `.env` درست تنظیم شده
- `collectstatic` را اجرا کنید

---

**موفق باشید! 🎉**

اگر هنوز مشکل دارید، بگویید چه خطایی می‌گیرید.











