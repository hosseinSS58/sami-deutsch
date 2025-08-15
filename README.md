# 🌟 Sami Deutsch - سیستم آموزش زبان آلمانی

## 📖 درباره پروژه

**Sami Deutsch** یک پلتفرم جامع آموزش زبان آلمانی است که با استفاده از Django ساخته شده است. این سیستم شامل ویژگی‌های متنوعی برای یادگیری موثر زبان آلمانی می‌باشد.

## ✨ ویژگی‌های کلیدی

- 🎓 **سیستم دوره‌ها**: مدیریت کامل دوره‌های آموزشی
- 📚 **سیستم ارزیابی**: آزمون‌ها و ارزیابی‌های تعاملی
- 🛒 **فروشگاه آنلاین**: خرید کتاب‌ها و منابع آموزشی
- 📝 **سیستم بلاگ**: مقالات آموزشی و اخبار
- 🔍 **جستجوی پیشرفته**: جستجو در محتوای آموزشی
- 👤 **مدیریت کاربران**: سیستم احراز هویت و پروفایل
- 🎨 **قالب‌بندی زیبا**: طراحی مدرن و ریسپانسیو

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- pip
- virtual environment

### مراحل نصب

1. **کلون کردن مخزن**
```bash
git clone https://github.com/yourusername/sami-deutsch.git
cd sami-deutsch
```

2. **ایجاد محیط مجازی**
```bash
python -m venv .venv
# در Windows:
.venv\Scripts\activate
# در Linux/Mac:
source .venv/bin/activate
```

3. **نصب وابستگی‌ها**
```bash
pip install -r requirements.txt
```

4. **تنظیمات پایگاه داده**
```bash
python manage.py migrate
```

5. **ایجاد کاربر ادمین**
```bash
python manage.py createsuperuser
```

6. **اجرای سرور توسعه**
```bash
python manage.py runserver
```

## 🏗️ ساختار پروژه

```
sami-deutsch/
├── accounts/          # مدیریت کاربران و احراز هویت
├── assessments/       # سیستم ارزیابی و آزمون
├── blog/             # سیستم بلاگ
├── courses/          # مدیریت دوره‌ها
├── shop/             # فروشگاه آنلاین
├── search/           # سیستم جستجو
├── core/             # هسته اصلی پروژه
├── templates/        # قالب‌های HTML
├── static/           # فایل‌های استاتیک
└── media/            # فایل‌های آپلود شده
```

## 🛠️ تکنولوژی‌های استفاده شده

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (توسعه) / PostgreSQL (تولید)
- **Authentication**: Django Allauth
- **Forms**: Django Crispy Forms
- **Editor**: CKEditor
- **Deployment**: Gunicorn + Whitenoise

## 📱 ویژگی‌های ریسپانسیو

- طراحی کاملاً ریسپانسیو برای تمام دستگاه‌ها
- بهینه‌سازی برای موبایل، تبلت و دسکتاپ
- رابط کاربری مدرن و جذاب

## 🔧 تنظیمات محیط

برای تنظیمات محیط، فایل `.env` را در ریشه پروژه ایجاد کنید:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📊 پایگاه داده

پروژه از SQLite برای توسعه استفاده می‌کند. برای تولید، PostgreSQL توصیه می‌شود.

## 🚀 استقرار (Deployment)

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### VPS/Server
```bash
# نصب Gunicorn
pip install gunicorn

# اجرا
gunicorn sami.wsgi:application
```

## 🤝 مشارکت

مشارکت‌های شما در بهبود این پروژه بسیار ارزشمند است!

1. Fork کنید
2. یک branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. به branch اصلی push کنید (`git push origin feature/amazing-feature`)
5. یک Pull Request ایجاد کنید

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

## 📞 پشتیبانی

برای سوالات و پشتیبانی:
- 📧 ایمیل: support@samideutsch.com
- 🐛 گزارش باگ: [Issues](https://github.com/yourusername/sami-deutsch/issues)

## 🙏 تشکر

از تمام افرادی که در توسعه این پروژه مشارکت داشته‌اند، تشکر می‌کنیم.

---

⭐ اگر این پروژه برایتان مفید بود، لطفاً آن را ستاره‌دار کنید!
