/**
 * Mobile Enhancements JavaScript
 * بهبودهای اضافی برای موبایل
 */

class MobileEnhancements {
  constructor() {
    this.header = document.querySelector('.modern-header');
    this.mobileNav = document.querySelector('.mobile-nav');
    this.isOnline = navigator.onLine;
    this.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    this.init();
  }

  init() {
    this.setupNetworkStatus();
    this.setupOrientationChange();
    this.setupViewportHeight();
    this.setupTouchOptimizations();
    this.setupPerformanceOptimizations();
    this.setupAccessibilityEnhancements();
  }

  setupNetworkStatus() {
    // Network status monitoring
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.header.classList.remove('offline');
      this.header.classList.add('online');
      setTimeout(() => {
        this.header.classList.remove('online');
      }, 3000);
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.header.classList.remove('online');
      this.header.classList.add('offline');
    });

    // Initial status
    if (!this.isOnline) {
      this.header.classList.add('offline');
    }
  }

  setupOrientationChange() {
    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
      // Delay to ensure proper viewport calculation
      setTimeout(() => {
        this.adjustViewportHeight();
        this.closeMobileMenuOnOrientationChange();
      }, 100);
    });

    // Handle resize events
    window.addEventListener('resize', () => {
      this.debounce(() => {
        this.adjustViewportHeight();
        this.handleResponsiveChanges();
      }, 250)();
    });
  }

  setupViewportHeight() {
    // Fix viewport height issues on mobile
    const setViewportHeight = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };

    setViewportHeight();
    window.addEventListener('resize', setViewportHeight);
    window.addEventListener('orientationchange', setViewportHeight);
  }

  setupTouchOptimizations() {
    // Prevent zoom on double tap
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
      const now = new Date().getTime();
      if (now - lastTouchEnd <= 300) {
        e.preventDefault();
      }
      lastTouchEnd = now;
    }, false);

    // Improve touch scrolling
    if (this.mobileNav) {
      this.mobileNav.addEventListener('touchstart', (e) => {
        this.mobileNav.style.overflowY = 'auto';
      });

      this.mobileNav.addEventListener('touchmove', (e) => {
        // Allow scrolling
      }, { passive: true });
    }

    // Touch feedback for interactive elements
    const touchElements = document.querySelectorAll('.mobile-link, .action-btn, .user-btn, .mobile-toggle');
    touchElements.forEach(element => {
      element.addEventListener('touchstart', () => {
        element.style.transform = 'scale(0.95)';
        element.style.transition = 'transform 0.1s ease';
      });

      element.addEventListener('touchend', () => {
        setTimeout(() => {
          element.style.transform = '';
        }, 100);
      });

      element.addEventListener('touchcancel', () => {
        element.style.transform = '';
      });
    });
  }

  setupPerformanceOptimizations() {
    // Lazy load non-critical resources
    if ('IntersectionObserver' in window) {
      const lazyElements = document.querySelectorAll('[data-lazy]');
      const lazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const element = entry.target;
            const src = element.dataset.lazy;
            if (src) {
              element.src = src;
              element.removeAttribute('data-lazy');
            }
            lazyObserver.unobserve(element);
          }
        });
      });

      lazyElements.forEach(element => {
        lazyObserver.observe(element);
      });
    }

    // Optimize animations for performance
    if (this.isReducedMotion) {
      document.documentElement.style.setProperty('--header-transition', 'none');
      document.documentElement.style.setProperty('--header-transition-fast', 'none');
    }

    // Preload critical resources
    this.preloadCriticalResources();
  }

  setupAccessibilityEnhancements() {
    // Skip links functionality
    const skipLinks = document.querySelectorAll('.skip-link');
    skipLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
          target.focus();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    // Keyboard navigation improvements
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });

    // Focus management for mobile menu
    if (this.mobileNav) {
      this.mobileNav.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          this.closeMobileMenu();
        }
      });
    }
  }

  adjustViewportHeight() {
    // Adjust for mobile browsers with dynamic viewport
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    
    // Adjust mobile nav height
    if (this.mobileNav) {
      this.mobileNav.style.height = `${window.innerHeight}px`;
    }
  }

  closeMobileMenuOnOrientationChange() {
    // Close mobile menu on orientation change to prevent layout issues
    if (window.innerWidth > 1024 && this.mobileNav.classList.contains('active')) {
      const header = window.modernHeader;
      if (header && header.closeMobileMenu) {
        header.closeMobileMenu();
      }
    }
  }

  handleResponsiveChanges() {
    // Handle responsive breakpoint changes
    if (window.innerWidth > 1024) {
      // Desktop view
      this.header.classList.add('desktop-view');
      this.header.classList.remove('mobile-view');
    } else {
      // Mobile view
      this.header.classList.add('mobile-view');
      this.header.classList.remove('desktop-view');
    }
  }

  preloadCriticalResources() {
    // Preload critical CSS and JS
    const criticalResources = [
      '/static/css/header-modern.css',
      '/static/css/header-mobile.css',
      '/static/js/header-modern.js'
    ];

    criticalResources.forEach(resource => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = resource;
      link.as = resource.endsWith('.css') ? 'style' : 'script';
      document.head.appendChild(link);
    });
  }

  // Utility methods
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  closeMobileMenu() {
    const header = window.modernHeader;
    if (header && header.closeMobileMenu) {
      header.closeMobileMenu();
    }
  }

  // Public methods
  showLoading() {
    this.header.classList.add('loading');
  }

  hideLoading() {
    this.header.classList.remove('loading');
  }

  showError() {
    this.header.classList.add('error');
    setTimeout(() => {
      this.header.classList.remove('error');
    }, 5000);
  }

  showSuccess() {
    this.header.classList.add('success');
    setTimeout(() => {
      this.header.classList.remove('success');
    }, 3000);
  }

  // Network status methods
  isNetworkOnline() {
    return this.isOnline;
  }

  setNetworkStatus(online) {
    this.isOnline = online;
    if (online) {
      this.header.classList.remove('offline');
      this.header.classList.add('online');
    } else {
      this.header.classList.remove('online');
      this.header.classList.add('offline');
    }
  }
}

// Initialize mobile enhancements when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const mobileEnhancements = new MobileEnhancements();
  
  // Make globally accessible
  window.mobileEnhancements = mobileEnhancements;
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MobileEnhancements;
}





