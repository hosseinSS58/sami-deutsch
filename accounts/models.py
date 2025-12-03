from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Profile(models.Model):
    class LanguageLevel(models.TextChoices):
        A1 = "A1", "A1"
        A2 = "A2", "A2"
        B1 = "B1", "B1"
        B2 = "B2", "B2"
        C1 = "C1", "C1"

    class UserCategory(models.TextChoices):
        USER = "user", _("یوزر معمولی")
        ADMIN = "admin", _("مدیر سایت")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    level = models.CharField(max_length=2, choices=LanguageLevel.choices, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    newsletter_opt_in = models.BooleanField(default=False)
    user_category = models.CharField(
        max_length=10,
        choices=UserCategory.choices,
        default=UserCategory.USER,
        verbose_name=_("دسته‌بندی کاربر"),
        help_text=_("دسته‌بندی کاربر برای تعیین سطح دسترسی")
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"


# Create your models here.
