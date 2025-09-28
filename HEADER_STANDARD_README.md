# 🎯 هدر استاندارد Sami Deutsch

## 📋 خلاصه

هدر استاندارد جدید با طراحی مدرن، دسترسی‌پذیری بالا و عملکرد بهینه برای پروژه Sami Deutsch طراحی شده است. این هدر از اصول طراحی استاندارد وب پیروی می‌کند و کاملاً responsive است.

## ✨ ویژگی‌های کلیدی

### 🎨 **طراحی مدرن**
- طراحی تمیز و مینیمال
- رنگ‌بندی استاندارد و قابل تنظیم
- انیمیشن‌های نرم و طبیعی
- سایه‌ها و افکت‌های بصری جذاب

### 📱 **Responsive Design**
- Mobile-first approach
- سازگار با تمام اندازه‌های صفحه
- منوی موبایل پیشرفته
- Touch-friendly interactions

### ♿ **دسترسی‌پذیری (Accessibility)**
- ARIA labels و roles کامل
- Keyboard navigation
- Screen reader support
- Focus management
- High contrast support

### ⚡ **عملکرد بهینه**
- CSS Variables برای مدیریت آسان
- JavaScript class-based architecture
- Event delegation
- Intersection Observer برای performance
- Resize Observer برای responsive behavior

## 🗂️ ساختار فایل‌ها

```
static/
├── css/
│   ├── header-standard.css      # استایل‌های اصلی هدر
│   └── search-modal.css         # استایل‌های modal جستجو
├── js/
│   └── header-standard.js       # عملکرد JavaScript هدر
└── templates/
    └── header-standard.html     # Template HTML هدر
```

## 🚀 نحوه استفاده

### 1. **اضافه کردن فایل‌های CSS**

```html
<!-- در base.html یا head -->
<link href="{% static 'css/header-standard.css' %}" rel="stylesheet">
<link href="{% static 'css/search-modal.css' %}" rel="stylesheet">
```

### 2. **اضافه کردن فایل JavaScript**

```html
<!-- قبل از closing body tag -->
<script src="{% static 'js/header-standard.js' %}"></script>
```

### 3. **استفاده از Template**

```html
<!-- جایگزینی هدر قدیمی -->
{% include 'header-standard.html' %}
```

## 🎨 شخصی‌سازی رنگ‌ها

### CSS Variables

```css
:root {
  /* Header Colors */
  --header-bg: #ffffff;
  --header-bg-scrolled: rgba(255, 255, 255, 0.95);
  --header-border: #e5e7eb;
  --header-text: #111827;
  --header-text-muted: #6b7280;
  --header-accent: #3b82f6;
  --header-accent-hover: #2563eb;
  
  /* Button Colors */
  --btn-primary-bg: #3b82f6;
  --btn-primary-hover: #2563eb;
  --btn-primary-text: #ffffff;
  --btn-secondary-bg: #f3f4f6;
  --btn-secondary-hover: #e5e7eb;
  --btn-secondary-text: #374151;
}
```

### تغییر رنگ‌ها

```css
/* در فایل CSS سفارشی */
:root {
  --header-accent: #10b981;        /* رنگ سبز */
  --header-accent-hover: #059669;  /* رنگ سبز تیره */
  --header-bg: #1f2937;            /* رنگ تیره */
  --header-text: #f9fafb;          /* متن روشن */
}
```

## 🔧 تنظیمات JavaScript

### تنظیمات پیش‌فرض

```javascript
// تنظیمات پیش‌فرض
const headerConfig = {
  scrollThreshold: 50,           // آستانه اسکرول برای تغییر استایل
  mobileBreakpoint: 768,        // نقطه شکست موبایل
  animationDuration: 300,       // مدت انیمیشن (ms)
  autoHideOnScroll: true,       // مخفی شدن خودکار در اسکرول
  enableSearch: true,           // فعال کردن جستجو
  enableDropdowns: true         // فعال کردن dropdown ها
};
```

### متدهای عمومی

```javascript
// دسترسی به instance هدر
const header = window.standardHeader;

// نمایش loading state
header.showLoading();

// مخفی کردن loading state
header.hideLoading();

// تنظیم لینک فعال
header.setActiveLink('/videos/');

// به‌روزرسانی اطلاعات کاربر
header.updateUserInfo({
  name: 'نام کاربر',
  avatar: '/path/to/avatar.jpg'
});
```

## 📱 Responsive Breakpoints

```css
/* Desktop */
@media (min-width: 1024px) { }

/* Tablet */
@media (max-width: 1023px) { }

/* Mobile */
@media (max-width: 768px) { }

/* Small Mobile */
@media (max-width: 480px) { }
```

## ♿ ویژگی‌های دسترسی‌پذیری

### ARIA Attributes

```html
<nav role="navigation" aria-label="Main navigation">
  <button aria-label="Toggle navigation menu" 
          aria-expanded="false" 
          aria-controls="mobile-navigation">
    <!-- Menu toggle button -->
  </button>
</nav>
```

### Keyboard Navigation

- **Tab**: حرکت بین عناصر
- **Enter/Space**: فعال کردن دکمه‌ها
- **Escape**: بستن منوها و modal ها
- **Arrow Keys**: حرکت در dropdown ها

### Focus Management

