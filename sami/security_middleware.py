"""
Additional security middleware for enhanced protection
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger("django.security")


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add additional security headers to responses
    """
    
    def process_response(self, request, response):
        # Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = getattr(settings, "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")
        
        # Remove server information
        if "Server" in response:
            del response["Server"]
        
        # Remove X-Powered-By if present
        if "X-Powered-By" in response:
            del response["X-Powered-By"]
        
        return response


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Additional session security measures
    """
    
    def process_request(self, request):
        # Regenerate session ID on login to prevent session fixation
        if request.user.is_authenticated and not request.session.get("_session_regenerated"):
            request.session.cycle_key()
            request.session["_session_regenerated"] = True
        return None


class IPWhitelistMiddleware(MiddlewareMixin):
    """
    Optional: Restrict admin access to specific IPs
    Only enable if ADMIN_IP_WHITELIST is set in settings
    """
    
    def process_request(self, request):
        admin_ip_whitelist = getattr(settings, "ADMIN_IP_WHITELIST", None)
        
        if admin_ip_whitelist and request.path.startswith(f"/{settings.ADMIN_URL}"):
            client_ip = self.get_client_ip(request)
            if client_ip not in admin_ip_whitelist:
                logger.warning(
                    f"Blocked admin access attempt from unauthorized IP: {client_ip}"
                )
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("Access denied")
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

