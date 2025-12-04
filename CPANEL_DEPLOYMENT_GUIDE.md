# 🚀 راهنمای کامل Deploy Django روی cPanel

این راهنما گام‌به‌گام نحوه deploy کردن سایت Sami Deutsch روی هاست cPanel را توضیح می‌دهد.

---

## 📋 پیش‌نیازها

### 1. **نیازمندی‌های cPanel**
- ✅ هاست لینوکسی با cPanel
- ✅ Python 3.8+ (معمولاً در cPanel از طریق Setup Python App در دسترس است)
- ✅ دسترسی به File Manager یا FTP
- ✅ دسترسی به MySQL/MariaDB یا PostgreSQL (از طریق phpMyAdmin یا Database section)
- ✅ Domain name متصل به هاست

### 2. **بررسی Python در cPanel**
1. وارد cPanel شوید
2. به بخش **"Setup Python App"** یا **"Python Selector"** بروید
3. نسخه Python را بررسی کنید (باید 3.8+ باشد)
4. اگر Python App ندارید، از **"Setup Python App"** یک اپلیکیشن جدید ایجاد کنید

---

## 🔧 مرحله 1: آماده‌سازی فایل‌ها

### 1.1. فشرده‌سازی پروژه

در کامپیوتر خودتان:

```bash
# فایل‌های غیرضروری را حذف کنید
# .git, __pycache__, *.pyc, venv, db.sqlite3 و ...
```

**فایل‌های که باید حذف شوند:**
- `.git/` (اگر می‌خواهید)
- `__pycache__/`
- `*.pyc`
- `venv/` یا `env/`
- `db.sqlite3` (اگر دارید)
- `.env` (بعداً در سرور ایجاد می‌کنیم)
- `logs/` (اگر دارید)

**فایل‌های ضروری:**
- تمام فایل‌های `.py`
- `requirements.txt`
- `manage.py`
- `templates/`
- `static/`
- `media/` (اگر محتوا دارید)

### 1.2. ایجاد فایل `passenger_wsgi.py`

در ریشه پروژه، فایل `passenger_wsgi.py` ایجاد کنید (این فایل برای cPanel ضروری است):

```python
import os
import sys
import django

# مسیر پروژه را اضافه کنید
sys.path.insert(0, os.path.dirname(__file__))

# تنظیمات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sami.settings')

# راه‌اندازی Django
django.setup()

# Import WSGI application
from sami.wsgi import application

# Passenger به این متغیر نیاز دارد
application = application
```

### 1.3. ایجاد فایل `.htaccess` (اختیاری)

اگر از Apache استفاده می‌کنید، فایل `.htaccess` در ریشه پروژه:

```apache
# Redirect to passenger_wsgi.py
PassengerEnabled On
PassengerAppRoot /home/username/public_html
PassengerBaseURI /
PassengerPython /home/username/virtualenv/public_html/3.8/bin/python
```

**نکته:** مسیرها را با اطلاعات واقعی cPanel خود جایگزین کنید.

---

## 📤 مرحله 2: آپلود فایل‌ها به سرور

### 2.1. آپلود از طریق File Manager

1. وارد cPanel شوید
2. به **File Manager** بروید
3. به پوشه `public_html` یا `public_html/yourdomain.com` بروید
4. تمام فایل‌های پروژه را آپلود کنید

**ساختار پیشنهادی:**
```
public_html/
├── manage.py
├── passenger_wsgi.py
├── .htaccess
├── requirements.txt
├── .env
├── sami/
├── accounts/
├── courses/
├── templates/
├── static/
└── media/
```

### 2.2. آپلود از طریق FTP

اگر از FTP استفاده می‌کنید:
- Host: `ftp.yourdomain.com` یا IP سرور
- Username: username cPanel شما
- Password: password cPanel شما
- Port: 21

---

## 🐍 مرحله 3: تنظیمات Python در cPanel

### 3.1. ایجاد Python App

