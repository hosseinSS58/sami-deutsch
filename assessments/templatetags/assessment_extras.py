"""
Template tags for assessments app
"""
import re
from django import template

register = template.Library()


@register.filter(name='extract_youtube_id')
def extract_youtube_id(url):
    """
    استخراج ID ویدیو از لینک یوتیوب در فرمت‌های مختلف
    """
    if not url:
        return None
    
    # الگوهای مختلف لینک یوتیوب
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


@register.filter(name='is_youtube_link')
def is_youtube_link(url):
    """
    بررسی اینکه آیا لینک یوتیوب است یا نه
    """
    return extract_youtube_id(url) is not None

