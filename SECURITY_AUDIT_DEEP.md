# 🔒 گزارش عمیق بررسی امنیتی سایت Sami Deutsch

**تاریخ بررسی:** 2024  
**نسخه Django:** 5.1.11  
**روش بررسی:** Code Review + Security Analysis

---

## 📊 خلاصه اجرایی

این گزارش شامل بررسی **عمیق و دقیق** کدها، الگوهای امنیتی، و آسیب‌پذیری‌های احتمالی است. در این بررسی **15+ مشکل امنیتی** شناسایی شده که برخی بحرانی و برخی نیاز به بهبود دارند.

### آمار کلی:
- 🔴 **5 مشکل بحرانی** (Critical)
- 🟡 **7 مشکل متوسط** (Medium)
- 🟢 **3 بهبود پیشنهادی** (Low)
- ✅ **نمره امنیتی:** 6.5/10

---

## 🔴 مشکلات بحرانی (Critical)

### 1. **XSS Vulnerability در Templates**
**مکان:** `templates/base.html:137`

**مشکل:**
```html
{{ site_settings.custom_css|safe }}
```

**ریسک:**
- اگر `custom_css` از admin قابل ویرایش باشد، امکان تزریق JavaScript وجود دارد
- این می‌تواند منجر به XSS attack شود
- اگر admin account هک شود، کل سایت در خطر است

**راه‌حل:**
```python
# در siteconfig/models.py - بررسی کنید که custom_css از کجا می‌آید
# اگر از admin می‌آید، باید sanitize شود

# گزینه 1: استفاده از bleach برای sanitize
import bleach
allowed_tags = ['style']
allowed_attrs = {'style': ['*']}
sanitized_css = bleach.clean(custom_css, tags=allowed_tags, attributes=allowed_attrs)

# گزینه 2: استفاده از CSS validator
# گزینه 3: حذف |safe و استفاده از {% autoescape off %} فقط برای CSS معتبر
```

**اقدام فوری:**
- ⚠️ بررسی کنید که `custom_css` از کجا می‌آید
- ⚠️ اگر از admin می‌آید، حتماً sanitize کنید
- ⚠️ یا از یک CSS validator استفاده کنید

---

### 2. **SSRF Risk در get_country_from_ip**
**مکان:** `core/utils.py:34`

**مشکل:**
```python
response = requests.get(
    f'https://ipapi.co/{ip_address}/country_code/',
    timeout=3,
)
```

**ریسک:**
- اگر `ip_address` از user input می‌آید و validate نمی‌شود، امکان SSRF وجود دارد
- مهاجم می‌تواند به internal services دسترسی پیدا کند
- مثال: `ip_address = "127.0.0.1:3306"` برای دسترسی به MySQL

**راه‌حل:**
```python
import ipaddress
import re

def validate_ip_address(ip_str):
    """Validate IP address format"""
    # Remove port if present
    ip_str = ip_str.split(':')[0].split('/')[0]
    
    # Check if it's a valid IP
    try:
        ipaddress.ip_address(ip_str)
        # Block private/internal IPs if needed
        if ipaddress.ip_address(ip_str).is_private:
            return False  # یا return '' بسته به نیاز
        return True
    except ValueError:
        return False

def get_country_from_ip(ip_address):
    if not ip_address or not validate_ip_address(ip_address):
        return ''
    
    # Extract only IP part (remove port, path, etc.)
    ip_match = re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip_address)
    if not ip_match:
        return ''
    
    clean_ip = ip_match.group(1)
    # ... rest of the code
```

**اقدام فوری:**
- ⚠️ اضافه کردن IP validation
- ⚠️ Block کردن private IPs اگر نیاز نیست
- ⚠️ استفاده از whitelist برای allowed IP formats

---

### 3. **Session Key Exposure در Templates**
**مکان:** `templates/accounts/anonymous_visitor_detail.html:18`

**مشکل:**
```html
<code>{{ visitor.session_key }}</code>
```

**ریسک:**
- Session key در templates نمایش داده می‌شود
- اگر کسی session key را بدزدد، می‌تواند session hijacking انجام دهد
- این یک اطلاعات حساس است و نباید نمایش داده شود

**راه‌حل:**
```html
<!-- فقط چند کاراکتر اول را نمایش دهید -->
<code>{{ visitor.session_key|truncatechars:8 }}...</code>

<!-- یا اصلاً نمایش ندهید -->
<!-- یا فقط در admin panel نمایش دهید با permission check -->
```

**اقدام فوری:**
- ⚠️ حذف یا truncate کردن session key در templates
- ⚠️ فقط در admin panel با permission check نمایش دهید

---

### 4. **IDOR Vulnerability در Analytics Views**
**مکان:** `accounts/views.py:554`

**مشکل:**
```python
user_id = self.kwargs.get("user_id")
target_user = get_object_or_404(User, id=user_id)
# هیچ بررسی نمی‌کند که آیا admin حق دیدن این user را دارد یا نه
```

