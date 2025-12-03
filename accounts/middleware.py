"""
Security middleware for logging authentication events
"""
import logging
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

logger = logging.getLogger("accounts")


class SecurityLoggingMiddleware:
    """
    Middleware to log security-related events
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Connect signal handlers
        user_logged_in.connect(self.log_successful_login)
        user_logged_out.connect(self.log_logout)
        user_login_failed.connect(self.log_failed_login)
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def log_successful_login(self, sender, request, user, **kwargs):
        """Log successful login attempts"""
        ip_address = self.get_client_ip(request)
        logger.info(
            f"Successful login: user={user.username}, ip={ip_address}, "
            f"timestamp={timezone.now()}"
        )
    
    def log_logout(self, sender, request, user, **kwargs):
        """Log logout events"""
        ip_address = self.get_client_ip(request)
        logger.info(
            f"User logout: user={user.username}, ip={ip_address}, "
            f"timestamp={timezone.now()}"
        )
    
    def log_failed_login(self, sender, credentials, request, **kwargs):
        """Log failed login attempts"""
        ip_address = self.get_client_ip(request)
        username = credentials.get("username", "unknown")
        logger.warning(
            f"Failed login attempt: username={username}, ip={ip_address}, "
            f"timestamp={timezone.now()}"
        )
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip







