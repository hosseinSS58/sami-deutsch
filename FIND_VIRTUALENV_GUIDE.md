# 🔍 راهنمای پیدا کردن Virtual Environment در cPanel

این راهنما به شما کمک می‌کند که مسیر virtual environment را در cPanel پیدا کنید.

---

## 🎯 روش‌های پیدا کردن Virtual Environment

### روش 1: از طریق Python App در cPanel

1. وارد cPanel شوید
2. به **"Setup Python App"** بروید
3. Python App خود را پیدا کنید
4. روی **"Edit"** یا **"⚙️"** کلیک کنید
5. در صفحه تنظیمات، مسیر virtual environment را می‌بینید

**معمولاً به این شکل است:**
```
/home/username/virtualenv/public_html/3.10/
```

---

### روش 2: از طریق Terminal

```bash
# لیست کردن تمام virtual environments
ls -la ~/virtualenv/

# یا اگر در public_html است:
ls -la ~/virtualenv/public_html/

# پیدا کردن آخرین نسخه Python
ls -1 ~/virtualenv/public_html/ | sort -V | tail -1
```

**خروجی مثال:**
```
3.8
3.9
3.10
3.11
```

---

### روش 3: پیدا کردن خودکار

```bash
# پیدا کردن مسیر virtual environment
find ~ -name "activate" -path "*/virtualenv/*" 2>/dev/null | head -1

# یا برای public_html:
find ~/virtualenv/public_html -name "activate" 2>/dev/null | head -1
```

---

## ✅ فعال‌سازی Virtual Environment

بعد از پیدا کردن مسیر، می‌توانید فعال کنید:

### اگر نسخه Python را می‌دانید (مثلاً 3.10):

```bash
source ~/virtualenv/public_html/3.10/bin/activate
```

### اگر نسخه را نمی‌دانید:

```bash
# پیدا کردن آخرین نسخه
PYTHON_VERSION=$(ls -1 ~/virtualenv/public_html/ | sort -V | tail -1)
echo "Python version: $PYTHON_VERSION"

# فعال‌سازی
source ~/virtualenv/public_html/$PYTHON_VERSION/bin/activate
```

### یا به صورت یک خط:

```bash
source ~/virtualenv/public_html/$(ls -1 ~/virtualenv/public_html/ | sort -V | tail -1)/bin/activate
```

---

## 🔍 بررسی Virtual Environment فعال

بعد از فعال‌سازی، باید prompt تغییر کند:

**قبل از فعال‌سازی:**
```bash
[username@server ~]$
```

**بعد از فعال‌سازی:**
```bash
(3.10) [username@server ~]$
```

یا می‌توانید بررسی کنید:

```bash
which python
# باید مسیر virtual environment را نشان دهد:
# /home/username/virtualenv/public_html/3.10/bin/python

python --version
# باید نسخه Python را نشان دهد
```

---

## 🐛 مشکلات رایج

### مشکل 1: "No such file or directory"

**علت:** مسیر virtual environment اشتباه است یا وجود ندارد.

**راه‌حل:**
```bash
# بررسی وجود virtualenv
ls -la ~/virtualenv/

# اگر وجود ندارد، باید از Python App در cPanel ایجاد کنید
# یا خودتان ایجاد کنید:
cd ~/public_html
python3 -m venv venv
source venv/bin/activate
```

### مشکل 2: "Permission denied"

**راه‌حل:**
```bash
# بررسی دسترسی‌ها
ls -la ~/virtualenv/public_html/3.10/bin/activate

# اگر دسترسی ندارید:
chmod +x ~/virtualenv/public_html/3.10/bin/activate
```

### مشکل 3: Virtual Environment وجود ندارد

**راه‌حل:**
1. در cPanel به **"Setup Python App"** بروید
2. Python App را ایجاد کنید (اگر نکرده‌اید)
3. cPanel به صورت خودکار virtual environment ایجاد می‌کند

یا خودتان ایجاد کنید:

```bash
cd ~/public_html
python3 -m venv venv
source venv/bin/activate
```

---

## 📝 مثال کامل

```bash
# 1. پیدا کردن نسخه Python
cd ~
ls -la virtualenv/public_html/
# خروجی: 3.8  3.9  3.10

# 2. فعال‌سازی (فرض کنید 3.10 آخرین نسخه است)
source ~/virtualenv/public_html/3.10/bin/activate

# 3. بررسی
which python
# خروجی: /home/username/virtualenv/public_html/3.10/bin/python

python --version
# خروجی: Python 3.10.x

# 4. نصب dependencies
pip install -r requirements.txt
```

---

## 🚀 Script خودکار

می‌توانید یک script برای فعال‌سازی خودکار ایجاد کنید:

```bash
# ایجاد فایل activate_venv.sh
nano ~/activate_venv.sh
```

**محتوای script:**

```bash
#!/bin/bash

# پیدا کردن آخرین نسخه Python
if [ -d ~/virtualenv/public_html ]; then
    PYTHON_VERSION=$(ls -1 ~/virtualenv/public_html/ | sort -V | tail -1)
    VENV_PATH=~/virtualenv/public_html/$PYTHON_VERSION
elif [ -d ~/public_html/venv ]; then
    VENV_PATH=~/public_html/venv
else
    echo "❌ Virtual environment پیدا نشد!"
    exit 1
fi

echo "✅ Virtual environment پیدا شد: $VENV_PATH"
source $VENV_PATH/bin/activate
echo "✅ Virtual environment فعال شد!"
```

**استفاده:**
```bash
chmod +x ~/activate_venv.sh
source ~/activate_venv.sh
```

---

## 💡 نکات مهم

1. **همیشه قبل از نصب packages، virtual environment را فعال کنید**
2. **مسیر virtual environment در cPanel معمولاً:**
   ```
   /home/username/virtualenv/public_html/VERSION/
   ```
3. **اگر Python App در cPanel ایجاد کرده‌اید، virtual environment به صورت خودکار ایجاد می‌شود**
4. **می‌توانید از `venv` محلی هم استفاده کنید (در پوشه پروژه)**

---

## 🔄 Deactivate کردن

برای غیرفعال کردن virtual environment:

```bash
deactivate
```

---

**موفق باشید! 🎉**

اگر هنوز مشکل دارید، بگویید چه خطایی می‌گیرید.






