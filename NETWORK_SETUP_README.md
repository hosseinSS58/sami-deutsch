# 🌐 Network Setup Guide - Sami Deutsch

## 📋 Overview

این راهنما نحوه تنظیم سایت Sami Deutsch برای دسترسی از IP آدرس‌های مختلف شبکه را توضیح می‌دهد.

## 🔧 Configuration

### 1. Django Settings

در فایل `sami/settings.py`، `ALLOWED_HOSTS` را به‌روزرسانی کنید:

```python
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[
    "localhost", 
    "127.0.0.1", 
    "192.168.1.100"
])
```

### 2. Environment Variables

فایل `.env` را در ریشه پروژه ایجاد کنید:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Allowed Hosts - Add your IP addresses here
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100

# Language and Timezone
LANGUAGE_CODE=fa
TIME_ZONE=UTC
```

### 3. IP Address Configuration

#### Local Development
- `localhost` - دسترسی از localhost
- `127.0.0.1` - دسترسی از loopback
- `192.168.1.100` - دسترسی از IP آدرس شبکه

#### Network Access
برای دسترسی از سایر دستگاه‌های شبکه، IP آدرس‌های مورد نظر را اضافه کنید:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100,192.168.1.101,192.168.1.102
```

## 🚀 Running the Server

### 1. Local Access Only
```bash
python manage.py runserver
```
- دسترسی: `http://localhost:8000` یا `http://127.0.0.1:8000`

### 2. Network Access
```bash
python manage.py runserver 0.0.0.0:8000
```
- دسترسی: `http://192.168.1.100:8000`
- سایر دستگاه‌های شبکه می‌توانند از این آدرس استفاده کنند

### 3. Custom Port
```bash
python manage.py runserver 0.0.0.0:8080
```
- دسترسی: `http://192.168.1.100:8080`

## 🔒 Security Considerations

### Development Environment
```python
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.100"]
```

### Production Environment
```python
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]
```

## 🌍 Network Configuration

### 1. Firewall Settings
اطمینان حاصل کنید که پورت 8000 (یا پورت انتخابی) در فایروال باز باشد:

#### Windows
```cmd
netsh advfirewall firewall add rule name="Django Development" dir=in action=allow protocol=TCP localport=8000
```

#### Linux (UFW)
```bash
sudo ufw allow 8000
```

#### macOS
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
```

### 2. Router Configuration
اگر از روتر استفاده می‌کنید، پورت forwarding را تنظیم کنید:
- External Port: 8000
- Internal IP: 192.168.1.100
- Internal Port: 8000

## 📱 Testing Network Access

### 1. From Local Machine
```bash
curl http://192.168.1.100:8000
```

### 2. From Other Devices
- موبایل: `http://192.168.1.100:8000`
- تبلت: `http://192.168.1.100:8000`
- لپ‌تاپ: `http://192.168.1.100:8000`

### 3. Network Scan
```bash
nmap -p 8000 192.168.1.100
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Refused
```bash
# Check if server is running
python manage.py runserver 0.0.0.0:8000

# Check if port is open
netstat -an | grep 8000
```

#### 2. Allowed Hosts Error
```
DisallowedHost at /
Invalid HTTP_HOST header: '192.168.1.100:8000'
```

**Solution**: IP آدرس را به `ALLOWED_HOSTS` اضافه کنید.

#### 3. Firewall Blocking
```bash
# Windows
netsh advfirewall firewall show rule name="Django Development"

# Linux
sudo ufw status
```

#### 4. Network Unreachable
```bash
# Test network connectivity
ping 192.168.1.100

# Check routing
traceroute 192.168.1.100
```

## 🔄 Advanced Configuration

### 1. Multiple IP Addresses
```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.1.100",
    "192.168.1.101",
    "192.168.1.102",
    "192.168.0.0/16",  # All IPs in 192.168.x.x range
]
```

### 2. Environment-Specific Settings
```python
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.100"]
else:
    ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]
```

### 3. Dynamic Host Detection
```python
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    get_local_ip(),
    "192.168.1.100"
]
```

## 📊 Network Monitoring

### 1. Server Logs
```bash
# View Django logs
tail -f django.log

# View access logs
tail -f access.log
```

### 2. Network Statistics
```bash
# Monitor network connections
netstat -an | grep 8000

# Monitor bandwidth usage
iftop -i eth0
```

### 3. Performance Monitoring
```bash
# Monitor CPU and memory
htop

# Monitor disk usage
df -h
```

## 🚀 Production Deployment

### 1. Gunicorn Configuration
```bash
gunicorn --bind 0.0.0.0:8000 sami.wsgi:application
```

### 2. Nginx Configuration
```nginx
server {
    listen 80;
    server_name 192.168.1.100;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Systemd Service
```ini
[Unit]
Description=Django Sami Deutsch
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/sami-deutsch
ExecStart=/path/to/venv/bin/gunicorn --bind 0.0.0.0:8000 sami.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📞 Support

برای سوالات و پشتیبانی:
- 📧 Email: support@samideutsch.com
- 🐛 Issues: GitHub Issues
- 📚 Documentation: این فایل README

---

**نکته**: این تنظیمات برای محیط توسعه هستند. برای تولید، حتماً امنیت را در نظر بگیرید.