1. در cPanel به **"Setup Python App"** بروید
2. روی **"Create Application"** کلیک کنید
3. تنظیمات را وارد کنید:
   - **Python Version:** آخرین نسخه موجود (3.8+)
   - **App Directory:** `public_html` یا مسیر پروژه شما
   - **App URL:** `/` (یا مسیر دلخواه)
   - **Application Startup File:** `passenger_wsgi.py`
   - **Application Entry Point:** `application`
4. روی **"Create"** کلیک کنید

### 3.2. فعال‌سازی Virtual Environment

cPanel معمولاً به صورت خودکار virtual environment ایجاد می‌کند. مسیر آن معمولاً:
```
/home/username/virtualenv/public_html/3.8/
```

یا در تنظیمات Python App می‌توانید ببینید.

---

## 📦 مرحله 4: نصب Dependencies

### 4.1. از طریق Terminal (SSH)

اگر دسترسی SSH دارید:

```bash
# وارد دایرکتوری پروژه شوید
cd ~/public_html

# فعال‌سازی virtual environment
source ~/virtualenv/public_html/3.8/bin/activate

# نصب dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.2. از طریق cPanel Terminal

1. در cPanel به **"Terminal"** بروید
2. دستورات بالا را اجرا کنید

### 4.3. از طریق Python App در cPanel

در صفحه Python App:
1. روی **"Run Pip Install"** کلیک کنید
2. نام پکیج‌ها را وارد کنید یا از `requirements.txt` استفاده کنید

---

## 🗄️ مرحله 5: تنظیمات Database

### 5.1. ایجاد Database در cPanel

1. در cPanel به **"MySQL Databases"** بروید
2. یک Database جدید ایجاد کنید (مثلاً `username_samideutsch`)
3. یک User جدید ایجاد کنید (مثلاً `username_sami_user`)
4. User را به Database اضافه کنید و تمام دسترسی‌ها را بدهید

**نکته:** اگر PostgreSQL می‌خواهید، از **"PostgreSQL Databases"** استفاده کنید.

### 5.2. تنظیمات `.env`

در File Manager، فایل `.env` در ریشه پروژه ایجاد کنید:

```env
# Critical Settings
SECRET_KEY=your-super-secret-key-min-50-characters
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (MySQL/MariaDB)
DATABASE_URL=mysql://username_sami_user:password@localhost:3306/username_samideutsch

# یا برای PostgreSQL:
# DATABASE_URL=postgresql://username_sami_user:password@localhost:5432/username_samideutsch

# Security (اگر SSL دارید)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Static & Media
STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=/home/username/public_html/staticfiles
MEDIA_ROOT=/home/username/public_html/media

# Time Zone
TIME_ZONE=Asia/Tehran
```

**نکته:** 
- `username` را با username cPanel خود جایگزین کنید
- `SECRET_KEY` را با یک کلید امن تولید کنید
- `password` را با password واقعی database جایگزین کنید

### 5.3. تولید SECRET_KEY

در Terminal یا Python App:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🔄 مرحله 6: اجرای Migrations

در Terminal یا از طریق Python App:

```bash
cd ~/public_html
source ~/virtualenv/public_html/3.8/bin/activate

# اجرای migrations
python manage.py migrate

# ایجاد superuser
python manage.py createsuperuser

