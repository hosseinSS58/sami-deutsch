# 🔍 حل مشکل: فایل‌ها پیدا نمی‌شوند

اگر خطای `cannot stat` می‌گیرید، یعنی فایل‌ها در `public_html` نیستند.

---

## 🔍 مرحله 1: بررسی محل فایل‌ها

### بررسی اینکه فایل‌ها کجا هستند:

```bash
# بررسی محتوای public_html
cd ~/public_html
ls -la

# جستجو برای manage.py
find ~ -name "manage.py" 2>/dev/null

# جستجو برای passenger_wsgi.py
find ~ -name "passenger_wsgi.py" 2>/dev/null
```

---

## ✅ راه‌حل: Clone کردن از GitHub

اگر فایل‌ها هنوز آپلود نشده‌اند، از GitHub clone کنید:

### روش 1: Clone مستقیم در django_app

```bash
# رفتن به public_html
cd ~/public_html

# ایجاد پوشه django_app
mkdir django_app

# Clone کردن از GitHub در django_app
cd django_app
git clone https://github.com/hosseinSS58/sami-deutsch.git .

# نقطه (.) در انتها یعنی clone در همین پوشه (نه در پوشه جدید)
```

**نکته:** نقطه (`.`) در انتهای دستور `git clone` مهم است و باعث می‌شود فایل‌ها مستقیماً در `django_app` قرار بگیرند.

---

### روش 2: Clone در جای دیگر و سپس انتقال

```bash
# Clone در home directory
cd ~
git clone https://github.com/hosseinSS58/sami-deutsch.git temp_clone

# ایجاد پوشه django_app
mkdir -p ~/public_html/django_app

# انتقال فایل‌ها
mv ~/temp_clone/* ~/public_html/django_app/
mv ~/temp_clone/.git ~/public_html/django_app/ 2>/dev/null

# حذف پوشه موقت
rmdir ~/temp_clone
```

---

## 📋 بررسی بعد از Clone

بعد از clone، بررسی کنید که فایل‌ها درست هستند:

```bash
cd ~/public_html/django_app
ls -la

# باید این فایل‌ها را ببینید:
# - manage.py
# - passenger_wsgi.py
# - requirements.txt
# - sami/
# - accounts/
# و ...
```

---

## 🔧 اگر فایل‌ها در جای دیگری هستند

اگر فایل‌ها در جای دیگری هستند (مثلاً در `~/sami-deutsch`):

```bash
# پیدا کردن محل فایل‌ها
find ~ -name "manage.py" 2>/dev/null

# فرض کنید در ~/sami-deutsch هستند:
cd ~/public_html
mkdir django_app
cp -r ~/sami-deutsch/* ~/public_html/django_app/
cp -r ~/sami-deutsch/.git ~/public_html/django_app/ 2>/dev/null
```

---

## ✅ مراحل کامل (از صفر)

اگر می‌خواهید از ابتدا شروع کنید:

```bash
# 1. رفتن به public_html
cd ~/public_html

# 2. ایجاد پوشه django_app
mkdir django_app

# 3. Clone از GitHub
cd django_app
git clone https://github.com/hosseinSS58/sami-deutsch.git .

# 4. بررسی فایل‌ها
ls -la

# 5. ایجاد فایل .env
nano .env
# (محتوای .env را وارد کنید)

# 6. حالا می‌توانید Python App را ایجاد کنید
# Application root: /home/username/public_html/django_app
```

---

## 🐛 مشکلات احتمالی

### مشکل: "git: command not found"

**راه‌حل:**
- با پشتیبانی هاستینگ تماس بگیرید
- یا از File Manager برای آپلود استفاده کنید

### مشکل: "Permission denied"

**راه‌حل:**
```bash
# تنظیم دسترسی‌ها
chmod 755 ~/public_html
chmod 755 ~/public_html/django_app
```

### مشکل: Repository private است

**راه‌حل:**
- از SSH Key استفاده کنید
- یا از Personal Access Token استفاده کنید

---

## 📝 چک‌لیست

- [ ] پوشه `django_app` ایجاد شده
- [ ] فایل‌ها از GitHub clone شده‌اند
- [ ] `manage.py` در `django_app` موجود است
- [ ] `passenger_wsgi.py` در `django_app` موجود است
- [ ] `requirements.txt` در `django_app` موجود است
- [ ] پوشه `sami/` در `django_app` موجود است

---

**بعد از این مراحل، می‌توانید Python App را با Application root: `/home/username/public_html/django_app` ایجاد کنید.**






