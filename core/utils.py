"""
Utility functions for core app
"""
import logging
import requests
import ipaddress
import re
from django.core.cache import cache

logger = logging.getLogger(__name__)


def validate_ip_address(ip_str):
    """
    Validate and clean IP address to prevent SSRF attacks
    
    Args:
        ip_str: IP address string (may contain port, path, etc.)
        
    Returns:
        Clean IP address string or None if invalid
    """
    if not ip_str:
        return None
    
    # Extract only IP part (remove port, path, etc.)
    ip_match = re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', str(ip_str))
    if not ip_match:
        return None
    
    clean_ip = ip_match.group(1)
    
    # Validate IP format
    try:
        ip_obj = ipaddress.ip_address(clean_ip)
        # Block private/internal IPs for security (SSRF prevention)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            return None
        return clean_ip
    except ValueError:
        return None


def get_country_from_ip(ip_address):
    """
    تشخیص کشور بر اساس IP address
    استفاده از ipapi.co API (رایگان تا 1000 درخواست در روز)
    
    Args:
        ip_address: آدرس IP
        
    Returns:
        کد کشور دو حرفی (مثل 'IR', 'US') یا رشته خالی در صورت خطا
    """
    if not ip_address or ip_address in ['127.0.0.1', 'localhost', '::1']:
        return ''
    
    # Validate and clean IP address to prevent SSRF
    clean_ip = validate_ip_address(ip_address)
    if not clean_ip:
        return ''
    
    # بررسی cache برای جلوگیری از درخواست‌های تکراری
    cache_key = f'country_ip_{clean_ip}'
    cached_country = cache.get(cache_key)
    if cached_country is not None:
        return cached_country
    
    try:
        # استفاده از ipapi.co API
        # می‌توانید از API های دیگر مثل ip-api.com هم استفاده کنید
        response = requests.get(
            f'https://ipapi.co/{clean_ip}/country_code/',
            timeout=3,
            headers={'User-Agent': 'Django-GeoIP/1.0'}
        )
        
        if response.status_code == 200:
            country_code = response.text.strip()
            # اعتبارسنجی کد کشور (باید 2 حرف باشد)
            if len(country_code) == 2 and country_code.isalpha():
                # ذخیره در cache برای 24 ساعت
                cache.set(cache_key, country_code, 86400)
                return country_code
        
        # در صورت خطا، از API جایگزین استفاده کن
        return _get_country_from_ip_api(clean_ip)
        
    except Exception as e:
        logger.warning(f"خطا در تشخیص کشور برای IP {clean_ip}: {str(e)}")
        # تلاش با API جایگزین
        try:
            return _get_country_from_ip_api(clean_ip)
        except Exception:
            return ''


def _get_country_from_ip_api(ip_address):
    """
    API جایگزین: ip-api.com
    """
    # Validate IP before making request
    clean_ip = validate_ip_address(ip_address)
    if not clean_ip:
        return ''
    
    try:
        response = requests.get(
            f'http://ip-api.com/json/{clean_ip}?fields=countryCode',
            timeout=3
        )
        
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('countryCode', '')
            if len(country_code) == 2 and country_code.isalpha():
                cache_key = f'country_ip_{clean_ip}'
                cache.set(cache_key, country_code, 86400)
                return country_code
    except Exception as e:
        logger.warning(f"خطا در API جایگزین برای IP {clean_ip}: {str(e)}")
    
    return ''


def detect_device_type(user_agent):
    """
    تشخیص نوع دستگاه بر اساس User Agent
    
    Args:
        user_agent: رشته User Agent
        
    Returns:
        'mobile', 'tablet', 'desktop', یا 'unknown'
    """
    if not user_agent:
        return 'unknown'
    
    user_agent_lower = user_agent.lower()
    
    # تشخیص موبایل
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipod', 'blackberry', 
        'windows phone', 'opera mini', 'opera mobi', 'iemobile',
        'mobile safari', 'webos', 'palm', 'symbian', 'nokia',
        'fennec', 'maemo', 'mib', 'kindle', 'silk', 'miui',
        'huawei', 'samsung', 'lg', 'sony', 'motorola', 'xiaomi',
        'oneplus', 'oppo', 'vivo', 'realme', 'meizu', 'zte'
    ]
    
    # تشخیص تبلت
    tablet_keywords = [
        'tablet', 'ipad', 'playbook', 'kindle fire', 'nexus 7',
        'nexus 10', 'galaxy tab', 'surface', 'xoom', 'touchpad'
    ]
    
    # بررسی تبلت
    for keyword in tablet_keywords:
        if keyword in user_agent_lower:
            return 'tablet'
    
    # بررسی موبایل
    for keyword in mobile_keywords:
        if keyword in user_agent_lower:
            return 'mobile'
    
    # اگر هیچکدام نبود، دسکتاپ است
    return 'desktop'


