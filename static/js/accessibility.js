/**
 * Accessibility Enhancement JavaScript
 * Handles keyboard navigation, focus management, and accessibility features
 */

document.addEventListener('DOMContentLoaded', function() {
  // Skip links functionality
  const skipLinks = document.querySelectorAll('.skip-link');
  skipLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.focus();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  
  // Keyboard navigation enhancement
  document.addEventListener('keydown', function(e) {
    // Tab key detection for keyboard navigation
    if (e.key === 'Tab') {
      document.body.classList.add('keyboard-navigation');
    }
  });
  
  // Remove keyboard navigation class on mouse use
  document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
  });
  
  // Focus management for modals and dropdowns
  const modals = document.querySelectorAll('.modal, .search-modal');
  modals.forEach(modal => {
    const focusableElements = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length > 0) {
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      // Trap focus within modal
      modal.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              e.preventDefault();
              lastElement.focus();
            }
          } else {
            if (document.activeElement === lastElement) {
              e.preventDefault();
              firstElement.focus();
            }
          }
        }
      });
    }
  });
  
  // ARIA live regions for dynamic content
  const liveRegion = document.createElement('div');
  liveRegion.setAttribute('aria-live', 'polite');
  liveRegion.setAttribute('aria-atomic', 'true');
  liveRegion.className = 'sr-only';
  document.body.appendChild(liveRegion);
  
  // Announce page changes
  function announcePageChange(message) {
    liveRegion.textContent = message;
    setTimeout(() => {
      liveRegion.textContent = '';
    }, 1000);
  }
  
  // High contrast mode detection
  if (window.matchMedia('(prefers-contrast: high)').matches) {
    document.body.classList.add('high-contrast');
  }
  
  // Reduced motion detection
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.body.classList.add('reduced-motion');
  }
  
  // Screen reader only content
  const srOnlyStyle = document.createElement('style');
  srOnlyStyle.textContent = `
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    
    .keyboard-navigation *:focus {
      outline: 2px solid var(--site-primary-color, #0d6efd);
      outline-offset: 2px;
    }
    
    .high-contrast {
      filter: contrast(1.5);
    }
    
    .reduced-motion * {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  `;
  document.head.appendChild(srOnlyStyle);
  
  // Focus indicators for better accessibility
  const focusStyle = document.createElement('style');
  focusStyle.textContent = `
    .focus-visible {
      outline: 2px solid var(--site-primary-color, #0d6efd);
      outline-offset: 2px;
    }
    
    .skip-link {
      position: absolute;
      top: -40px;
      left: 6px;
      background: var(--site-primary-color, #0d6efd);
      color: white;
      padding: 8px;
      text-decoration: none;
      z-index: 1000;
      border-radius: 4px;
    }
    
    .skip-link:focus {
      top: 6px;
    }
  `;
  document.head.appendChild(focusStyle);
  
  // Error handling for accessibility features
  window.addEventListener('error', function(e) {
    console.error('Accessibility error:', e.error);
    announcePageChange('خطا در بارگذاری صفحه');
  });
});

// Export functions for use in other scripts
window.accessibility = {
  announcePageChange: function(message) {
    const liveRegion = document.querySelector('[aria-live="polite"]');
    if (liveRegion) {
      liveRegion.textContent = message;
      setTimeout(() => {
        liveRegion.textContent = '';
      }, 1000);
    }
  }
};




