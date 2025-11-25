"""
ابزارهای کمکی برای استخراج اطلاعات از ویدیوهای یوتیوب
"""
import re
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs
from django.utils.text import slugify
from django.core.files.base import ContentFile
from io import BytesIO


def extract_youtube_id(url: str) -> Optional[str]:
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


def extract_youtube_metadata(url: str) -> Dict:
    """
    استخراج اطلاعات کامل ویدیو از یوتیوب با استفاده از yt-dlp
    
    Returns:
        dict: شامل title, description, duration, thumbnail_url, channel, etc.
    """
    # Lazy import - فقط وقتی که نیاز است
    try:
        import yt_dlp
    except ImportError:
        return {
            'success': False,
            'error': 'yt-dlp نصب نشده است. لطفاً آن را نصب کنید: pip install yt-dlp'
        }
    
    video_id = extract_youtube_id(url)
    if not video_id:
        return {
            'error': 'لینک یوتیوب معتبر نیست',
            'success': False
        }
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # تبدیل duration از ثانیه به دقیقه
            duration_seconds = info.get('duration', 0)
            duration_minutes = duration_seconds // 60 if duration_seconds else 0
            
            # استخراج thumbnail با کیفیت بالا
            thumbnail_url = None
            thumbnails = info.get('thumbnails', [])
            if thumbnails:
                # انتخاب thumbnail با بالاترین کیفیت
                thumbnail_url = thumbnails[-1].get('url') if thumbnails else None
            
            # اگر thumbnail پیدا نشد، از فرمت استاندارد استفاده کن
            if not thumbnail_url:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            return {
                'success': True,
                'youtube_id': video_id,
                'youtube_url': url,
                'title': info.get('title', ''),
                'description': info.get('description', '') or '',
                'duration_seconds': duration_seconds,
                'duration_minutes': duration_minutes,
                'thumbnail_url': thumbnail_url,
                'channel': info.get('channel', ''),
                'channel_id': info.get('channel_id', ''),
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'upload_date': info.get('upload_date', ''),
                'tags': info.get('tags', []),
                'categories': info.get('categories', []),
            }
    
    except yt_dlp.utils.DownloadError as e:
        return {
            'success': False,
            'error': f'خطا در دریافت اطلاعات: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'خطای غیرمنتظره: {str(e)}'
        }


def download_thumbnail(thumbnail_url: str, video_id: str) -> Optional[ContentFile]:
    """
    دانلود thumbnail از یوتیوب و تبدیل آن به ContentFile
    
    Args:
        thumbnail_url: URL تصویر thumbnail
        video_id: ID ویدیو یوتیوب
    
    Returns:
        ContentFile: فایل تصویر برای ذخیره در ImageField
    """
    try:
        import requests
    except ImportError:
        print("requests نصب نشده است. لطفاً آن را نصب کنید: pip install requests")
        return None
    
    try:
        response = requests.get(thumbnail_url, timeout=10, stream=True)
        response.raise_for_status()
        
        # خواندن محتوای تصویر
        image_data = BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            image_data.write(chunk)
        image_data.seek(0)
        
        # تبدیل به ContentFile
        filename = f"youtube_{video_id}_cover.jpg"
        return ContentFile(image_data.read(), name=filename)
    
    except Exception as e:
        print(f"خطا در دانلود thumbnail: {str(e)}")
        return None


def create_video_from_youtube(url: str, **kwargs) -> tuple:
    """
    ایجاد یک Video object از لینک یوتیوب
    
    Args:
        url: لینک ویدیو یوتیوب
        **kwargs: مقادیر اضافی برای override کردن فیلدهای ویدیو
            مثل level, topic, difficulty, is_free, etc.
    
    Returns:
        tuple: (video_object, youtube_link_object, success_message)
    """
    from .models import Video, YouTubeLink
    
    # استخراج اطلاعات
    metadata = extract_youtube_metadata(url)
    
    if not metadata.get('success'):
        return None, None, metadata.get('error', 'خطا در استخراج اطلاعات')
    
    # استخراج YouTube ID برای slug
    youtube_id = metadata.get('youtube_id')
    
    # ایجاد slug ساده از YouTube ID
    # فرمت: yt-{youtube_id}
    base_slug = f"yt-{youtube_id}"
    
    # بررسی یکتایی slug
    slug = base_slug
    counter = 1
    while Video.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
        if counter > 9999:  # جلوگیری از حلقه بی‌نهایت
            slug = f"{base_slug}-{hash(url) % 10000}"
            break
    
    # آماده‌سازی عنوان
    title = metadata.get('title', 'ویدیو جدید')
    if not title or title.strip() == '':
        title = 'ویدیو جدید'
    
    # محدود کردن طول عنوان به max_length (200)
    if len(title) > 200:
        title = title[:197] + '...'
    
    # آماده‌سازی توضیحات
    description = kwargs.get('description') or metadata.get('description', '')
    # TextField محدودیت طول ندارد، اما برای نمایش بهتر، اول 2000 کاراکتر را نگه می‌داریم
    if description and len(description) > 2000:
        description = description[:2000] + '...'
    
    # ایجاد Video object (بدون cover برای حالا)
    video = Video(
        title=kwargs.get('title') or title,
        description=description,
        slug=slug,
        level=kwargs.get('level', 'A1'),
        topic=kwargs.get('topic', 'grammar'),
        difficulty=kwargs.get('difficulty', 'beginner'),
        duration_minutes=kwargs.get('duration_minutes') or metadata.get('duration_minutes', 0),
        is_featured=kwargs.get('is_featured', False),
        is_free=kwargs.get('is_free', True),
    )
    video.save()
    
    # دانلود و ذخیره thumbnail به عنوان cover
    thumbnail_url = metadata.get('thumbnail_url')
    if thumbnail_url:
        thumbnail_file = download_thumbnail(thumbnail_url, youtube_id)
        if thumbnail_file:
            video.cover.save(
                f"youtube_{youtube_id}_cover.jpg",
                thumbnail_file,
                save=True
            )
    
    # آماده‌سازی عنوان و توضیحات برای YouTubeLink
    yt_title = metadata.get('title', '')
    if len(yt_title) > 200:
        yt_title = yt_title[:197] + '...'
    
    yt_description = metadata.get('description', '')
    if len(yt_description) > 1000:
        yt_description = yt_description[:1000] + '...'
    
    # ایجاد YouTubeLink object
    youtube_link = YouTubeLink(
        video=video,
        title=yt_title,
        youtube_url=url,
        description=yt_description,
        duration_minutes=metadata.get('duration_minutes', 0),
        order=0,
        is_active=True,
    )
    youtube_link.save()
    
    success_message = f'ویدیو "{video.title}" با موفقیت ایجاد شد.'
    
    return video, youtube_link, success_message
