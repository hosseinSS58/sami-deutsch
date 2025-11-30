# 🚀 راهنمای کامل Deploy به Production

این راهنما گام‌به‌گام نحوه deploy کردن سایت Sami Deutsch به production را توضیح می‌دهد.

---

## 📋 پیش‌نیازها

### 1. **Server Requirements**
- Ubuntu 20.04+ یا CentOS 8+ (توصیه: Ubuntu 22.04 LTS)
- حداقل 2GB RAM (توصیه: 4GB برای performance بهتر)
- **فضای ذخیره‌سازی:**
  - **حداقل برای شروع:** 10-15 GB
  - **توصیه شده برای production:** 20-30 GB
  - **برای پروژه‌های بزرگ:** 50-100 GB+
  
  **تجزیه فضای مورد نیاز:**
  - سیستم عامل و نرم‌افزارها: ~5 GB
  - کد پروژه و virtual environment: ~1 GB
  - Database: ~500 MB - 2 GB (بسته به داده‌ها)
  - Static files: ~200 MB
  - Media files (تصاویر، آواتارها): متغیر - بسته به محتوا
    - 100 تصویر: ~100-500 MB
    - 1000 تصویر: ~1-5 GB
  - Logs (با rotation): ~1-2 GB
  - Backups (30 روز retention): ~2-5 GB
  - فضای اضافی (20%): ~2-5 GB
  
  **نکته:** برای جزئیات بیشتر، فایل `STORAGE_REQUIREMENTS.md` را ببینید.
  
- دسترسی root یا sudo
- Domain name (مثلاً samideutsch.com)

### 2. **Software Requirements**
- Python 3.10+
- PostgreSQL 14+ (یا MySQL 8+)
- Nginx
- Gunicorn
- Supervisor (یا systemd)
- Certbot (برای SSL)

---

## 🔧 مرحله 1: آماده‌سازی Server

### 1.1. به‌روزرسانی سیستم
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 1.2. نصب Python و Dependencies
```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y supervisor
sudo apt install -y git
sudo apt install -y build-essential libpq-dev

# CentOS/RHEL
sudo yum install -y python3 python3-pip python3-venv python3-devel
sudo yum install -y postgresql postgresql-server
sudo yum install -y nginx
sudo yum install -y supervisor
sudo yum install -y git gcc postgresql-devel
```

### 1.3. ایجاد User برای Django
```bash
# ایجاد user جدید
sudo adduser --disabled-password --gecos "" sami
sudo usermod -aG sudo sami

# ورود به user
su - sami
```

---

## 🗄️ مرحله 2: تنظیمات Database

### 2.1. ایجاد Database و User
```bash
# ورود به PostgreSQL
sudo -u postgres psql

# در PostgreSQL shell:
CREATE DATABASE sami_deutsch;
CREATE USER sami_user WITH PASSWORD 'your_strong_password_here';
ALTER ROLE sami_user SET client_encoding TO 'utf8';
ALTER ROLE sami_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sami_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sami_deutsch TO sami_user;
\q
```

### 2.2. تنظیمات PostgreSQL
```bash
# ویرایش pg_hba.conf
sudo nano /etc/postgresql/14/main/pg_hba.conf

# اضافه کردن:
host    sami_deutsch    sami_user    127.0.0.1/32    md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 📦 مرحله 3: Deploy کد

### 3.1. Clone Repository
```bash
cd /home/sami
git clone https://github.com/yourusername/sami_deutsch.git
cd sami_deutsch
```

### 3.2. ایجاد Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.3. تنظیمات Environment Variables
```bash
# ایجاد فایل .env
nano .env
```

**محتوای `.env` برای Production:**
```bash
# Critical Settings
SECRET_KEY=your-super-secret-key-min-50-characters-generate-with-python
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,IP_ADDRESS

# Database
DATABASE_URL=postgresql://sami_user:your_strong_password@localhost:5432/sami_deutsch

