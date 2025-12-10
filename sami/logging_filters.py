"""
Logging filters to prevent sensitive data exposure
"""
import logging
import re


class SensitiveDataFilter(logging.Filter):
    """
    Filter to remove sensitive data from log messages
    """
    
    # Patterns to match sensitive data
    SENSITIVE_PATTERNS = [
        (r'password["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'password="***"'),
        (r'secret["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'secret="***"'),
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'api_key="***"'),
        (r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'token="***"'),
        (r'auth["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'auth="***"'),
        (r'authorization["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'authorization="***"'),
    ]
    
    def filter(self, record):
        """Filter log records to remove sensitive data"""
        if hasattr(record, 'msg') and record.msg:
            msg = str(record.msg)
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                msg = re.sub(pattern, replacement, msg, flags=re.IGNORECASE)
            record.msg = msg
        
        if hasattr(record, 'args') and record.args:
            args = list(record.args)
            for i, arg in enumerate(args):
                if isinstance(arg, str):
                    for pattern, replacement in self.SENSITIVE_PATTERNS:
                        args[i] = re.sub(pattern, replacement, arg, flags=re.IGNORECASE)
            record.args = tuple(args)
        
        return True










