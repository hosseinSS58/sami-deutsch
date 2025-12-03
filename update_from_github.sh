#!/bin/bash

# Script برای به‌روزرسانی پروژه از GitHub روی cPanel
# استفاده: ./update_from_github.sh

echo "🚀 شروع به‌روزرسانی پروژه..."

# رفتن به دایرکتوری پروژه
cd ~/public_html || exit 1

echo "📥 Pull کردن آخرین تغییرات از GitHub..."
git pull origin main

if [ $? -ne 0 ]; then
    echo "❌ خطا در pull کردن از GitHub!"
    exit 1
fi

echo "✅ تغییرات با موفقیت دریافت شد"

# فعال‌سازی virtual environment
echo "🐍 فعال‌سازی virtual environment..."
if [ -d ~/virtualenv/public_html ]; then
    # پیدا کردن آخرین نسخه Python
    PYTHON_VERSION=$(ls -1 ~/virtualenv/public_html/ | sort -V | tail -1)
    source ~/virtualenv/public_html/$PYTHON_VERSION/bin/activate
else
    echo "⚠️  Virtual environment پیدا نشد. از venv محلی استفاده می‌شود..."
    if [ -d venv ]; then
        source venv/bin/activate
    else
        echo "❌ Virtual environment پیدا نشد!"
        exit 1
    fi
fi

echo "📦 نصب/به‌روزرسانی dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ خطا در نصب dependencies!"
    exit 1
fi

echo "🔄 اجرای migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ خطا در اجرای migrations!"
    exit 1
fi

echo "📁 جمع‌آوری static files..."
python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo "❌ خطا در جمع‌آوری static files!"
    exit 1
fi

echo "🔄 Restart کردن Python App..."
touch passenger_wsgi.py

echo "✅ به‌روزرسانی با موفقیت انجام شد!"
echo "🌐 سایت باید در چند ثانیه به‌روز شود."







