# 🌐 Language Selector - Minimal & Professional Design

## 📋 Overview

این سیستم انتخاب زبان جدید با طراحی مینیمال و حرفه‌ای برای سایت Sami Deutsch ایجاد شده است که شامل:

- **طراحی مینیمال**: ظاهر تمیز و مدرن مشابه سایت‌های معتبر
- **پرچم‌های SVG**: کیفیت بالا و اندازه بهینه
- **پشتیبانی از RTL**: سازگار با زبان فارسی
- **ریسپانسیو**: بهینه‌سازی شده برای موبایل و دسکتاپ
- **دسترسی‌پذیری**: پشتیبانی کامل از کیبورد و screen reader

## 🎨 Features

### Visual Design
- **Backdrop Blur**: افکت شیشه‌ای مدرن
- **Smooth Animations**: انیمیشن‌های نرم و طبیعی
- **Flag Icons**: پرچم‌های SVG با کیفیت بالا
- **Hover Effects**: افکت‌های تعاملی زیبا

### Functionality
- **Dropdown Menu**: منوی کشویی حرفه‌ای
- **Language Switching**: تغییر زبان بدون reload صفحه
- **Current Language**: نمایش زبان فعلی
- **Native Names**: نام زبان‌ها به زبان اصلی

### Accessibility
- **Keyboard Navigation**: پشتیبانی کامل از کیبورد
- **ARIA Labels**: برچسب‌های مناسب برای screen reader
- **Focus Management**: مدیریت فوکوس مناسب
- **High Contrast**: پشتیبانی از حالت کنتراست بالا

## 🛠️ Technical Implementation

### Files Structure
```
static/
├── css/
│   ├── language-selector.css          # استایل‌های اصلی
│   └── language-selector-rtl.css     # استایل‌های RTL
├── js/
│   └── language-selector.js          # عملکرد JavaScript
└── img/
    └── flags/                        # پرچم‌های SVG
        ├── fa.svg                    # پرچم ایران
        ├── en.svg                    # پرچم انگلستان
        └── de.svg                    # پرچم آلمان
```

### CSS Classes
- `.language-selector`: کانتینر اصلی
- `.language-selector__button`: دکمه انتخاب زبان
- `.language-selector__dropdown`: منوی کشویی
- `.language-selector__list`: لیست زبان‌ها
- `.language-selector__item`: آیتم زبان
- `.language-selector__link`: لینک انتخاب زبان

### JavaScript API
```javascript
// Initialize language selector
new LanguageSelector('.language-selector');

// Available methods
selector.open();           // باز کردن منو
selector.close();          // بستن منو
selector.toggle();         // تغییر وضعیت
selector.selectLanguage(); // انتخاب زبان
```

## 🚀 Usage

### Basic Implementation
```html
<div class="language-selector">
  <button class="language-selector__button" type="button" aria-expanded="false">
    <div class="flag">
      <img src="/static/img/flags/fa.svg" alt="فارسی">
    </div>
    <span>فارسی</span>
    <svg class="chevron">...</svg>
  </button>
  
  <div class="language-selector__dropdown">
    <ul class="language-selector__list">
      <li class="language-selector__item">
        <a href="#" class="language-selector__link" data-lang="fa">
          <div class="flag">...</div>
          <div class="name">
            <div>فارسی</div>
            <div class="native-name">Persian</div>
          </div>
        </a>
      </li>
    </ul>
  </div>
</div>
```

### Required Dependencies
```html
<!-- CSS Files -->
<link href="/static/css/language-selector.css" rel="stylesheet">
<link href="/static/css/language-selector-rtl.css" rel="stylesheet">

<!-- JavaScript File -->
<script src="/static/js/language-selector.js"></script>
```

## 🎯 Customization

### Colors
```css
:root {
  --language-selector-bg: rgba(255, 255, 255, 0.95);
  --language-selector-border: rgba(0, 0, 0, 0.1);
  --language-selector-shadow: rgba(0, 0, 0, 0.15);
}
```