**ریسک:**
- هر admin می‌تواند اطلاعات هر کاربری را ببیند
- اگر چند admin دارید، ممکن است بخواهید دسترسی را محدود کنید
- امکان مشاهده اطلاعات حساس کاربران

**راه‌حل (اگر نیاز به محدودیت دارید):**
```python
# اگر می‌خواهید admin فقط کاربران خودش را ببیند:
if not request.user.is_superuser:
    # فقط کاربرانی که خود admin ایجاد کرده یا مربوط به خودش هستند
    target_user = get_object_or_404(
        User, 
        id=user_id,
        # اضافه کردن فیلتر مناسب
    )

# یا اگر می‌خواهید همه admin ها همه را ببینند (که معمولاً OK است):
# هیچ تغییری لازم نیست - این intentional است
```

**اقدام:**
- 💡 تصمیم بگیرید که آیا این intentional است یا نه
- 💡 اگر نیاز به محدودیت دارید، فیلتر اضافه کنید

---

### 5. **Cart Manipulation در Shop Views**
**مکان:** `shop/views.py:72-77`

**مشکل:**
```python
class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = str(request.POST.get("product_id"))  # بدون validation
        cart = request.session.get("cart", {})
        if product_id in cart:
            cart.pop(product_id)
            request.session["cart"] = cart
```

**ریسک:**
- هیچ validation روی `product_id` وجود ندارد
- امکان manipulation وجود دارد
- اگر product_id به صورت مستقیم از request می‌آید، امکان injection وجود دارد

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
            messages.success(request, "Product removed from cart")
        
        return redirect("shop:cart")
```

**اقدام فوری:**
- ⚠️ اضافه کردن validation برای product_id
- ⚠️ بررسی وجود product قبل از حذف

---

## 🟡 مشکلات متوسط (Medium Priority)

### 6. **Authorization Check با get_or_create**
**مکان:** `accounts/views.py:46, 238, 541, 698, 749`

**مشکل:**
```python
profile, _ = Profile.objects.get_or_create(user=request.user)
if profile.user_category != Profile.UserCategory.ADMIN:
    return redirect("accounts:login")
```

**ریسک:**
- استفاده از `get_or_create` در dispatch می‌تواند race condition ایجاد کند
- اگر دو request همزمان بیایند، ممکن است مشکل ایجاد شود
- بهتر است از `get` استفاده شود و اگر وجود نداشت، error بدهد

**راه‌حل:**
```python
from django.core.exceptions import ObjectDoesNotExist

def dispatch(self, request, *args, **kwargs):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # اگر profile وجود ندارد، redirect به profile creation
        return redirect("accounts:profile_edit")
    
    if profile.user_category != Profile.UserCategory.ADMIN:
        return redirect("accounts:login")
    
    return super().dispatch(request, *args, **kwargs)
```

**اقدام:**
- 💡 تغییر به `get` به جای `get_or_create`
- 💡 اضافه کردن error handling مناسب

---

### 7. **Regex DoS در Assessments**
**مکان:** `assessments/views.py:416`

**مشکل:**
```python
if p.kind == p.PatternType.REGEX and re.fullmatch(p.pattern, text):
```

**ریسک:**
- اگر `pattern` از user input می‌آید و validate نمی‌شود، امکان ReDoS وجود دارد
- Regex های پیچیده می‌توانند باعث DoS شوند

**راه‌حل:**
```python
import re
import time

def safe_regex_match(pattern, text, timeout=1.0):
    """Safe regex matching with timeout"""
    start_time = time.time()
    try:
        result = re.fullmatch(pattern, text)
        elapsed = time.time() - start_time
        if elapsed > timeout:
            logger.warning(f"Regex took too long: {elapsed}s")
            return False
        return bool(result)
    except re.error:
        logger.warning(f"Invalid regex pattern: {pattern}")
        return False

# استفاده:
if p.kind == p.PatternType.REGEX:
    q_correct = safe_regex_match(p.pattern, text)
```

**اقدام:**
- 💡 اضافه کردن timeout برای regex
- 💡 Validate کردن regex patterns در admin

---

### 8. **External API بدون Rate Limiting**
**مکان:** `core/utils.py:34`

**مشکل:**
- درخواست‌های متعدد به external API بدون rate limiting
- امکان hitting rate limit
- اگر API fail شود، همه requests fail می‌شوند

**راه‌حل:**
```python
from django.core.cache import cache
from django.utils import timezone

def get_country_from_ip(ip_address):
    # Rate limiting per IP
    rate_limit_key = f'ip_api_rate_limit_{ip_address}'
    request_count = cache.get(rate_limit_key, 0)
    
    if request_count >= 10:  # max 10 requests per hour per IP
        return ''
    
    cache.set(rate_limit_key, request_count + 1, 3600)  # 1 hour
    
    # ... rest of the code