# Security (with HTTPS)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Admin URL (change for security)
ADMIN_URL=secret-admin-2024/

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Time Zone
TIME_ZONE=Asia/Tehran

# Optional: IP Whitelist for Admin
# ADMIN_IP_WHITELIST=YOUR_IP_ADDRESS
```

**تولید SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.4. اجرای Migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 🔒 مرحله 4: تنظیمات SSL/HTTPS

### 4.1. نصب Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### 4.2. دریافت SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot به صورت خودکار:
- SSL certificate را دریافت می‌کند
- Nginx را پیکربندی می‌کند
- Auto-renewal را تنظیم می‌کند

---

## 🌐 مرحله 5: تنظیمات Nginx

### 5.1. ایجاد Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/samideutsch
```

**محتوای فایل:**
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Logging
    access_log /var/log/nginx/samideutsch_access.log;
    error_log /var/log/nginx/samideutsch_error.log;

    # Client Max Body Size (for file uploads)
    client_max_body_size 10M;

    # Static Files
    location /static/ {
        alias /home/sami/sami_deutsch/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media Files
    location /media/ {
        alias /home/sami/sami_deutsch/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 5.2. فعال‌سازی Site
```bash
sudo ln -s /etc/nginx/sites-available/samideutsch /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

## 🔄 مرحله 6: تنظیمات Gunicorn

### 6.1. ایجاد Gunicorn Service File
```bash
sudo nano /etc/systemd/system/samideutsch.service
```

**محتوای فایل:**
```ini
[Unit]
Description=Sami Deutsch Gunicorn daemon
After=network.target

[Service]
User=sami
Group=sami
WorkingDirectory=/home/sami/sami_deutsch
Environment="PATH=/home/sami/sami_deutsch/venv/bin"
ExecStart=/home/sami/sami_deutsch/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --access-logfile /home/sami/sami_deutsch/logs/gunicorn_access.log \
    --error-logfile /home/sami/sami_deutsch/logs/gunicorn_error.log \
    --log-level info \
    --timeout 120 \
    --keep-alive 5 \
    sami.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6.2. فعال‌سازی و Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable samideutsch
sudo systemctl start samideutsch
sudo systemctl status samideutsch
```

---

## 📊 مرحله 7: تنظیمات Monitoring

### 7.1. ایجاد Logs Directory
```bash
mkdir -p /home/sami/sami_deutsch/logs
chmod 755 /home/sami/sami_deutsch/logs
```

### 7.2. Log Rotation
```bash
sudo nano /etc/logrotate.d/samideutsch
```

**محتوای فایل:**
```
/home/sami/sami_deutsch/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 sami sami
    sharedscripts
    postrotate
        systemctl reload samideutsch > /dev/null 2>&1 || true
    endscript
}
```

---

## 💾 مرحله 8: تنظیمات Backup

### 8.1. ایجاد Backup Script
```bash
nano /home/sami/backup_samideutsch.sh
```

**محتوای Script:**
```bash
#!/bin/bash
BACKUP_DIR="/home/sami/backups"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/home/sami/sami_deutsch"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U sami_user sami_deutsch > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $PROJECT_DIR media/

# Backup .env file
cp $PROJECT_DIR/.env $BACKUP_DIR/env_$DATE

# Remove backups older than 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 8.2. قابل اجرا کردن Script
```bash
chmod +x /home/sami/backup_samideutsch.sh
```

### 8.3. تنظیم Cron Job
```bash
crontab -e

# اضافه کردن:
# Backup daily at 2 AM
0 2 * * * /home/sami/backup_samideutsch.sh >> /home/sami/backup.log 2>&1
```

---

## 🔐 مرحله 9: تنظیمات Firewall

### 9.1. UFW (Ubuntu)
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

### 9.2. Firewalld (CentOS)
```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## ✅ مرحله 10: تست و بررسی

### 10.1. بررسی Services
```bash
# بررسی Gunicorn
sudo systemctl status samideutsch

# بررسی Nginx
sudo systemctl status nginx

# بررسی PostgreSQL
sudo systemctl status postgresql
```

### 10.2. بررسی Logs
```bash
# Gunicorn logs
tail -f /home/sami/sami_deutsch/logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/samideutsch_error.log

# Django logs
tail -f /home/sami/sami_deutsch/logs/django.log

# Security logs
tail -f /home/sami/sami_deutsch/logs/security.log
```

### 10.3. تست Website
```bash
# تست از server
curl -I https://yourdomain.com

# بررسی Security Headers
curl -I https://yourdomain.com | grep -i "x-frame\|x-content\|strict-transport"
```

---

## 🔄 مرحله 11: به‌روزرسانی (Updates)

### 11.1. Process به‌روزرسانی
```bash
cd /home/sami/sami_deutsch
source venv/bin/activate

# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart samideutsch

# Reload Nginx (if config changed)
sudo nginx -t && sudo systemctl reload nginx
```

---

## 📝 چک‌لیست نهایی

### قبل از Go Live:
- [ ] تمام environment variables تنظیم شده
- [ ] DEBUG=False
- [ ] SECRET_KEY قوی و منحصر به فرد
- [ ] ALLOWED_HOSTS شامل دامنه‌های واقعی
- [ ] SSL/HTTPS فعال و کار می‌کند
- [ ] Database migrations اجرا شده
- [ ] Static files collect شده
- [ ] Superuser ایجاد شده
- [ ] Gunicorn service فعال است
- [ ] Nginx configuration صحیح است
- [ ] Firewall تنظیم شده
- [ ] Backup script تست شده
- [ ] Logs در حال نوشتن هستند
- [ ] Security headers موجود هستند
- [ ] Custom error pages کار می‌کنند

### بعد از Go Live:
- [ ] سایت در HTTPS لود می‌شود
- [ ] تمام صفحات کار می‌کنند
- [ ] Login/logout کار می‌کند
- [ ] File uploads کار می‌کنند
- [ ] Admin panel قابل دسترسی است
- [ ] Logs بررسی شده‌اند
- [ ] Performance قابل قبول است
- [ ] Monitoring فعال است

---

## 🆘 Troubleshooting

### مشکل: Gunicorn start نمی‌شود
```bash
# بررسی logs
sudo journalctl -u samideutsch -n 50

# بررسی permissions
ls -la /home/sami/sami_deutsch

# بررسی .env file
cat /home/sami/sami_deutsch/.env
```

### مشکل: 502 Bad Gateway
```bash
# بررسی Gunicorn
sudo systemctl status samideutsch

# بررسی port
sudo netstat -tlnp | grep 8000

# بررسی Nginx error log
sudo tail -f /var/log/nginx/samideutsch_error.log
```

### مشکل: Static files نمایش داده نمی‌شوند
```bash
# بررسی collectstatic
python manage.py collectstatic --noinput

# بررسی permissions
sudo chown -R sami:sami /home/sami/sami_deutsch/staticfiles

# بررسی Nginx config
sudo nginx -t
```

### مشکل: Database connection error
```bash
# تست connection
psql -U sami_user -d sami_deutsch -h localhost

# بررسی PostgreSQL
sudo systemctl status postgresql

# بررسی .env DATABASE_URL
cat /home/sami/sami_deutsch/.env | grep DATABASE
```

---

## 📚 منابع بیشتر

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

## 🔐 نکات امنیتی مهم

1. **هرگز `.env` را commit نکنید**
2. **SECRET_KEY را به صورت منحصر به فرد برای هر environment تولید کنید**
3. **Database password را قوی انتخاب کنید**
4. **Admin URL را تغییر دهید**
5. **Firewall را فعال کنید**
6. **Backups را به صورت منظم تست کنید**
7. **Logs را به صورت منظم بررسی کنید**
8. **Security updates را به موقع نصب کنید**

---

**نکته:** این راهنما یک template است. حتماً با توجه به نیازهای خاص خودتان تنظیم کنید.

