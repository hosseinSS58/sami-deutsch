from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_category", "phone", "level", "newsletter_opt_in", "updated_at")
    list_filter = ("user_category", "level", "newsletter_opt_in", "updated_at")
    search_fields = ("user__username", "user__email", "phone")
    readonly_fields = ("updated_at",)
    
    fieldsets = (
        ("اطلاعات کاربر", {"fields": ("user", "user_category")}),
        ("اطلاعات تماس", {"fields": ("phone", "website")}),
        ("تنظیمات", {"fields": ("level", "newsletter_opt_in")}),
        ("اطلاعات تکمیلی", {"fields": ("bio", "avatar")}),
        ("اطلاعات سیستم", {"fields": ("updated_at",)}),
    )


# Unregister default UserAdmin and register custom one
# Note: UserAdmin is registered by default in django.contrib.auth
# We need to unregister it first if we want to customize it
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Already unregistered or not registered yet


# Security: Custom UserAdmin with enhanced security
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom UserAdmin with security enhancements"""
    
    list_display = ("username", "email", "first_name", "last_name", "get_user_category", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "profile__user_category", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login", "password")
    
    def get_user_category(self, obj):
        """نمایش دسته‌بندی کاربر در لیست"""
        if hasattr(obj, "profile"):
            return obj.profile.get_user_category_display()
        return "-"
    get_user_category.short_description = "دسته‌بندی"
    
    # Use BaseUserAdmin fieldsets but customize them
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name", "email")}),
        ("دسترسی‌ها", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("اطلاعات سیستم", {"fields": ("date_joined", "last_login")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related("profile")
