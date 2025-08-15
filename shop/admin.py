from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ("__str__", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("translations__name", "translations__description")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "status", "total_amount", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "email")
    readonly_fields = ("total_amount",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price", "line_total")


# Register your models here.
