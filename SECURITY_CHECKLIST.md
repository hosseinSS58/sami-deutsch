# ✅ چک‌لیست امنیتی Production Deployment

این چک‌لیست باید قبل از deploy به production کامل شود.

---

## 🔴 Critical (باید انجام شود)

### Environment Variables
- [ ] `SECRET_KEY` تنظیم شده و قوی است (حداقل 50 کاراکتر)
- [ ] `DEBUG=False` در production
- [ ] `ALLOWED_HOSTS` شامل دامنه‌های واقعی است
- [ ] `DATABASE_URL` برای production database تنظیم شده
- [ ] `ADMIN_URL` تغییر یافته (مثلاً `secret-admin-2024/`)

### Security Settings
- [ ] `SECURE_SSL_REDIRECT=True` (با HTTPS)
- [ ] `SECURE_HSTS_SECONDS=31536000` (1 year)
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `CSRF_TRUSTED_ORIGINS` شامل دامنه‌های production

### Server Configuration
- [ ] HTTPS/SSL certificate نصب و فعال است
- [ ] Firewall rules تنظیم شده
- [ ] Database backups خودکار فعال است
- [ ] Static files به درستی serve می‌شوند (نه از Django)
- [ ] Media files محافظت شده‌اند

---

## 🟡 Important (توصیه می‌شود)

### Application Security
- [ ] Admin users محدود و trusted هستند
- [ ] Password policies قوی هستند
- [ ] Rate limiting برای login فعال است
- [ ] Logging و monitoring تنظیم شده
- [ ] Error pages custom شده (بدون debug info)

### Database Security
- [ ] Database user با حداقل دسترسی‌های لازم
- [ ] Connection encryption فعال است
- [ ] Regular backups تست شده‌اند
- [ ] Database credentials در environment variables

### File Security
- [ ] File upload validation کامل است
- [ ] Media files در مسیر امن هستند
- [ ] File size limits تنظیم شده
- [ ] File type validation فعال است

---

## 🟢 Optional (بهبودهای آینده)

### Advanced Security
- [ ] 2FA برای admin users
- [ ] Content Security Policy (CSP) کامل
- [ ] IP whitelist برای admin
- [ ] Security headers کامل
- [ ] DDoS protection

### Monitoring & Logging
- [ ] Security event monitoring
- [ ] Failed login attempt alerts
- [ ] Unusual activity detection
- [ ] Log aggregation و analysis

---

## 📋 Pre-Deployment Tests

### Security Tests
- [ ] CSRF protection تست شده
- [ ] XSS protection تست شده
- [ ] SQL injection protection تست شده
- [ ] File upload security تست شده
- [ ] Authentication flows تست شده

### Functional Tests
- [ ] تمام features کار می‌کنند
- [ ] Admin panel قابل دسترسی است
- [ ] User registration/login کار می‌کند
- [ ] File uploads کار می‌کنند
- [ ] Email sending کار می‌کند

---

## 🔍 Post-Deployment Checks

### Immediate Checks
- [ ] سایت در HTTPS لود می‌شود
- [ ] Security headers در response موجود هستند
- [ ] Admin panel با URL جدید قابل دسترسی است
- [ ] Log files در حال نوشتن هستند
- [ ] Error handling درست کار می‌کند

### Monitoring (اولین 24 ساعت)
- [ ] Log files را بررسی کنید
- [ ] Failed login attempts را مانیتور کنید
- [ ] Error rates را بررسی کنید
- [ ] Performance metrics را چک کنید
- [ ] User feedback را جمع‌آوری کنید

---

## 📝 Quick Reference

### Environment Variables Template
```bash
# Critical
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ADMIN_URL=secret-admin-2024/

# Security (with HTTPS)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Security Headers Check
```bash
# Test with curl
curl -I https://yourdomain.com

# Should see:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Strict-Transport-Security: max-age=31536000
```

---

## 🚨 Emergency Contacts

- **Security Issues**: [Your security team email]
- **Server Issues**: [Your DevOps team email]
- **Database Issues**: [Your DBA email]

---

**نکته:** این چک‌لیست باید قبل از هر deployment بررسی شود.







