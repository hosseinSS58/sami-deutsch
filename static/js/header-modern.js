/**
 * Modern Header JavaScript
 * مدیریت هدر مدرن با قابلیت‌های پیشرفته
 */

class ModernHeader {
  constructor() {
    this.header = document.querySelector('.modern-header');
    this.mobileToggle = document.querySelector('.mobile-toggle');
    this.mobileNav = document.querySelector('.mobile-nav');
    this.mobileClose = document.querySelector('.mobile-close');
    this.searchBtn = document.querySelector('.search-btn');
    this.searchModal = document.querySelector('.search-modal');
    this.searchClose = document.querySelector('.search-close');
    this.userBtn = document.querySelector('.user-btn');
    this.userDropdown = document.querySelector('.user-dropdown');
    this.dropdowns = document.querySelectorAll('.dropdown');
    
    this.isScrolled = false;
    this.isMobileMenuOpen = false;
    this.isSearchOpen = false;
    this.isUserDropdownOpen = false;
    
    this.init();
  }

  init() {
    this.bindEvents();
    this.setupScrollEffect();
    this.setupResizeObserver();
    this.setupKeyboardNavigation();
    this.setupTouchEvents();
  }

  bindEvents() {
    // Mobile menu toggle
    if (this.mobileToggle) {
      this.mobileToggle.addEventListener('click', () => this.toggleMobileMenu());
    }

    // Mobile menu close
    if (this.mobileClose) {
      this.mobileClose.addEventListener('click', () => this.closeMobileMenu());
    }

    // Search functionality
    if (this.searchBtn) {
      this.searchBtn.addEventListener('click', () => this.openSearch());
    }

    if (this.searchClose) {
      this.searchClose.addEventListener('click', () => this.closeSearch());
    }

  // User dropdown
  if (this.userBtn) {
    this.userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleUserDropdown();
    });
    