### Sizes
```css
.language-selector__button {
  padding: 8px 12px;        /* تغییر padding */
  font-size: 14px;          /* تغییر اندازه فونت */
  border-radius: 6px;       /* تغییر گردی گوشه */
}

.language-selector__dropdown {
  min-width: 160px;         /* تغییر عرض منو */
  border-radius: 8px;       /* تغییر گردی گوشه */
}
```

### Animations
```css
.language-selector__button,
.language-selector__dropdown {
  transition: all 0.2s ease; /* تغییر سرعت انیمیشن */
}
```

## 📱 Mobile Optimization

### Touch-Friendly Design
- **Larger Touch Targets**: اندازه مناسب برای لمس
- **Bottom Sheet**: منوی کشویی از پایین در موبایل
- **Swipe Gestures**: پشتیبانی از حرکات لمسی

### Responsive Breakpoints
```css
@media (max-width: 768px) {
  .language-selector__button {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;
  }
  
  .language-selector__dropdown {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    border-radius: 16px 16px 0 0;
  }
}
```

## 🌍 Internationalization

### Language Support
- **Persian (فارسی)**: زبان اصلی سایت
- **English**: زبان بین‌المللی
- **German (Deutsch)**: زبان هدف آموزش

### RTL Support
```css
[dir="rtl"] .language-selector__dropdown {
  right: auto;
  left: 0;
}

[dir="rtl"] .language-selector__link {
  text-align: right;
  flex-direction: row-reverse;
}
```

## ♿ Accessibility Features

### Keyboard Navigation
- **Tab**: حرکت بین عناصر
- **Enter/Space**: باز/بسته کردن منو
- **Escape**: بستن منو
- **Arrow Keys**: حرکت در منو

### Screen Reader Support
```html
<button 
  class="language-selector__button" 
  aria-expanded="false" 
  aria-label="انتخاب زبان"
>
```

### Focus Management
- **Focus Trap**: محدود کردن فوکوس در منو
- **Focus Return**: بازگشت فوکوس به دکمه
- **Visible Focus**: نمایش واضح فوکوس

## 🔧 Browser Support

### Modern Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Legacy Support
- ⚠️ IE 11 (limited)
- ⚠️ Older mobile browsers (graceful degradation)

## 📊 Performance

### Optimization Techniques
- **CSS-in-JS**: استایل‌های بهینه
- **Event Delegation**: مدیریت رویدادهای کارآمد
- **Lazy Loading**: بارگذاری تنبل تصاویر
- **Minimal DOM**: کمترین تغییرات DOM

### Bundle Size
- **CSS**: ~8KB (minified)
- **JavaScript**: ~4KB (minified)
- **Images**: ~2KB total (SVG)

## 🐛 Troubleshooting

### Common Issues

#### Language Not Changing
```javascript
// Check if form submission is working
console.log('Language selected:', langCode);

// Verify CSRF token
console.log('CSRF token:', csrfToken);
```

#### Styling Issues
```css
/* Force override Bootstrap styles */
.language-selector__button {
  background: var(--language-selector-bg) !important;
  border: var(--language-selector-border) !important;
}
```

#### Mobile Issues
```css
/* Ensure proper mobile positioning */
@media (max-width: 768px) {
  .language-selector__dropdown {
    position: fixed !important;
    z-index: 9999 !important;
  }
}
```

## 🔄 Updates & Maintenance

### Version History
- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added RTL support and mobile optimization
- **v1.2.0**: Enhanced accessibility and performance

### Future Enhancements
- [ ] Support for more languages
- [ ] Custom flag uploads
- [ ] Language preferences storage
- [ ] Analytics integration
- [ ] A/B testing support

## 📞 Support

برای سوالات و پشتیبانی:
- 📧 Email: support@samideutsch.com
- 🐛 Issues: GitHub Issues
- 📚 Documentation: این فایل README

---

**نکته**: این سیستم طراحی شده تا با استانداردهای مدرن وب سازگار باشد و تجربه کاربری بهتری ارائه دهد.
