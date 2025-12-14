# ⚡ راهنمای سریع Deploy روی cPanel

این یک راهنمای سریع برای deploy کردن سایت روی cPanel است. برای جزئیات کامل، `CPANEL_DEPLOYMENT_GUIDE.md` را ببینید.

---

## 🎯 مراحل سریع

### 1️⃣ آماده‌سازی فایل‌ها

```bash
# در کامپیوتر خودتان
# فایل‌های غیرضروری را حذف کنید:
# - .git/
# - __pycache__/
# - venv/
# - db.sqlite3
# - .env (بعداً در سرور ایجاد می‌کنیم)
```

**فایل‌های ضروری:**
- ✅ تمام فایل‌های `.py`
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ `passenger_wsgi.py` (در پروژه موجود است)
- ✅ `templates/`, `static/`, `media/`

### 2️⃣ آپلود به سرور

1. وارد cPanel شوید
2. به **File Manager** بروید
3. به `public_html` بروید
4. تمام فایل‌ها را آپلود کنید

### 3️⃣ ایجاد Python App

1. در cPanel به **"Setup Python App"** بروید
2. **Create Application** را بزنید
3. تنظیمات:
   - Python Version: آخرین نسخه (3.8+)
   - App Directory: `public_html`
   - App URL: `/`
   - Startup File: `passenger_wsgi.py`
   - Entry Point: `application`
4. **Create** را بزنید

### 4️⃣ نصب Dependencies

در Terminal cPanel:

```bash
cd ~/public_html
source ~/virtualenv/public_html/3.8/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5️⃣ ایجاد Database

1. در cPanel به **MySQL Databases** بروید
2. Database جدید ایجاد کنید: `username_samideutsch`
3. User جدید ایجاد کنید: `username_sami_user`
4. User را به Database اضافه کنید

### 6️⃣ تنظیمات `.env`

در File Manager، فایل `.env` ایجاد کنید:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=mysql://username_sami_user:password@localhost:3306/username_samideutsch
```

**تولید SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7️⃣ اجرای Migrations

```bash
cd ~/public_html
source ~/virtualenv/public_html/3.8/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 8️⃣ Restart App

در صفحه Python App، **Restart** را بزنید.

---

## ✅ چک‌لیست

- [ ] فایل‌ها آپلود شده
- [ ] Python App ایجاد شده
- [ ] Dependencies نصب شده
- [ ] Database ایجاد شده
- [ ] `.env` تنظیم شده
- [ ] Migrations اجرا شده
- [ ] Static files جمع‌آوری شده
- [ ] App restart شده
- [ ] سایت تست شده

---

## 🐛 مشکلات رایج

### خطای ModuleNotFoundError
```bash
source ~/virtualenv/public_html/3.8/bin/activate
pip install -r requirements.txt
```

### Static Files لود نمی‌شوند
```bash
python manage.py collectstatic --noinput
```

### Permission Denied
```bash
chmod 755 ~/public_html
chmod 755 ~/public_html/media
```

---

**برای جزئیات بیشتر، `CPANEL_DEPLOYMENT_GUIDE.md` را ببینید.**











