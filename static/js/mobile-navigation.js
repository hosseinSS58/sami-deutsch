/**
 * Enhanced Mobile Navigation JavaScript
 * Handles mobile menu animations, touch interactions, and scroll effects
 */

document.addEventListener('DOMContentLoaded', function() {
  // Enhanced mobile menu animations
  const mobileMenu = document.getElementById('mobileMenu');
  const navbarToggler = document.querySelector('.navbar-toggler');
  
  if (mobileMenu && navbarToggler) {
    // Enhanced toggle button animation
    navbarToggler.addEventListener('click', function() {
      this.classList.add('clicked');
      setTimeout(() => this.classList.remove('clicked'), 300);
    });
    
    // Enhanced mobile menu open animation
    mobileMenu.addEventListener('show.bs.offcanvas', function() {
      // Add entrance animation to menu items
      const menuItems = this.querySelectorAll('.mobile-nav li, .mobile-user-actions .btn');
      menuItems.forEach((item, index) => {
        item.style.animationDelay = `${(index + 1) * 0.1}s`;
        item.classList.add('animate-in');
      });
      
      // Enhanced backdrop
      const backdrop = document.querySelector('.offcanvas-backdrop');
      if (backdrop) {
        backdrop.style.animation = 'fadeIn 0.3s ease';
      }
    });
    
    // Enhanced mobile menu close animation
    mobileMenu.addEventListener('hide.bs.offcanvas', function() {
      // Add exit animation to menu items
      const menuItems = this.querySelectorAll('.mobile-nav li, .mobile-user-actions .btn');
      menuItems.forEach((item, index) => {
        item.style.animationDelay = `${(menuItems.length - index) * 0.05}s`;
        item.classList.add('animate-out');
      });
      
      // Enhanced backdrop fade out
      const backdrop = document.querySelector('.offcanvas-backdrop');
      if (backdrop) {
        backdrop.style.animation = 'fadeOut 0.2s ease';
      }
    });
    
    // Enhanced mobile link interactions
    const mobileLinks = mobileMenu.querySelectorAll('.mobile-nav-link');
    mobileLinks.forEach(link => {
      link.addEventListener('touchstart', function() {
        this.classList.add('touch-active');
      });
      
      link.addEventListener('touchend', function() {
        setTimeout(() => {
          this.classList.remove('touch-active');
        }, 150);
      });
      
      // Enhanced hover effect for devices with hover support
      if (window.matchMedia('(hover: hover)').matches) {
        link.addEventListener('mouseenter', function() {
          this.classList.add('hover-active');
        });
        
        link.addEventListener('mouseleave', function() {
          this.classList.remove('hover-active');
        });
      }
    });
    
    // Enhanced button interactions
    const mobileButtons = mobileMenu.querySelectorAll('.btn');
    mobileButtons.forEach(btn => {
      btn.addEventListener('touchstart', function() {
        this.classList.add('touch-active');
      });
      
      btn.addEventListener('touchend', function() {
        setTimeout(() => {
          this.classList.remove('touch-active');
        }, 150);
      });
    });
  }
  
  // Enhanced navbar scroll effect
  let lastScrollTop = 0;
  const navbar = document.querySelector('.navbar');
  
  // Debounce scroll event for better performance
  const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  };
  
  const handleScroll = debounce(() => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    
    // Hide navbar on scroll down, show on scroll up (mobile only)
    if (window.innerWidth <= 768) {
      if (scrollTop > lastScrollTop && scrollTop > 100) {
        navbar.style.transform = 'translateY(-100%)';
      } else {
        navbar.style.transform = 'translateY(0)';
      }
    }
    
    lastScrollTop = scrollTop;
  }, 10);
  
  window.addEventListener('scroll', handleScroll);
  
  // Enhanced search functionality
  const searchToggle = document.querySelector('.search-toggle');
  const searchModal = document.querySelector('.search-modal');
  
  if (searchToggle && searchModal) {
    searchToggle.addEventListener('click', function() {
      searchModal.classList.add('active');
      const searchInput = searchModal.querySelector('input[type="text"]');
      if (searchInput) {
        setTimeout(() => searchInput.focus(), 300);
      }
    });
    
    // Close search on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && searchModal.classList.contains('active')) {
        searchModal.classList.remove('active');
      }
    });
  }
  
  // Add CSS animations dynamically
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes fadeOut {
      from { opacity: 1; }
      to { opacity: 0; }
    }
    
    .mobile-nav li.animate-in,
    .mobile-user-actions .btn.animate-in {
      animation: fadeInUp 0.6s ease forwards;
    }
    
    .mobile-nav li.animate-out,
    .mobile-user-actions .btn.animate-out {
      animation: fadeOutDown 0.4s ease forwards;
    }
    
    @keyframes fadeOutDown {
      from {
        opacity: 1;
        transform: translateY(0);
      }
      to {
        opacity: 0;
        transform: translateY(20px);
      }
    }
    
    .navbar-toggler.clicked {
      transform: scale(0.95);
      transition: transform 0.1s ease;
    }
    
    .mobile-nav-link.touch-active {
      transform: scale(0.98);
      background: rgba(255, 255, 255, 0.2);
      transition: all 0.1s ease;
    }
    
    .mobile-nav-link.hover-active {
      transform: translateX(8px) scale(1.02);
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .btn.touch-active {
      transform: scale(0.98);
      transition: transform 0.1s ease;
    }
    
    .navbar {
      transition: transform 0.3s ease, background-color 0.3s ease, backdrop-filter 0.3s ease;
    }
    
    .offcanvas-backdrop {
      transition: opacity 0.3s ease, backdrop-filter 0.3s ease;
    }
  `;
  document.head.appendChild(style);
});

// Error handling for mobile navigation
window.addEventListener('error', function(e) {
  console.error('Mobile navigation error:', e.error);
});

// Performance monitoring
if ('performance' in window) {
  window.addEventListener('load', function() {
    const perfData = performance.getEntriesByType('navigation')[0];
    console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
  });
}




