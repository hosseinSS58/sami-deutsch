# 🚀 راهنمای انتقال پروژه از GitHub به cPanel

این راهنما به شما کمک می‌کند که پروژه Django را از GitHub به سرور cPanel منتقل کنید.

---

## 📋 پیش‌نیازها

- ✅ حساب GitHub
- ✅ پروژه در GitHub آپلود شده
- ✅ دسترسی SSH به سرور cPanel (یا Terminal در cPanel)
- ✅ Git نصب شده روی سرور (معمولاً در cPanel موجود است)

---

## 🔧 مرحله 1: آماده‌سازی پروژه برای GitHub

### 1.1. بررسی فایل `.gitignore`

مطمئن شوید که فایل `.gitignore` شامل موارد زیر است:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Backup files
*.bak
*.backup
```

### 1.2. آپلود پروژه به GitHub

اگر پروژه را هنوز به GitHub آپلود نکرده‌اید:

```bash
# در کامپیوتر خودتان
cd C:\Users\Hossein\OneDrive\Documents\Sami_deutsch

# Initialize git (اگر قبلاً نکرده‌اید)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote repository
git remote add origin https://github.com/yourusername/sami-deutsch.git

# Push to GitHub
git push -u origin main
```

**نکته:** اگر repository از قبل وجود دارد:
```bash
git remote add origin https://github.com/yourusername/sami-deutsch.git
git branch -M main
git push -u origin main
```

---

## 📤 مرحله 2: Clone کردن از GitHub روی سرور

### 2.1. دسترسی به Terminal در cPanel

**روش 1: Terminal در cPanel**
1. وارد cPanel شوید
2. به بخش **"Terminal"** بروید
3. Terminal باز می‌شود

**روش 2: SSH (اگر دسترسی دارید)**
```bash
ssh username@yourdomain.com
# یا
ssh username@server-ip
```

### 2.2. Clone کردن پروژه

```bash
# رفتن به دایرکتوری home
cd ~

# Clone کردن از GitHub
git clone https://github.com/yourusername/sami-deutsch.git public_html

git clone https://github.com/hosseinSS58/sami-deutsch.git public_html


# یا اگر public_html از قبل وجود دارد:
cd ~/public_html
git clone https://github.com/yourusername/sami-deutsch.git temp
git clone https://github.com/hosseinSS58/sami-deutsch.git temp


