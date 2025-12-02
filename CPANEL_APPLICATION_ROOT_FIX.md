# 🔧 حل مشکل "Directory 'public_html' not allowed" در cPanel

این راهنما به شما کمک می‌کند که مشکل ایجاد Python App در cPanel را حل کنید.

---

## ❌ مشکل

هنگام ایجاد Python App در cPanel، این خطا را می‌گیرید:

```
Error: Directory "public_html" not allowed
```

---

## ✅ راه‌حل‌ها

### راه‌حل 1: استفاده از Subdirectory (توصیه می‌شود - اگر public_html کار نکرد)

اگر cPanel اجازه استفاده از `public_html` را نمی‌دهد، از یک subdirectory استفاده کنید:

**مرحله 1: ایجاد پوشه جدید**
```bash
# در Terminal
cd ~/public_html
mkdir django_app
```

**مرحله 2: انتقال فایل‌ها**
```bash
# اگر فایل‌ها در public_html هستند، به django_app منتقل کنید
cd ~/public_html
mv manage.py passenger_wsgi.py requirements.txt django_app/
mv sami accounts courses templates static django_app/
# و بقیه فایل‌ها و پوشه‌ها
```

**مرحله 3: تنظیمات Python App**
- **Application root:** `/home/username/public_html/django_app`
- **Application URL:** `/` (اگر می‌خواهید در root اجرا شود)

**نکته:** بعد از این کار، باید `.htaccess` در `public_html` ایجاد کنید که درخواست‌ها را به `django_app` هدایت کند.

---

### راه‌حل 2: استفاده از مسیر کامل (اگر راه‌حل 1 کار نکرد)

به جای `public_html`، از مسیر کامل استفاده کنید:

**Application root:**
```
/home/username/public_html
```

**نکته:** `username` را با username cPanel خود جایگزین کنید.

**چطور پیدا کنید:**
1. در cPanel به **File Manager** بروید
2. به پوشه `public_html` بروید
3. در بالای صفحه، مسیر کامل را می‌بینید (مثلاً `/home/samideut/public_html`)

---

### راه‌حل 2: استفاده از Subdirectory

اگر راه‌حل 1 کار نکرد، می‌توانید از یک subdirectory استفاده کنید:

**گزینه A: ایجاد پوشه جداگانه**

```bash
# در Terminal
cd ~/public_html
mkdir django_app
cd django_app
# فایل‌های پروژه را اینجا قرار دهید
```

سپس در Python App:
- **Application root:** `/home/username/public_html/django_app`
- **Application URL:** `/django_app` یا `/`

**گزینه B: استفاده از پوشه موجود**

اگر پروژه در یک subdirectory است:
- **Application root:** `/home/username/public_html/your_project_folder`
- **Application URL:** `/` (اگر می‌خواهید در root اجرا شود)

---

### راه‌حل 3: بررسی دسترسی‌ها

مطمئن شوید که دسترسی‌های مناسب دارید:

```bash
# بررسی دسترسی‌ها
ls -la ~/public_html

# تنظیم دسترسی‌ها (اگر نیاز باشد)
chmod 755 ~/public_html
```

---

## 📋 تنظیمات صحیح Python App

### اگر می‌خواهید سایت در root domain اجرا شود:

| فیلد | مقدار |
|------|-------|
| **Python version** | `Python 3.10` (یا آخرین نسخه) |
| **Application root** | `/home/username/public_html` |
| **Application URL** | `/` |
| **Application startup file** | `passenger_wsgi.py` |
| **Application Entry point** | `application` |
| **Passenger log file** | `/home/username/logs/passenger.log` |

**نکته:** `username` را با username cPanel خود جایگزین کنید.

---

### اگر می‌خواهید در subdirectory اجرا شود:

| فیلد | مقدار |
|------|-------|
| **Python version** | `Python 3.10` |
| **Application root** | `/home/username/public_html/django_app` |
| **Application URL** | `/django_app` |
| **Application startup file** | `passenger_wsgi.py` |
| **Application Entry point** | `application` |
| **Passenger log file** | `/home/username/logs/passenger.log` |

---

## 🔍 پیدا کردن Username

### روش 1: از File Manager
1. در cPanel به **File Manager** بروید
2. به پوشه `public_html` بروید
3. در بالای صفحه، مسیر کامل را می‌بینید:
   ```
   Current Path: /home/samideut/public_html
   ```
   در این مثال، `samideut` username شماست.

### روش 2: از Terminal
```bash
# نمایش username
whoami

# یا
echo $USER

# یا از مسیر home
echo $HOME
# خروجی: /home/username
```

---

## 📝 مثال کامل

فرض کنید:
- Username: `samideut`
- می‌خواهید سایت در root domain اجرا شود

**تنظیمات:**

```
Python version: Python 3.10
Application root: /home/samideut/public_html
Application URL: /
Application startup file: passenger_wsgi.py
Application Entry point: application
Passenger log file: /home/samideut/logs/passenger.log
```

---

## 🐛 مشکلات دیگر

### مشکل: "Application root not found"

**راه‌حل:**
- مطمئن شوید که مسیر درست است
- از File Manager مسیر را کپی کنید
- دقت کنید که `/` در ابتدای مسیر باشد

### مشکل: "Permission denied"

**راه‌حل:**
```bash
# تنظیم دسترسی‌ها
chmod 755 ~/public_html
chmod 644 ~/public_html/*.py
```

### مشکل: "Startup file not found"

**راه‌حل:**
- مطمئن شوید که `passenger_wsgi.py` در Application root است
- نام فایل باید دقیقاً `passenger_wsgi.py` باشد

---

## ✅ چک‌لیست

قبل از ایجاد Python App:

- [ ] Username cPanel را می‌دانید
- [ ] مسیر کامل `public_html` را می‌دانید
- [ ] فایل `passenger_wsgi.py` در `public_html` موجود است
- [ ] فایل `manage.py` در `public_html` موجود است
- [ ] پوشه `logs` ایجاد شده (برای Passenger log)

---

## 🚀 مراحل بعدی

بعد از ایجاد موفق Python App:

1. Virtual environment به صورت خودکار ایجاد می‌شود
2. Dependencies را نصب کنید:
   ```bash
   source ~/virtualenv/public_html/3.10/bin/activate
   pip install -r requirements.txt
   ```
3. Migrations را اجرا کنید:
   ```bash
   python manage.py migrate
   ```
4. Static files را جمع‌آوری کنید:
   ```bash
   python manage.py collectstatic --noinput
   ```

---

**موفق باشید! 🎉**

اگر هنوز مشکل دارید، بگویید چه خطایی می‌گیرید.

