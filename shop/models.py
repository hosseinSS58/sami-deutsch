from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("نام"), default="")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, default="")
    description = models.TextField(blank=True, verbose_name=_("توضیحات"), default="")
    price = models.PositiveIntegerField(verbose_name=_("قیمت به تومان"))
    is_active = models.BooleanField(default=True)
    cover = models.ImageField(upload_to="products/covers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("shop:detail", kwargs={"slug": self.slug})

    @property
    def slug_current(self) -> str:
        return self.slug


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", _("ایجاد شده")
        PAID = "paid", _("پرداخت شده")
        CANCELED = "canceled", _("لغو شده")

    full_name = models.CharField(max_length=150, verbose_name=_("نام و نام خانوادگی"))
    email = models.EmailField(verbose_name=_("ایمیل"))
    phone = models.CharField(max_length=20, verbose_name=_("تلفن"), blank=True)
    address = models.TextField(verbose_name=_("آدرس"), blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    total_amount = models.PositiveIntegerField(default=0, verbose_name=_("مبلغ کل"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش‌ها")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.full_name}"

    def recalculate_total(self) -> int:
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount"])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField()
    line_total = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم‌های سفارش")

    def __str__(self) -> str:
        return f"{self.product} x{self.quantity}"


# Create your models here.
