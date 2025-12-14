# ✅ چک‌لیست سریع Deploy

این یک چک‌لیست سریع برای deploy است. برای جزئیات کامل، `DEPLOYMENT_GUIDE.md` را ببینید.

---

## 🔴 قبل از Deploy

### Server Setup
- [ ] Server آماده است (Ubuntu 22.04+)
- [ ] Python 3.10+ نصب شده
- [ ] PostgreSQL نصب و راه‌اندازی شده
- [ ] Nginx نصب شده
- [ ] Domain name به IP server اشاره می‌کند

### کد و تنظیمات
- [ ] کد در repository است
- [ ] `.env` file با تنظیمات production ایجاد شده
- [ ] `SECRET_KEY` تولید و در `.env` قرار گرفته
- [ ] `DEBUG=False` در `.env`
- [ ] `ALLOWED_HOSTS` شامل دامنه‌های واقعی
- [ ] Database credentials در `.env`

---

## 🟡 مراحل Deploy

### 1. Server Setup
```bash
# روی server
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql nginx git
```

### 2. Database Setup
```bash
sudo -u postgres psql
# در PostgreSQL:
CREATE DATABASE sami_deutsch;
CREATE USER sami_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE sami_deutsch TO sami_user;
\q
```

### 3. Clone و Setup
```bash
cd /home/sami
git clone YOUR_REPO_URL
cd sami_deutsch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Environment Variables
```bash
nano .env
# تمام تنظیمات را وارد کنید
```

### 5. Django Setup
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 7. Gunicorn Service
```bash
# ایجاد service file (مطابق DEPLOYMENT_GUIDE.md)
sudo systemctl enable samideutsch
sudo systemctl start samideutsch
```

### 8. Nginx Configuration
```bash
# ایجاد config (مطابق DEPLOYMENT_GUIDE.md)
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🟢 بعد از Deploy

### بررسی‌ها
- [ ] سایت در HTTPS لود می‌شود
- [ ] تمام صفحات کار می‌کنند
- [ ] Login/logout کار می‌کند
- [ ] Admin panel قابل دسترسی است
- [ ] Static files نمایش داده می‌شوند
- [ ] Logs در حال نوشتن هستند

### Monitoring
- [ ] Logs را بررسی کنید
- [ ] Performance را چک کنید
- [ ] Security logs را مانیتور کنید

---

## 🆘 مشکلات رایج

### 502 Bad Gateway
```bash
sudo systemctl status samideutsch
sudo tail -f /home/sami/sami_deutsch/logs/gunicorn_error.log
```

### Static files نمایش داده نمی‌شوند
```bash
python manage.py collectstatic --noinput
sudo chown -R sami:sami staticfiles/
```

### Database connection error
```bash
# تست connection
psql -U sami_user -d sami_deutsch -h localhost
```

---

**برای جزئیات کامل، `DEPLOYMENT_GUIDE.md` را مطالعه کنید.**











