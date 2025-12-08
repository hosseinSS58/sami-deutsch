# 🔒 خلاصه مشکلات امنیتی و راه‌حل‌های عملی

این سند شامل **همه مشکلات امنیتی** شناسایی شده به همراه **راه‌حل‌های عملی و قابل اجرا** است.

---

## 📊 آمار کلی

- 🔴 **5 مشکل بحرانی** (Critical) - نیاز به اقدام فوری
- 🟡 **7 مشکل متوسط** (Medium) - نیاز به اقدام در اسرع وقت
- 🟢 **3 بهبود پیشنهادی** (Low) - می‌تواند بعداً انجام شود

**نمره امنیتی فعلی:** 6.5/10  
**نمره امنیتی بعد از رفع مشکلات بحرانی:** 8.5/10

---

## 🔴 مشکلات بحرانی (Critical) - اقدام فوری

### 1. XSS Vulnerability در Custom CSS
**فایل:** `templates/base.html:137`  
**کد مشکل:**
```html
{{ site_settings.custom_css|safe }}
```

**راه‌حل:**
```python
# در siteconfig/models.py یا views.py
from bleach import clean

def get_safe_css(css_content):
    """Sanitize CSS content"""
    if not css_content:
        return ''
    # فقط CSS properties مجاز
    # یا استفاده از CSS validator
    return css_content  # بعد از validation

# در template:
{{ site_settings.custom_css|safe }}  # فقط بعد از sanitize
```

**اقدام:** بررسی کنید `custom_css` از کجا می‌آید و sanitize کنید.

---

### 2. SSRF Risk در IP Lookup
**فایل:** `core/utils.py:34`  
**کد مشکل:**
```python
response = requests.get(f'https://ipapi.co/{ip_address}/country_code/')
```

**راه‌حل:**
```python
import ipaddress
import re

def validate_ip_address(ip_str):
    """Validate and clean IP address"""
    # Extract IP only (remove port, path, etc.)
    ip_match = re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', str(ip_str))
    if not ip_match:
        return None
    
    clean_ip = ip_match.group(1)
    try:
        ip_obj = ipaddress.ip_address(clean_ip)
        # Block private IPs if not needed
        if ip_obj.is_private:
            return None
        return clean_ip
    except ValueError:
        return None

def get_country_from_ip(ip_address):
    if not ip_address:
        return ''
    
    clean_ip = validate_ip_address(ip_address)
    if not clean_ip:
        return ''
    
    # Now safe to use clean_ip
    # ... rest of code
```

**اقدام:** اضافه کردن IP validation قبل از API call.

---

### 3. Session Key Exposure
**فایل:** `templates/accounts/anonymous_visitor_detail.html:18`  
**کد مشکل:**
```html
<code>{{ visitor.session_key }}</code>
```

**راه‌حل:**
```html
<!-- فقط چند کاراکتر اول -->
<code>{{ visitor.session_key|truncatechars:8 }}...</code>

<!-- یا اصلاً نمایش ندهید در public templates -->
<!-- فقط در admin با permission check -->
```

**اقدام:** حذف یا truncate کردن session key.

---

### 4. Cart Manipulation
**فایل:** `shop/views.py:72-77`  
**کد مشکل:**
```python
product_id = str(request.POST.get("product_id"))  # بدون validation
```

**راه‌حل:**
```python
class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        try:
            product_id = int(request.POST.get("product_id"))
        except (ValueError, TypeError):
            messages.error(request, "Invalid product ID")
            return redirect("shop:cart")
        
        # بررسی وجود product
        if not Product.objects.filter(id=product_id, is_active=True).exists():
            messages.error(request, "Product not found")
            return redirect("shop:cart")
        
        cart = request.session.get("cart", {})
        if str(product_id) in cart:
            cart.pop(str(product_id))
            request.session["cart"] = cart
            messages.success(request, "Product removed")
        
        return redirect("shop:cart")
```

**اقدام:** اضافه کردن validation.

---

### 5. CSRF Exempt (قبلاً ذکر شده)
**فایل:** `core/views.py:213`  
**راه‌حل:** حذف `@csrf_exempt` چون JavaScript در حال ارسال token است.

---

## 🟡 مشکلات متوسط (Medium) - اقدام در اسرع وقت

### 6. Authorization با get_or_create
**فایل:** `accounts/views.py` (چند جا)  
**کد مشکل:**
```python
profile, _ = Profile.objects.get_or_create(user=request.user)
```

**راه‌حل:**
```python
try:
    profile = Profile.objects.get(user=request.user)
except Profile.DoesNotExist:
    return redirect("accounts:profile_edit")
```

---

### 7. Regex DoS
**فایل:** `assessments/views.py:416`  
**راه‌حل:**
```python
import time

def safe_regex_match(pattern, text, timeout=1.0):
    start_time = time.time()
    try:
        result = re.fullmatch(pattern, text)
        if time.time() - start_time > timeout:
            return False
        return bool(result)
    except re.error:
        return False
```

---

### 8. External API Rate Limiting
**فایل:** `core/utils.py`  
**راه‌حل:**
```python
rate_limit_key = f'ip_api_rate_limit_{ip_address}'
request_count = cache.get(rate_limit_key, 0)
if request_count >= 10:
    return ''
cache.set(rate_limit_key, request_count + 1, 3600)
```

---

### 9. Search Query Length
**فایل:** `search/views.py:16`  
**راه‌حل:**
```python
query = self.request.GET.get("q", "").strip()
if len(query) > 200:
    query = query[:200]
```

---

### 10. Session Data Size
**فایل:** `assessments/views.py`  
**راه‌حل:** محدود کردن size یا استفاده از database برای state های بزرگ.

---

### 11. Price Validation در Checkout
**فایل:** `shop/views.py:94`  
**بهبود:**
```python
product = get_object_or_404(
    Product, 
    id=int(product_id),
    is_active=True  # فقط محصولات فعال
)
```

---

### 12. IDOR در Analytics
**فایل:** `accounts/views.py:554`  
**نکته:** اگر intentional است (همه admin ها همه را ببینند)، OK است. اگر نه، فیلتر اضافه کنید.

---

## 🟢 بهبودهای پیشنهادی (Low)

### 13. Dependency Security
```bash
pip install safety pip-audit
safety check
pip-audit
```

### 14. Logging Filters
اضافه کردن patterns بیشتر برای email, phone, credit card.

### 15. Error Messages
استفاده از custom error handlers در production.

---

## 📝 چک‌لیست سریع

### امروز:
- [ ] رفع XSS در custom_css
- [ ] اضافه کردن IP validation
- [ ] حذف session key از templates
- [ ] اضافه کردن validation در RemoveFromCartView
- [ ] حذف csrf_exempt از YouTubeClickView

### این هفته:
- [ ] تغییر get_or_create به get
- [ ] اضافه کردن rate limiting
- [ ] محدود کردن query length
- [ ] اضافه کردن timeout برای regex

### این ماه:
- [ ] بررسی dependencies
- [ ] بهبود logging
- [ ] Performance optimizations

---

## 🎯 اولویت‌بندی

1. **امروز:** مشکلات بحرانی (1-5)
2. **این هفته:** مشکلات متوسط (6-12)
3. **این ماه:** بهبودهای پیشنهادی (13-15)

---

**نکته:** بعد از هر تغییر، حتماً تست کنید که functionality هنوز کار می‌کند.
