"""
اسکریپت ایجاد superuser برای Django
"""
import os
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sami.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


def create_superuser():
    """ایجاد superuser با دریافت اطلاعات از کاربر"""
    
    print("=" * 50)
    print("ایجاد Superuser برای پنل ادمین")
    print("=" * 50)
    
    # دریافت نام کاربری
    while True:
        username = input("\nنام کاربری (username): ").strip()
        if not username:
            print("⚠️  نام کاربری نمی‌تواند خالی باشد!")
            continue
        
        if User.objects.filter(username=username).exists():
            print(f"⚠️  کاربر با نام کاربری '{username}' قبلاً وجود دارد!")
            overwrite = input("آیا می‌خواهید آن را به superuser تبدیل کنید؟ (y/n): ").strip().lower()
            if overwrite == 'y':
                user = User.objects.get(username=username)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print(f"✅ کاربر '{username}' به superuser تبدیل شد!")
                return user
            else:
                continue
        break
    
    # دریافت ایمیل
    while True:
        email = input("ایمیل (email): ").strip().lower()
        if not email:
            email = None
            break
        
        if '@' not in email:
            print("⚠️  فرمت ایمیل معتبر نیست!")
            continue
        
        if User.objects.filter(email=email).exists():
            print(f"⚠️  کاربری با ایمیل '{email}' قبلاً وجود دارد!")
            continue
        break
    
    # دریافت رمز عبور
    while True:
        password = input("رمز عبور (password): ").strip()
        if not password:
            print("⚠️  رمز عبور نمی‌تواند خالی باشد!")
            continue
        
        if len(password) < 8:
            print("⚠️  رمز عبور باید حداقل 8 کاراکتر باشد!")
            continue
        
        password_confirm = input("تکرار رمز عبور: ").strip()
        if password != password_confirm:
            print("⚠️  رمز عبورها مطابقت ندارند!")
            continue
        break
    
    # دریافت نام و نام خانوادگی (اختیاری)
    first_name = input("نام (اختیاری): ").strip() or ""
    last_name = input("نام خانوادگی (اختیاری): ").strip() or ""
    
    # ایجاد superuser
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        # ایجاد Profile برای کاربر (اگر signal وجود نداشته باشد)
        Profile.objects.get_or_create(user=user)
        
        print("\n" + "=" * 50)
        print("✅ Superuser با موفقیت ایجاد شد!")
        print("=" * 50)
        print(f"نام کاربری: {user.username}")
        print(f"ایمیل: {user.email or 'تعیین نشده'}")
        print(f"نام کامل: {user.get_full_name() or 'تعیین نشده'}")
        print("\nحالا می‌توانید با این اطلاعات وارد پنل ادمین شوید:")
        print(f"URL: /admin/")
        
        return user
    
    except Exception as e:
        print(f"\n❌ خطا در ایجاد superuser: {str(e)}")
        return None


if __name__ == "__main__":
    create_superuser()



