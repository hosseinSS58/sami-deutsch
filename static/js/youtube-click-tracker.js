/**
 * YouTube Click Tracker
 * ثبت خودکار کلیک‌های کاربران روی لینک‌های یوتیوب
 */

(function() {
    'use strict';

    // تابع استخراج شناسه ویدیو از URL
    function extractYouTubeId(url) {
        if (!url) return null;
        try {
            const urlObj = new URL(url);
            if (urlObj.hostname === 'youtu.be' || urlObj.hostname === 'www.youtu.be') {
                return urlObj.pathname.slice(1) || null;
            }
            if (urlObj.hostname.includes('youtube.com')) {
                if (urlObj.pathname.startsWith('/watch')) {
                    return urlObj.searchParams.get('v');
                }
                if (urlObj.pathname.startsWith('/embed/')) {
                    return urlObj.pathname.split('/embed/')[1];
                }
                if (urlObj.pathname.startsWith('/shorts/')) {
                    return urlObj.pathname.split('/shorts/')[1];
                }
            }
        } catch (e) {
            console.warn('Error extracting YouTube ID:', e);
        }
        return null;
    }

    // تابع ثبت کلیک
    function trackYouTubeClick(event) {
        const link = event.currentTarget;
        const youtubeUrl = link.href;
        
        // اگر لینک یوتیوب نیست، رد کن
        if (!youtubeUrl || (!youtubeUrl.includes('youtube.com') && !youtubeUrl.includes('youtu.be'))) {
            return;
        }

        // دریافت اطلاعات منبع از data attributes
        const sourceType = link.dataset.sourceType || 'other';
        const sourceId = link.dataset.sourceId || '';
        const sourceTitle = link.dataset.sourceTitle || link.textContent.trim() || '';

        // ارسال درخواست به سرور (بدون انتظار برای پاسخ)
        fetch('/api/youtube-click/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: new URLSearchParams({
                'youtube_url': youtubeUrl,
                'source_type': sourceType,
                'source_id': sourceId,
                'source_title': sourceTitle
            }),
            keepalive: true // برای اینکه درخواست حتی بعد از بسته شدن صفحه هم ارسال شود
        }).catch(function(error) {
            // خطا را نادیده بگیر (برای اینکه لینک باز شود)
            console.warn('Failed to track YouTube click:', error);
        });
    }

    // تابع دریافت CSRF token از cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // اضافه کردن event listener به همه لینک‌های یوتیوب
    function initTracking() {
        // لینک‌های موجود در صفحه
        const youtubeLinks = document.querySelectorAll('a[href*="youtube.com"], a[href*="youtu.be"]');
        
        youtubeLinks.forEach(function(link) {
            // اگر قبلاً listener اضافه شده، اضافه نکن
            if (link.dataset.tracked === 'true') {
                return;
            }
            
            link.dataset.tracked = 'true';
            link.addEventListener('click', trackYouTubeClick, { passive: true });
        });
    }

    // اجرای اولیه
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTracking);
    } else {
        initTracking();
    }

    // برای محتوای داینامیک (مثلاً AJAX)
    const observer = new MutationObserver(function(mutations) {
        initTracking();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

})();