# جمع‌آوری static files
python manage.py collectstatic --noinput
```

---

## 📁 مرحله 7: تنظیمات Static و Media Files

### 7.1. Static Files

بعد از `collectstatic`، فایل‌های static در `staticfiles/` جمع می‌شوند.

در cPanel:
1. به **File Manager** بروید
2. پوشه `staticfiles` را پیدا کنید
3. مطمئن شوید که دسترسی‌های مناسب دارد (755)

### 7.2. Media Files

پوشه `media/` باید قابل نوشتن باشد:

```bash
chmod 755 media
chmod 755 media/*
```

یا از File Manager:
1. روی پوشه `media` راست کلیک کنید
2. **Change Permissions** را انتخاب کنید
3. دسترسی‌ها را روی `755` تنظیم کنید

### 7.3. تنظیمات Nginx/Apache (اگر دسترسی دارید)

اگر از Nginx استفاده می‌کنید، باید static files را به صورت مستقیم سرو کنید.

---

## 🔒 مرحله 8: تنظیمات امنیتی

### 8.1. بررسی `.env`

مطمئن شوید که:
- `DEBUG=False`
- `SECRET_KEY` امن است
- `ALLOWED_HOSTS` شامل دامنه‌های واقعی است

### 8.2. تنظیمات SSL

اگر SSL دارید:
1. در cPanel به **"SSL/TLS"** بروید
2. گواهینامه را نصب کنید
3. در `.env` تنظیمات SSL را فعال کنید

---

## 🚀 مرحله 9: راه‌اندازی و تست

### 9.1. Restart Python App

در صفحه Python App:
1. روی **"Restart"** کلیک کنید
2. یا از Terminal:

```bash
touch ~/public_html/passenger_wsgi.py
```

### 9.2. تست سایت

1. به دامنه خود بروید
2. بررسی کنید که سایت لود می‌شود
3. صفحه admin را تست کنید: `yourdomain.com/admin/`
4. بررسی کنید که static files لود می‌شوند

---

## 🐛 رفع مشکلات رایج

### مشکل 1: خطای "ModuleNotFoundError"

**راه‌حل:**
```bash
# مطمئن شوید virtual environment فعال است
source ~/virtualenv/public_html/3.8/bin/activate

# dependencies را دوباره نصب کنید
pip install -r requirements.txt
```

### مشکل 2: خطای Database Connection

**راه‌حل:**
- بررسی کنید که اطلاعات database در `.env` درست است
- بررسی کنید که database و user در cPanel ایجاد شده‌اند
- بررسی کنید که user دسترسی به database دارد

### مشکل 3: Static Files لود نمی‌شوند

**راه‌حل:**
```bash
# دوباره collectstatic را اجرا کنید
python manage.py collectstatic --noinput

# بررسی کنید که STATIC_ROOT در settings درست است
```

### مشکل 4: خطای Permission Denied

**راه‌حل:**
```bash
# دسترسی‌های فایل‌ها را تنظیم کنید
chmod 755 ~/public_html
chmod 644 ~/public_html/*.py
chmod 755 ~/public_html/media
```

### مشکل 5: Passenger نمی‌تواند Python App را پیدا کند

**راه‌حل:**
- بررسی کنید که `passenger_wsgi.py` در ریشه پروژه است
- بررسی کنید که مسیرها در Python App درست است
- بررسی کنید که virtual environment درست فعال شده است

---

## 📝 چک‌لیست نهایی

قبل از اینکه سایت را live کنید:

- [ ] تمام فایل‌ها آپلود شده‌اند
- [ ] Python App در cPanel ایجاد شده
- [ ] Virtual environment فعال است
- [ ] Dependencies نصب شده‌اند
- [ ] Database ایجاد شده و متصل است
- [ ] فایل `.env` با تنظیمات صحیح ایجاد شده
- [ ] Migrations اجرا شده
- [ ] Superuser ایجاد شده
- [ ] Static files جمع‌آوری شده
- [ ] `DEBUG=False` در production
- [ ] SSL فعال است (اگر دارید)
- [ ] سایت تست شده و کار می‌کند

---

## 🔄 به‌روزرسانی سایت

برای به‌روزرسانی سایت:

1. فایل‌های جدید را آپلود کنید
2. در Terminal:
```bash
cd ~/public_html
source ~/virtualenv/public_html/3.8/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch passenger_wsgi.py  # Restart app
```

---

## 📞 پشتیبانی

اگر مشکلی پیش آمد:
1. Logs را بررسی کنید (در cPanel: **"Errors"** یا **"Python App Logs"**)
2. Terminal errors را بررسی کنید
3. با پشتیبانی هاستینگ تماس بگیرید

---

## 📚 منابع بیشتر

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [cPanel Python App Documentation](https://docs.cpanel.net/cpanel/software/python-apps/)
- [Passenger Documentation](https://www.phusionpassenger.com/docs/)

---

**موفق باشید! 🎉**