    // Touch events for mobile
    if ('ontouchstart' in window) {
      this.userBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        this.toggleUserDropdown();
      });
    }
  }

    // Close dropdowns on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.dropdown')) {
        this.closeAllDropdowns();
      }
      if (!e.target.closest('.user-profile')) {
        this.closeUserDropdown();
      }
    });

    // Close mobile menu on link click
    const mobileLinks = document.querySelectorAll('.mobile-link');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => this.closeMobileMenu());
    });

    // Search form submission
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
      searchForm.addEventListener('submit', (e) => this.handleSearch(e));
    }

    // Close modals on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeAllModals();
      }
    });
  }

  setupScrollEffect() {
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      // Add scrolled class
      if (scrollTop > 50) {
        if (!this.isScrolled) {
          this.isScrolled = true;
          this.header.classList.add('scrolled');
        }
      } else {
        if (this.isScrolled) {
          this.isScrolled = false;
          this.header.classList.remove('scrolled');
        }
      }

      // Hide header on scroll down, show on scroll up
      if (scrollTop > lastScrollTop && scrollTop > 100) {
        this.header.style.transform = 'translateY(-100%)';
      } else {
        this.header.style.transform = 'translateY(0)';
      }

      lastScrollTop = scrollTop;
    });
  }

  setupResizeObserver() {
    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver(() => {
        if (window.innerWidth > 1024) {
          this.closeMobileMenu();
        }
      });
      
      resizeObserver.observe(document.body);
    }
  }

  setupKeyboardNavigation() {
    // Tab navigation for dropdowns
    this.dropdowns.forEach(dropdown => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      const menu = dropdown.querySelector('.dropdown-menu');
      
      if (toggle && menu) {
        toggle.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.toggleDropdown(dropdown);
          }
        });
      }
    });
  }

  setupTouchEvents() {
    // Touch gestures for mobile
    if ('ontouchstart' in window) {
      let startY = 0;
      let startX = 0;
      
      // Mobile nav touch events
      this.mobileNav.addEventListener('touchstart', (e) => {
        startY = e.touches[0].clientY;
        startX = e.touches[0].clientX;
      });
      
      this.mobileNav.addEventListener('touchend', (e) => {
        const endY = e.changedTouches[0].clientY;
        const endX = e.changedTouches[0].clientX;
        const diffY = startY - endY;
        const diffX = startX - endX;
        
        // Swipe up to close
        if (diffY < -50 && Math.abs(diffX) < 50) {
          this.closeMobileMenu();
        }
        
        // Swipe right to close (RTL)
        if (diffX < -50 && Math.abs(diffY) < 50) {
          this.closeMobileMenu();
        }
      });
      
      // Touch feedback for buttons
      const touchElements = document.querySelectorAll('.mobile-toggle, .action-btn, .user-btn, .mobile-link');
      touchElements.forEach(element => {
        element.addEventListener('touchstart', () => {
          element.style.transform = 'scale(0.95)';
        });
        
        element.addEventListener('touchend', () => {
          setTimeout(() => {
            element.style.transform = '';
          }, 150);
        });
      });
    }
  }

  // Mobile menu methods
  toggleMobileMenu() {
    if (this.isMobileMenuOpen) {
      this.closeMobileMenu();
    } else {
      this.openMobileMenu();
    }
  }

  openMobileMenu() {
    this.mobileNav.classList.add('active');
    this.isMobileMenuOpen = true;
    document.body.style.overflow = 'hidden';
    this.mobileToggle.setAttribute('aria-expanded', 'true');
    
    // Animate hamburger
    const spans = this.mobileToggle.querySelectorAll('.hamburger span');
    spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
    spans[1].style.opacity = '0';
    spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    
    // Add mobile menu animation
    const menuItems = this.mobileNav.querySelectorAll('.mobile-link');
    menuItems.forEach((item, index) => {
      item.style.opacity = '0';
      item.style.transform = 'translateX(20px)';
      setTimeout(() => {
        item.style.transition = 'all 0.3s ease';
        item.style.opacity = '1';
        item.style.transform = 'translateX(0)';
      }, index * 100);
    });
    
    // Haptic feedback
    if (navigator.vibrate) {
      navigator.vibrate(50);
    }
  }

  closeMobileMenu() {
    this.mobileNav.classList.remove('active');
    this.isMobileMenuOpen = false;
    document.body.style.overflow = '';
    this.mobileToggle.setAttribute('aria-expanded', 'false');
    
    // Reset hamburger
    const spans = this.mobileToggle.querySelectorAll('.hamburger span');
    spans.forEach(span => {
      span.style.transform = '';
      span.style.opacity = '';
    });
    
    // Reset menu items animation
    const menuItems = this.mobileNav.querySelectorAll('.mobile-link');
    menuItems.forEach(item => {
      item.style.transition = '';
      item.style.opacity = '';
      item.style.transform = '';
    });
    
    // Haptic feedback
    if (navigator.vibrate) {
      navigator.vibrate(30);
    }
  }

  // Search methods
  openSearch() {
    this.searchModal.classList.add('active');
    this.isSearchOpen = true;
    document.body.style.overflow = 'hidden';
    
    // Focus search input
    const searchInput = this.searchModal.querySelector('.search-input');
    if (searchInput) {
      setTimeout(() => searchInput.focus(), 300);
    }
  }

  closeSearch() {
    this.searchModal.classList.remove('active');
    this.isSearchOpen = false;
    document.body.style.overflow = '';
  }

  handleSearch(e) {
    const query = e.target.querySelector('.search-input').value.trim();
    if (query) {
      // Store search in localStorage
      this.storeRecentSearch(query);
      
      // Close modal
      this.closeSearch();
      
      // Redirect to search page
      window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }
  }

  storeRecentSearch(query) {
    let recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    recentSearches = recentSearches.filter(item => item !== query);
    recentSearches.unshift(query);
    recentSearches = recentSearches.slice(0, 5);
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
  }

  // User dropdown methods
  toggleUserDropdown() {
    if (this.isUserDropdownOpen) {
      this.closeUserDropdown();
    } else {
      this.openUserDropdown();
    }
  }

  openUserDropdown() {
    if (this.userDropdown) {
      this.userDropdown.style.opacity = '1';
      this.userDropdown.style.visibility = 'visible';
      this.userDropdown.style.transform = 'translateY(0)';
      this.userDropdown.classList.add('active');
      this.isUserDropdownOpen = true;
      
      // Haptic feedback for mobile
      if (navigator.vibrate) {
        navigator.vibrate(30);
      }
    }
  }

  closeUserDropdown() {
    if (this.userDropdown) {
      this.userDropdown.style.opacity = '0';
      this.userDropdown.style.visibility = 'hidden';
      this.userDropdown.style.transform = 'translateY(-10px)';
      this.userDropdown.classList.remove('active');
      this.isUserDropdownOpen = false;
    }
  }

  // Dropdown methods
  toggleDropdown(dropdown) {
    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) {
      const isOpen = menu.style.opacity === '1';
      if (isOpen) {
        this.closeDropdown(dropdown);
      } else {
        this.openDropdown(dropdown);
      }
    }
  }

  openDropdown(dropdown) {
    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) {
      menu.style.opacity = '1';
      menu.style.visibility = 'visible';
      menu.style.transform = 'translateY(0)';
    }
  }

  closeDropdown(dropdown) {
    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) {
      menu.style.opacity = '0';
      menu.style.visibility = 'hidden';
      menu.style.transform = 'translateY(-10px)';
    }
  }

  closeAllDropdowns() {
    this.dropdowns.forEach(dropdown => {
      this.closeDropdown(dropdown);
    });
  }

  closeAllModals() {
    this.closeMobileMenu();
    this.closeSearch();
    this.closeUserDropdown();
    this.closeAllDropdowns();
  }

  // Public methods
  showLoading() {
    this.header.classList.add('loading');
  }

  hideLoading() {
    this.header.classList.remove('loading');
  }

  updateUserInfo(userData) {
    const userName = document.querySelector('.user-name');
    const userAvatar = document.querySelector('.user-avatar');
    
    if (userName && userData.name) {
      userName.textContent = userData.name;
    }
    
    if (userAvatar && userData.avatar) {
      userAvatar.innerHTML = `<img src="${userData.avatar}" alt="${userData.name}">`;
    }
  }

  setActiveNavItem(url) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === url) {
        link.classList.add('active');
      }
    });
  }
}

// Initialize header when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const header = new ModernHeader();
  
  // Make header globally accessible
  window.modernHeader = header;
  
  // Set active nav item based on current URL
  const currentPath = window.location.pathname;
  header.setActiveNavItem(currentPath);
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ModernHeader;
}