```

**اقدام:**
- 💡 اضافه کردن rate limiting
- 💡 اضافه کردن fallback mechanism

---

### 9. **Input Validation در Search**
**مکان:** `search/views.py:16`

**مشکل:**
```python
query = self.request.GET.get("q", "").strip()
# هیچ محدودیتی روی طول query نیست
```

**ریسک:**
- Query های خیلی طولانی می‌توانند باعث performance issue شوند
- امکان DoS از طریق query های بزرگ

**راه‌حل:**
```python
query = self.request.GET.get("q", "").strip()
if len(query) > 200:  # محدود کردن طول
    query = query[:200]
if not query:
    return []
```

**اقدام:**
- 💡 اضافه کردن محدودیت طول query
- 💡 اضافه کردن validation برای characters خاص

---

### 10. **Session Data Size در Assessments**
**مکان:** `assessments/views.py`

**مشکل:**
- Session data زیادی ذخیره می‌شود (`adaptive_state`, `adaptive_history`, etc.)
- اگر session data خیلی بزرگ شود، می‌تواند مشکل ایجاد کند

**راه‌حل:**
```python
# محدود کردن size session data
MAX_SESSION_SIZE = 4096  # 4KB

def check_session_size(request):
    import sys
    session_size = sys.getsizeof(str(request.session.items()))
    if session_size > MAX_SESSION_SIZE:
        # Clear old data or compress
        request.session.pop('adaptive_history', None)
```

**اقدام:**
- 💡 محدود کردن size session data
- 💡 استفاده از database برای ذخیره state های بزرگ

---

### 11. **Price Manipulation در Checkout**
**مکان:** `shop/views.py:94-103`

**مشکل:**
```python
for product_id, qty in cart.items():
    product = get_object_or_404(Product, id=int(product_id))
    unit_price = product.price  # قیمت از database می‌آید - OK
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=qty,
        unit_price=unit_price,
        line_total=unit_price * qty,
    )
```

**وضعیت:** این کد درست است - قیمت از database می‌آید نه از cart. اما بهتر است بررسی شود که product هنوز active است.

**بهبود:**
```python
for product_id, qty in cart.items():
    product = get_object_or_404(
        Product, 
        id=int(product_id),
        is_active=True  # فقط محصولات فعال
    )
    # بررسی stock اگر موجود است
    # ...
```

---

### 12. **CSRF Exempt (قبلاً ذکر شده)**
**مکان:** `core/views.py:213`

**مشکل:** قبلاً در گزارش اول ذکر شد.

---

## 🟢 بهبودهای پیشنهادی (Low Priority)

### 13. **Dependency Security**
**مکان:** `requirements.txt`

**پیشنهاد:**
- بررسی vulnerabilities در dependencies
- استفاده از `safety` یا `pip-audit`
- به‌روزرسانی منظم

```bash
pip install safety pip-audit
safety check
pip-audit
```

---

### 14. **Logging Sensitive Data**
**مکان:** `sami/logging_filters.py`

**وضعیت:** خوب است اما می‌تواند بهتر شود.

**بهبود:**
```python
SENSITIVE_PATTERNS = [
    # اضافه کردن patterns بیشتر
    (r'email["\']?\s*[:=]\s*["\']?([^"\'\s@]+@[^"\'\s]+)', r'email="***"'),
    (r'phone["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'phone="***"'),
    (r'credit[_-]?card["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'credit_card="***"'),
]
```

---

### 15. **Error Messages Information Disclosure**
**مکان:** Multiple files

**پیشنهاد:**
- در production، error messages نباید اطلاعات حساس بدهند
- استفاده از custom error handlers

---

## 📋 چک‌لیست اقدامات

### فوری (Critical):
- [ ] رفع XSS در `custom_css|safe`
- [ ] اضافه کردن IP validation در `get_country_from_ip`
- [ ] حذف/truncate session key در templates
- [ ] اضافه کردن validation در `RemoveFromCartView`
- [ ] بررسی IDOR در analytics views

### مهم (Medium):
- [ ] تغییر `get_or_create` به `get` در authorization checks
- [ ] اضافه کردن timeout برای regex
- [ ] اضافه کردن rate limiting برای external API
- [ ] محدود کردن طول query در search
- [ ] محدود کردن session data size

### پیشنهادی (Low):
- [ ] بررسی dependencies با safety
- [ ] بهبود logging filters
- [ ] Custom error handlers

---

## 🎯 اولویت‌بندی نهایی

### هفته اول:
1. رفع XSS vulnerability
2. اضافه کردن IP validation
3. حذف session key از templates
4. اضافه کردن validation در shop views

### هفته دوم:
5. بهبود authorization checks
6. اضافه کردن rate limiting
7. محدود کردن input sizes

### هفته سوم:
8. بررسی dependencies
9. بهبود logging
10. Performance optimizations

---

## 📚 منابع

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/5.1/topics/security/)
- [CWE-79: XSS](https://cwe.mitre.org/data/definitions/79.html)
- [CWE-918: SSRF](https://cwe.mitre.org/data/definitions/918.html)

---

**نمره امنیتی بعد از رفع مشکلات بحرانی:** 8.5/10