- Focus trap در منوی موبایل
- Focus return پس از بستن modal
- Visible focus indicators
- Logical tab order

## 🎭 انیمیشن‌ها و Transitions

### CSS Transitions

```css
/* Fast transitions */
--transition-fast: 0.15s ease-in-out;

/* Normal transitions */
--transition-normal: 0.3s ease-in-out;

/* Smooth animations */
.header-nav-link {
  transition: all var(--transition-fast);
}
```

### Keyframe Animations

```css
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## 🔍 قابلیت جستجو

### Search Modal

```html
<div class="search-modal" id="search-modal" aria-hidden="true">
  <div class="search-modal-content">
    <div class="search-modal-header">
      <h3>جستجو در سایت</h3>
      <button class="search-modal-close">×</button>
    </div>
    <div class="search-modal-body">
      <form class="search-form" role="search">
        <input type="search" class="search-input" placeholder="جستجو...">
        <button type="submit" class="search-submit">جستجو</button>
      </form>
    </div>
  </div>
</div>
```

### Search Functionality

```javascript
// باز کردن modal جستجو
header.openSearch();

// بستن modal جستجو
document.querySelector('.search-modal-close').click();

// جستجو با Enter
document.querySelector('.search-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    // انجام جستجو
  }
});
```

## 🌐 پشتیبانی RTL

### RTL Styles

```css
[dir="rtl"] .header-nav-menu {
  flex-direction: row-reverse;
}

[dir="rtl"] .header-actions {
  flex-direction: row-reverse;
}

[dir="rtl"] .header-dropdown {
  left: auto;
  right: 0;
}
```

### RTL JavaScript

```javascript
// تشخیص جهت زبان
const isRTL = document.documentElement.dir === 'rtl';

// تنظیم موقعیت dropdown ها
if (isRTL) {
  dropdown.style.right = '0';
  dropdown.style.left = 'auto';
}
```

## 🧪 تست و Debug

### Console Logs

```javascript
// فعال کردن debug mode
const header = new StandardHeader();
header.debug = true;

// مشاهده وضعیت هدر
console.log('Header state:', {
  isScrolled: header.isScrolled,
  isMobileMenuOpen: header.isMobileMenuOpen,
  currentBreakpoint: header.getCurrentBreakpoint()
});
```

### Browser DevTools

```css
/* اضافه کردن outline برای debug */
.header * {
  outline: 1px solid red;
}

/* نمایش breakpoint فعلی */
.header::before {
  content: 'Desktop';
}

@media (max-width: 768px) {
  .header::before {
    content: 'Mobile';
  }
}
```

## 📊 Performance Metrics

### Core Web Vitals

- **LCP**: < 2.5s
- **FID**: < 100ms
- **CLS**: < 0.1

### Optimization Techniques

- CSS Variables برای کاهش repetition
- Event delegation برای کاهش event listeners
- Intersection Observer برای scroll events
- Resize Observer برای responsive behavior
- Passive event listeners برای scroll performance

## 🔒 امنیت

### CSRF Protection

```html
<form method="post" action="{% url 'accounts:logout' %}">
  {% csrf_token %}
  <button type="submit">خروج</button>
</form>
```

### XSS Prevention

```javascript
// Sanitize user input
const sanitizeInput = (input) => {
  return input.replace(/[<>]/g, '');
};

// Safe DOM manipulation
const safeSetInnerHTML = (element, content) => {
  element.textContent = content;
};
```

## 🚀 Deployment

### Production Build

```bash
# Minify CSS
npm install -g cssnano
cssnano header-standard.css header-standard.min.css

# Minify JavaScript
npm install -g terser
terser header-standard.js -o header-standard.min.js
```

### CDN Integration

```html
<!-- استفاده از CDN -->
<link href="https://cdn.example.com/header-standard.min.css" rel="stylesheet">
<script src="https://cdn.example.com/header-standard.min.js"></script>
```

## 📝 Changelog

### Version 1.0.0
- ✅ هدر استاندارد پایه
- ✅ Responsive design
- ✅ Accessibility features
- ✅ Search functionality
- ✅ Mobile menu
- ✅ RTL support

### Version 1.1.0 (Planned)
- 🔄 Dark mode support
- 🔄 Advanced animations
- 🔄 Performance optimizations
- 🔄 Additional customization options

## 🤝 مشارکت

### گزارش Bug

```markdown
**Bug Description:**
- What happened?
- Expected behavior?
- Steps to reproduce?
- Browser/Device info?

**Code Example:**
```html
<!-- کد مشکل‌دار -->
```

### پیشنهاد Feature

```markdown
**Feature Request:**
- Description
- Use case
- Implementation ideas
- Priority level
```

## 📞 پشتیبانی

### منابع مفید

- [MDN Web Docs](https://developer.mozilla.org/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/)
- [CSS Grid Layout](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

### تماس

- **Email**: support@samideutsch.com
- **GitHub**: [Issues](https://github.com/samideutsch/header-standard)
- **Documentation**: [Wiki](https://github.com/samideutsch/header-standard/wiki)

---

**نکته**: این هدر بر اساس آخرین استانداردهای وب طراحی شده و با تمام مرورگرهای مدرن سازگار است. برای بهترین تجربه کاربری، از آخرین نسخه مرورگر استفاده کنید.
