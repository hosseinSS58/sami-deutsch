from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام"))
    email = models.EmailField(verbose_name=_("ایمیل"))
    message = models.TextField(verbose_name=_("پیام"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("پیام تماس")
        verbose_name_plural = _("پیام‌های تماس")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"

from django.db import models

# Create your models here.
