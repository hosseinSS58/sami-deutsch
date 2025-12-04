"""
Admin security enhancements
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import logging

logger = logging.getLogger("django.security")


class SecureAdminSite(AdminSite):
    """
    Enhanced admin site with additional security features
    """
    
    def login(self, request, extra_context=None):
        """
        Override login to add security logging
        """
        # Log admin login attempts
        if request.method == "POST":
            username = request.POST.get("username", "unknown")
            ip_address = self.get_client_ip(request)
            logger.info(
                f"Admin login attempt: username={username}, ip={ip_address}"
            )
        
        return super().login(request, extra_context)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# Optional: Use secure admin site (uncomment to enable)
# admin_site = SecureAdminSite(name="secure_admin")
# Then use admin_site.register() instead of admin.site.register()








