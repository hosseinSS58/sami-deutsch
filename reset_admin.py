"""
اسکریپت ریست کردن رمز عبور ادمین
"""
import os
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sami.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# بررسی وجود کاربر admin
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123456')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.save()
    print("Password changed for admin user: admin123456")
except User.DoesNotExist:
    # ایجاد کاربر admin
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123456'
    )
    print("Admin user created with password: admin123456")