mv temp/* .
mv temp/.git .
rmdir temp
```

**نکته:** اگر repository private است، باید از SSH استفاده کنید یا token ایجاد کنید.

---

## 🔐 مرحله 3: تنظیمات امنیتی

### 3.1. ایجاد فایل `.env`

فایل `.env` در GitHub نیست (به خاطر `.gitignore`). باید در سرور ایجاد کنید:

```bash
cd ~/public_html

# ایجاد فایل .env
nano .env
```

**محتوای `.env` برای Production:**

```env
# Critical Settings
SECRET_KEY=b17em$e3eb+k!)6(j6nkx1dw_+osa8a(!8)gmtkgmc75@&-o+0
DEBUG=False
ALLOWED_HOSTS=samideutsch.ir,www.samideutsch.ir

# Database
DATABASE_URL=mysql://username_sami_user:password@localhost:3306/username_samideutsch

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

**تولید SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.2. بررسی دسترسی‌های فایل

```bash
# محافظت از .env
chmod 600 .env

# دسترسی‌های پوشه‌ها
chmod 755 ~/public_html
chmod 755 ~/public_html/media
chmod 755 ~/public_html/staticfiles
```

---

## 🐍 مرحله 4: تنظیمات Python و Virtual Environment

### 4.1. ایجاد Virtual Environment

```bash
cd ~/public_html

# ایجاد virtual environment
python3 -m venv venv

# فعال‌سازی
source venv/bin/activate

# به‌روزرسانی pip
pip install --upgrade pip

# نصب dependencies
pip install -r requirements.txt
```

**نکته:** در cPanel، ممکن است virtual environment به صورت خودکار ایجاد شود. مسیر آن معمولاً:
```
/home/username/virtualenv/public_html/3.10/
```

### 4.2. استفاده از Virtual Environment cPanel

اگر cPanel virtual environment ایجاد کرده:

```bash
# فعال‌سازی virtual environment cPanel
source ~/virtualenv/public_html/3.10/bin/activate

# نصب dependencies
pip install -r requirements.txt
```

---

## 🗄️ مرحله 5: تنظیمات Database

### 5.1. ایجاد Database در cPanel

1. در cPanel به **"MySQL Databases"** بروید
2. Database جدید ایجاد کنید
3. User جدید ایجاد کنید
4. User را به Database اضافه کنید

### 5.2. اجرای Migrations

```bash
cd ~/public_html
source ~/virtualenv/public_html/3.10/bin/activate

# اجرای migrations
python manage.py migrate

# ایجاد superuser
python manage.py createsuperuser

# جمع‌آوری static files
python manage.py collectstatic --noinput
```

---

## 🔄 مرحله 6: به‌روزرسانی پروژه از GitHub

هر بار که تغییراتی در GitHub می‌دهید، می‌توانید روی سرور به‌روزرسانی کنید:

### 6.1. Pull کردن تغییرات

```bash
cd ~/public_html

# Pull کردن آخرین تغییرات
git pull origin main

# نصب dependencies جدید (اگر requirements.txt تغییر کرده)
source ~/virtualenv/public_html/3.10/bin/activate
pip install -r requirements.txt

# اجرای migrations جدید (اگر migrations جدید دارید)
python manage.py migrate

# جمع‌آوری static files
python manage.py collectstatic --noinput

# Restart Python App (در cPanel)
# یا touch کردن passenger_wsgi.py
touch passenger_wsgi.py
```

### 6.2. ایجاد Script برای به‌روزرسانی

می‌توانید یک script برای به‌روزرسانی سریع ایجاد کنید:

```bash
# ایجاد فایل update.sh
nano ~/update.sh
```

**محتوای `update.sh`:**

```bash
#!/bin/bash

cd ~/public_html

# Pull از GitHub
git pull origin main

# فعال‌سازی virtual environment
source ~/virtualenv/public_html/3.10/bin/activate

# نصب dependencies
pip install -r requirements.txt

# اجرای migrations
python manage.py migrate

# جمع‌آوری static files
python manage.py collectstatic --noinput

# Restart app
touch passenger_wsgi.py

echo "Update completed!"
```

**اجرای script:**
```bash
chmod +x ~/update.sh
~/update.sh
```

---

## 🔐 مرحله 7: استفاده از SSH Key برای GitHub (اختیاری)

اگر repository private است، بهتر است از SSH Key استفاده کنید:

### 7.1. ایجاد SSH Key روی سرور

```bash
# ایجاد SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# نمایش public key
cat ~/.ssh/id_ed25519.pub
```

### 7.2. اضافه کردن SSH Key به GitHub

1. محتوای public key را کپی کنید
2. در GitHub به **Settings > SSH and GPG keys** بروید
3. **New SSH key** را بزنید
4. Key را اضافه کنید

### 7.3. Clone با SSH

```bash
# Clone با SSH
git clone git@github.com:yourusername/sami-deutsch.git public_html
```

---

## 🔄 مرحله 8: استفاده از GitHub Token (برای HTTPS)

اگر می‌خواهید از HTTPS استفاده کنید اما repository private است:

### 8.1. ایجاد Personal Access Token

1. در GitHub به **Settings > Developer settings > Personal access tokens > Tokens (classic)** بروید
2. **Generate new token** را بزنید
3. Scopes را انتخاب کنید (حداقل `repo`)
4. Token را کپی کنید

### 8.2. استفاده از Token

```bash
# Clone با token
git clone https://YOUR_TOKEN@github.com/yourusername/sami-deutsch.git public_html

# یا تنظیم credential helper
git config --global credential.helper store
# سپس در اولین pull، username و token را وارد کنید
```

---

## 📝 چک‌لیست کامل

### قبل از Clone:
- [ ] پروژه در GitHub آپلود شده
- [ ] `.gitignore` شامل فایل‌های حساس است
- [ ] `.env` در `.gitignore` است

### بعد از Clone:
- [ ] فایل `.env` در سرور ایجاد شده
- [ ] `SECRET_KEY` تولید و تنظیم شده
- [ ] `DEBUG=False` در `.env`
- [ ] `ALLOWED_HOSTS` شامل دامنه‌های واقعی
- [ ] Database ایجاد شده
- [ ] `DATABASE_URL` در `.env` تنظیم شده
- [ ] Virtual environment فعال است
- [ ] Dependencies نصب شده
- [ ] Migrations اجرا شده
- [ ] Static files جمع‌آوری شده
- [ ] Python App در cPanel ایجاد شده
- [ ] سایت تست شده

---

## 🐛 مشکلات رایج

### مشکل 1: "Permission denied (publickey)"

**راه‌حل:**
- از SSH Key استفاده کنید
- یا از Personal Access Token با HTTPS استفاده کنید

### مشکل 2: "Repository not found"

**راه‌حل:**
- مطمئن شوید که repository public است
- یا از SSH Key یا Token استفاده کنید

### مشکل 3: "Git command not found"

**راه‌حل:**
```bash
# بررسی نصب git
which git

# اگر نصب نیست، با پشتیبانی هاستینگ تماس بگیرید
```

### مشکل 4: تغییرات `.env` overwrite می‌شود

**راه‌حل:**
- مطمئن شوید که `.env` در `.gitignore` است
- از `git pull` استفاده کنید (نه `git clone` دوباره)

---

## 🚀 Workflow پیشنهادی

### برای Development:
1. تغییرات را در کامپیوتر خودتان انجام دهید
2. Commit و Push به GitHub
3. روی سرور: `git pull` و `~/update.sh`

### برای Production:
1. همیشه از branch `main` استفاده کنید
2. قبل از push، تست کنید
3. بعد از pull روی سرور، حتماً migrations و collectstatic را اجرا کنید

---

## 📚 منابع بیشتر

- [GitHub Documentation](https://docs.github.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

---

**موفق باشید! 🎉**

اگر سوالی دارید یا مشکلی پیش آمد، بپرسید.







