# 📊 راهنمای مانیتورینگ امنیتی

این راهنما نحوه مانیتورینگ و بررسی رویدادهای امنیتی را توضیح می‌دهد.

---

## 📁 فایل‌های Log

### 1. **logs/django.log**
لاگ‌های عمومی Django شامل:
- Request/Response logs
- Application errors
- Database queries (در DEBUG mode)
- General application events

### 2. **logs/security.log**
لاگ‌های امنیتی شامل:
- Login attempts (موفق و ناموفق)
- Logout events
- Failed authentication attempts
- Security warnings
- Admin access attempts

---

## 🔍 بررسی Log Files

### Linux/Mac
```bash
# مشاهده آخرین 50 خط security log
tail -n 50 logs/security.log

# دنبال کردن log در real-time
tail -f logs/security.log

# جستجوی failed login attempts
grep "Failed login" logs/security.log

# جستجوی admin access
grep "admin" logs/security.log -i
```

### Windows PowerShell
```powershell
# مشاهده آخرین 50 خط
Get-Content logs/security.log -Tail 50

# دنبال کردن log
Get-Content logs/security.log -Wait -Tail 10

# جستجوی failed login
Select-String -Path logs/security.log -Pattern "Failed login"
```

---

## 🚨 رویدادهای امنیتی مهم

### 1. **Failed Login Attempts**
```
WARNING Failed login attempt: username=admin, ip=192.168.1.100, timestamp=2024-01-15 10:30:00
```

**اقدام:**
- بررسی تعداد attempts
- اگر بیش از 5 بار در 15 دقیقه: احتمال brute force attack
- بررسی IP address
- در صورت نیاز: block کردن IP

### 2. **Successful Admin Login**
```
INFO Admin login attempt: username=admin, ip=192.168.1.100
```

**بررسی:**
- آیا IP address شناخته شده است؟
- آیا در زمان غیرمعمول است؟
- آیا از location جدید است؟

### 3. **Security Warnings**
```
WARNING Blocked admin access attempt from unauthorized IP: 192.168.1.200
```

**اقدام:**
- بررسی فوری
- بررسی source IP
- در صورت نیاز: اضافه کردن به whitelist یا block

---

## 📊 مانیتورینگ منظم

### روزانه
- [ ] بررسی failed login attempts
- [ ] بررسی admin access logs
- [ ] بررسی error rates
- [ ] بررسی unusual activity

### هفتگی
- [ ] بررسی log file sizes
- [ ] بررسی patterns در failed attempts
- [ ] بررسی IP addresses مشکوک
- [ ] Review security events

### ماهانه
- [ ] بررسی log retention
- [ ] بررسی security trends
- [ ] Review و update security policies
- [ ] بررسی access patterns

---

## 🔧 ابزارهای مانیتورینگ

### 1. **Log Analysis Tools**
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Graylog**
- **Loki + Grafana**

### 2. **Security Monitoring**
- **Fail2ban** - برای block کردن IP های مشکوک
- **ModSecurity** - Web Application Firewall
- **OSSEC** - Host-based intrusion detection

### 3. **Alerting**
- Email alerts برای critical events
- Slack/Discord notifications
- SMS alerts برای emergencies

---

## 📈 Metrics مهم

### Authentication Metrics
- تعداد login attempts (موفق/ناموفق)
- تعداد unique IP addresses
- تعداد failed attempts per IP
- زمان login attempts

### Security Metrics
- تعداد blocked requests
- تعداد security warnings
- تعداد unauthorized access attempts
- تعداد password reset requests

### Application Metrics
- تعداد errors
- تعداد 404/500 errors
- Response times
- Request rates

---

## 🛡️ Best Practices

### 1. **Log Retention**
- نگهداری logs برای حداقل 90 روز
- Archive کردن logs قدیمی
- Backup منظم log files

### 2. **Log Analysis**
- بررسی منظم logs
- استفاده از automated tools
- Alert برای suspicious patterns

### 3. **Incident Response**
- داشتن plan برای security incidents
- Documentation برای هر incident
- Review و بهبود بعد از incidents

---

## 🔐 Sensitive Data Protection

### در Logs
- ✅ Passwords فیلتر می‌شوند
- ✅ API keys فیلتر می‌شوند
- ✅ Tokens فیلتر می‌شوند
- ✅ Secret keys فیلتر می‌شوند

### در Error Messages
- ✅ Debug info در production نمایش داده نمی‌شود
- ✅ Stack traces فقط در development
- ✅ Custom error pages در production

---

## 📝 Log Format

### Security Log Format
```
{levelname} {asctime} {module} {process:d} {thread:d} {message}
```

### Example
```
WARNING 2024-01-15 10:30:00,123 accounts.middleware 12345 67890 Failed login attempt: username=admin, ip=192.168.1.100, timestamp=2024-01-15 10:30:00
```

---

## 🚀 Quick Commands

### بررسی Failed Logins
```bash
# Linux/Mac
grep "Failed login" logs/security.log | tail -20

# Windows
Select-String -Path logs/security.log -Pattern "Failed login" | Select-Object -Last 20
```

### بررسی Admin Access
```bash
# Linux/Mac
grep -i "admin" logs/security.log | tail -20

# Windows
Select-String -Path logs/security.log -Pattern "admin" -CaseSensitive:$false | Select-Object -Last 20
```

### بررسی IP Addresses
```bash
# Linux/Mac
grep -oE "ip=[0-9.]+" logs/security.log | sort | uniq -c | sort -rn

# Windows
Select-String -Path logs/security.log -Pattern "ip=" | ForEach-Object { $_.Matches.Value } | Group-Object | Sort-Object Count -Descending
```

---

## 📞 Emergency Contacts

در صورت مشاهده security incident:
1. بررسی فوری logs
2. Block کردن IP مشکوک (در صورت نیاز)
3. اطلاع به تیم امنیتی
4. Documentation کامل incident

---

**نکته:** این راهنما باید به صورت منظم به‌روزرسانی شود.