def get_device_type_display(device_type):
    """
    تبدیل نوع دستگاه به نام فارسی
    """
    device_names = {
        'mobile': 'موبایل',
        'tablet': 'تبلت',
        'desktop': 'دسکتاپ',
        'unknown': 'نامشخص'
    }
    return device_names.get(device_type, 'نامشخص')


def get_country_name(country_code):
    """
    تبدیل کد کشور به نام کشور (فارسی)
    """
    if not country_code:
        return 'نامشخص'
    
    country_names = {
        'IR': 'ایران',
        'US': 'ایالات متحده',
        'GB': 'انگلستان',
        'DE': 'آلمان',
        'FR': 'فرانسه',
        'CA': 'کانادا',
        'AU': 'استرالیا',
        'TR': 'ترکیه',
        'AE': 'امارات متحده عربی',
        'SA': 'عربستان سعودی',
        'IQ': 'عراق',
        'AF': 'افغانستان',
        'PK': 'پاکستان',
        'IN': 'هند',
        'CN': 'چین',
        'JP': 'ژاپن',
        'KR': 'کره جنوبی',
        'RU': 'روسیه',
        'IT': 'ایتالیا',
        'ES': 'اسپانیا',
        'NL': 'هلند',
        'BE': 'بلژیک',
        'CH': 'سوئیس',
        'AT': 'اتریش',
        'SE': 'سوئد',
        'NO': 'نروژ',
        'DK': 'دانمارک',
        'FI': 'فنلاند',
        'PL': 'لهستان',
        'CZ': 'جمهوری چک',
        'GR': 'یونان',
        'PT': 'پرتغال',
        'IE': 'ایرلند',
        'NZ': 'نیوزیلند',
        'BR': 'برزیل',
        'MX': 'مکزیک',
        'AR': 'آرژانتین',
        'CL': 'شیلی',
        'CO': 'کلمبیا',
        'PE': 'پرو',
        'VE': 'ونزوئلا',
        'EG': 'مصر',
        'ZA': 'آفریقای جنوبی',
        'NG': 'نیجریه',
        'KE': 'کنیا',
        'MA': 'مراکش',
        'TN': 'تونس',
        'DZ': 'الجزایر',
        'LY': 'لیبی',
        'SD': 'سودان',
        'ET': 'اتیوپی',
        'GH': 'غنا',
        'UG': 'اوگاندا',
        'TZ': 'تانزانیا',
        'ZM': 'زامبیا',
        'ZW': 'زیمبابوه',
        'BW': 'بوتسوانا',
        'NA': 'نامیبیا',
        'MU': 'موریس',
        'SC': 'سیشل',
        'MV': 'مالدیو',
        'LK': 'سری‌لانکا',
        'BD': 'بنگلادش',
        'MM': 'میانمار',
        'TH': 'تایلند',
        'VN': 'ویتنام',
        'PH': 'فیلیپین',
        'ID': 'اندونزی',
        'MY': 'مالزی',
        'SG': 'سنگاپور',
        'BN': 'برونئی',
        'KH': 'کامبوج',
        'LA': 'لائوس',
        'MN': 'مغولستان',
        'KZ': 'قزاقستان',
        'UZ': 'ازبکستان',
        'TM': 'ترکمنستان',
        'TJ': 'تاجیکستان',
        'KG': 'قرقیزستان',
        'GE': 'گرجستان',
        'AM': 'ارمنستان',
        'AZ': 'آذربایجان',
        'BY': 'بلاروس',
        'UA': 'اوکراین',
        'MD': 'مولداوی',
        'RO': 'رومانی',
        'BG': 'بلغارستان',
        'RS': 'صربستان',
        'HR': 'کرواسی',
        'SI': 'اسلوونی',
        'SK': 'اسلواکی',
        'HU': 'مجارستان',
        'LT': 'لیتوانی',
        'LV': 'لتونی',
        'EE': 'استونی',
        'IS': 'ایسلند',
        'LU': 'لوکزامبورگ',
        'MT': 'مالت',
        'CY': 'قبرس',
        'IL': 'اسرائیل',
        'JO': 'اردن',
        'LB': 'لبنان',
        'SY': 'سوریه',
        'YE': 'یمن',
        'OM': 'عمان',
        'QA': 'قطر',
        'BH': 'بحرین',
        'KW': 'کویت',
        'IQ': 'عراق',
        'AZ': 'آذربایجان',
        'AM': 'ارمنستان',
        'GE': 'گرجستان',
        'UZ': 'ازبکستان',
        'TM': 'ترکمنستان',
        'TJ': 'تاجیکستان',
        'KZ': 'قزاقستان',
        'KG': 'قرقیزستان',
        'MN': 'مغولستان',
        'KP': 'کره شمالی',
        'TW': 'تایوان',
        'HK': 'هنگ کنگ',
        'MO': 'ماکائو',
        'MY': 'مالزی',
        'SG': 'سنگاپور',
        'ID': 'اندونزی',
        'PH': 'فیلیپین',
        'VN': 'ویتنام',
        'TH': 'تایلند',
        'MM': 'میانمار',
        'BD': 'بنگلادش',
        'LK': 'سری‌لانکا',
        'MV': 'مالدیو',
        'NP': 'نپال',
        'BT': 'بوتان',
        'MV': 'مالدیو',
        'SC': 'سیشل',
        'MU': 'موریس',
        'RE': 'رئونیون',
        'YT': 'مایوت',
        'KM': 'کومور',
        'DJ': 'جیبوتی',
        'ER': 'اریتره',
        'SO': 'سومالی',
        'SS': 'سودان جنوبی',
        'CF': 'جمهوری آفریقای مرکزی',
        'TD': 'چاد',
        'CM': 'کامرون',
        'GQ': 'گینه استوایی',
        'GA': 'گابن',
        'CG': 'کنگو',
        'CD': 'جمهوری دموکراتیک کنگو',
        'AO': 'آنگولا',
        'ZM': 'زامبیا',
        'MW': 'مالاوی',
        'MZ': 'موزامبیک',
        'MG': 'ماداگاسکار',
        'MU': 'موریس',
        'SC': 'سیشل',
        'KM': 'کومور',
        'YT': 'مایوت',
        'RE': 'رئونیون',
        'ZW': 'زیمبابوه',
        'BW': 'بوتسوانا',
        'NA': 'نامیبیا',
        'LS': 'لسوتو',
        'SZ': 'سوازیلند',
        'ST': 'سائوتومه و پرنسیپ',
        'CV': 'کیپ ورد',
        'GW': 'گینه بیسائو',
        'GN': 'گینه',
        'SL': 'سیرالئون',
        'LR': 'لیبریا',
        'CI': 'ساحل عاج',
        'BF': 'بورکینافاسو',
        'ML': 'مالی',
        'NE': 'نیجر',
        'TD': 'چاد',
        'SD': 'سودان',
        'ET': 'اتیوپی',
        'ER': 'اریتره',
        'DJ': 'جیبوتی',
        'SO': 'سومالی',
        'KE': 'کنیا',
        'UG': 'اوگاندا',
        'RW': 'روآندا',
        'BI': 'بوروندی',
        'TZ': 'تانزانیا',
        'MZ': 'موزامبیک',
        'MW': 'مالاوی',
        'ZM': 'زامبیا',
        'ZW': 'زیمبابوه',
        'BW': 'بوتسوانا',
        'NA': 'نامیبیا',
        'LS': 'لسوتو',
        'SZ': 'سوازیلند',
        'ZA': 'آفریقای جنوبی',
        'MG': 'ماداگاسکار',
        'MU': 'موریس',
        'SC': 'سیشل',
        'KM': 'کومور',
        'YT': 'مایوت',
        'RE': 'رئونیون',
        'MV': 'مالدیو',
        'LK': 'سری‌لانکا',
        'BD': 'بنگلادش',
        'BT': 'بوتان',
        'NP': 'نپال',
        'PK': 'پاکستان',
        'AF': 'افغانستان',
        'TJ': 'تاجیکستان',
        'UZ': 'ازبکستان',
        'TM': 'ترکمنستان',
        'KZ': 'قزاقستان',
        'KG': 'قرقیزستان',
        'MN': 'مغولستان',
        'CN': 'چین',
        'KP': 'کره شمالی',
        'KR': 'کره جنوبی',
        'JP': 'ژاپن',
        'TW': 'تایوان',
        'HK': 'هنگ کنگ',
        'MO': 'ماکائو',
        'VN': 'ویتنام',
        'LA': 'لائوس',
        'KH': 'کامبوج',
        'TH': 'تایلند',
        'MM': 'میانمار',
        'MY': 'مالزی',
        'SG': 'سنگاپور',
        'BN': 'برونئی',
        'ID': 'اندونزی',
        'TL': 'تیمور شرقی',
        'PH': 'فیلیپین',
        'PG': 'پاپوآ نیو گینه',
        'SB': 'جزایر سلیمان',
        'VU': 'وانواتو',
        'NC': 'کالدونیای جدید',
        'PF': 'پلی‌نزی فرانسه',
        'WS': 'ساموآ',
        'TO': 'تونگا',
        'FJ': 'فیجی',
        'KI': 'کیریباتی',
        'TV': 'تووالو',
        'NR': 'نائورو',
        'PW': 'پالائو',
        'FM': 'میکرونزی',
        'MH': 'جزایر مارشال',
        'GU': 'گوام',
        'MP': 'جزایر ماریانای شمالی',
        'AS': 'ساموآی آمریکا',
        'CK': 'جزایر کوک',
        'NU': 'نیوئه',
        'TK': 'توکلائو',
        'PN': 'پیتکرن',
        'NF': 'جزیره نورفولک',
        'CX': 'جزیره کریسمس',
        'CC': 'جزایر کوکوس',
        'HM': 'جزیره هرد و جزایر مک‌دونالد',
        'AQ': 'جنوبگان',
        'GS': 'جورجیا جنوبی و جزایر ساندویچ جنوبی',
        'FK': 'جزایر فالکلند',
        'BV': 'جزیره بووت',
        'TF': 'سرزمین‌های جنوبی و جنوبگان فرانسه',
        'IO': 'قلمرو اقیانوس هند بریتانیا',
        'SH': 'سنت هلنا',
        'AC': 'جزیره اسنشن',
        'TA': 'تریستان دا کونا',
        'EH': 'صحرای غربی',
        'PS': 'فلسطين',
        'AX': 'جزایر آلاند',
        'FO': 'جزایر فارو',
        'GI': 'جبل الطارق',
        'AD': 'آندورا',
        'MC': 'موناکو',
        'SM': 'سان مارینو',
        'VA': 'واتیکان',
        'LI': 'لیختن‌اشتاین',
        'JE': 'جرزی',
        'GG': 'گرنزی',
        'IM': 'جزیره من',
        'SJ': 'اسوالبارد و یان ماین',
        'GL': 'گرینلند',
        'PM': 'سنت پیر و میکلون',
        'BL': 'سنت بارتلمی',
        'MF': 'سنت مارتین',
        'SX': 'سینت مارتن',
        'CW': 'کوراسائو',
        'AW': 'آروبا',
        'BQ': 'بونیر',
        'VG': 'جزایر ویرجین بریتانیا',
        'VI': 'جزایر ویرجین ایالات متحده',
        'PR': 'پورتوریکو',
        'GP': 'گوادلوپ',
        'MQ': 'مارتینیک',
        'DM': 'دومینیکا',
        'GD': 'گرنادا',
        'LC': 'سنت لوسیا',
        'VC': 'سنت وینسنت و گرنادین‌ها',
        'BB': 'باربادوس',
        'TT': 'ترینیداد و توباگو',
        'AG': 'آنتیگوا و باربودا',
        'KN': 'سنت کیتس و نویس',
        'BS': 'باهاما',
        'CU': 'کوبا',
        'JM': 'جامائیکا',
        'HT': 'هائیتی',
        'DO': 'جمهوری دومینیکن',
        'BZ': 'بلیز',
        'GT': 'گواتمالا',
        'SV': 'السالوادور',
        'HN': 'هندوراس',
        'NI': 'نیکاراگوئه',
        'CR': 'کاستاریکا',
        'PA': 'پاناما',
        'CO': 'کلمبیا',
        'VE': 'ونزوئلا',
        'GY': 'گویان',
        'SR': 'سورینام',
        'GF': 'گویان فرانسه',
        'UY': 'اروگوئه',
        'PY': 'پاراگوئه',
        'BO': 'بولیوی',
        'PE': 'پرو',
        'EC': 'اکوادور',
        'CL': 'شیلی',
        'AR': 'آرژانتین',
        'FK': 'جزایر فالکلند',
        'GS': 'جورجیا جنوبی و جزایر ساندویچ جنوبی',
        'BV': 'جزیره بووت',
        'TF': 'سرزمین‌های جنوبی و جنوبگان فرانسه',
        'HM': 'جزیره هرد و جزایر مک‌دونالد',
        'AQ': 'جنوبگان',
        'PN': 'پیتکرن',
        'NU': 'نیوئه',
        'TK': 'توکلائو',
        'CK': 'جزایر کوک',
        'AS': 'ساموآی آمریکا',
        'MP': 'جزایر ماریانای شمالی',
        'GU': 'گوام',
        'MH': 'جزایر مارشال',
        'FM': 'میکرونزی',
        'PW': 'پالائو',
        'NR': 'نائورو',
        'TV': 'تووالو',
        'KI': 'کیریباتی',
        'FJ': 'فیجی',
        'TO': 'تونگا',
        'WS': 'ساموآ',
        'PF': 'پلی‌نزی فرانسه',
        'NC': 'کالدونیای جدید',
        'VU': 'وانواتو',
        'SB': 'جزایر سلیمان',
        'PG': 'پاپوآ نیو گینه',
        'TL': 'تیمور شرقی',
        'ID': 'اندونزی',
        'BN': 'برونئی',
        'SG': 'سنگاپور',
        'MY': 'مالزی',
        'MM': 'میانمار',
        'TH': 'تایلند',
        'KH': 'کامبوج',
        'LA': 'لائوس',
        'VN': 'ویتنام',
        'MO': 'ماکائو',
        'HK': 'هنگ کنگ',
        'TW': 'تایوان',
        'JP': 'ژاپن',
        'KR': 'کره جنوبی',
        'KP': 'کره شمالی',
        'MN': 'مغولستان',
        'KZ': 'قزاقستان',
        'KG': 'قرقیزستان',
        'TJ': 'تاجیکستان',
        'TM': 'ترکمنستان',
        'UZ': 'ازبکستان',
        'AF': 'افغانستان',
        'PK': 'پاکستان',
        'NP': 'نپال',
        'BT': 'بوتان',
        'BD': 'بنگلادش',
        'LK': 'سری‌لانکا',
        'MV': 'مالدیو',
        'IN': 'هند',
        'CN': 'چین',
        'MO': 'ماکائو',
        'HK': 'هنگ کنگ',
        'TW': 'تایوان',
        'JP': 'ژاپن',
        'KR': 'کره جنوبی',
        'KP': 'کره شمالی',
        'MN': 'مغولستان',
        'KZ': 'قزاقستان',
        'KG': 'قرقیزستان',
        'TJ': 'تاجیکستان',
        'TM': 'ترکمنستان',
        'UZ': 'ازبکستان',
        'AF': 'افغانستان',
        'PK': 'پاکستان',
        'NP': 'نپال',
        'BT': 'بوتان',
        'BD': 'بنگلادش',
        'LK': 'سری‌لانکا',
        'MV': 'مالدیو',
        'IN': 'هند',
    }
    
    return country_names.get(country_code.upper(), country_code.upper())

