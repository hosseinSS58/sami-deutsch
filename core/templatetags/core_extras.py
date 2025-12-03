"""
Template tags for core app
"""
from django import template
from core.utils import get_country_name, get_device_type_display

register = template.Library()


@register.filter(name='get_country_name')
def get_country_name_filter(country_code):
    """
    تبدیل کد کشور به نام کشور (فارسی)
    """
    if not country_code:
        return 'نامشخص'
    return get_country_name(country_code)


@register.filter(name='get_device_type_display')
def get_device_type_display_filter(device_type):
    """
    تبدیل نوع دستگاه به نام فارسی
    """
    return get_device_type_display(device_type)

