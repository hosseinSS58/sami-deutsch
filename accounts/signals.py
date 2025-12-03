from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance)
        # تنظیم دسته‌بندی پیش‌فرض به یوزر معمولی
        if not profile.user_category:
            profile.user_category = Profile.UserCategory.USER
            profile.save()




