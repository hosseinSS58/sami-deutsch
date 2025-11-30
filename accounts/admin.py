from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "level", "newsletter_opt_in", "updated_at")
    list_filter = ("level", "newsletter_opt_in", "updated_at")
    search_fields = ("user__username", "user__email", "phone")
    readonly_fields = ("updated_at",)
    
    fieldsets = (
        ("اطلاعات کاربر", {"fields": ("user",)}),
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
    
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login", "password")
    
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
