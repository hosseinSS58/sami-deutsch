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
    this.sidebar = document.querySelector('#siteSidebar');
    this.sidebarOverlay = document.querySelector('[data-sidebar-overlay]');
    this.sidebarToggles = document.querySelectorAll('[data-sidebar-toggle]');
    this.sidebarCloseButtons = document.querySelectorAll('[data-sidebar-close]');
    this.lastFocusedBeforeSidebar = null;
    this.handleSidebarKeydown = this.handleSidebarKeydown.bind(this);
    this.isScrolled = false;
    this.isMobileMenuOpen = false;
    this.isSearchOpen = false;
    this.isUserDropdownOpen = false;
    this.isSidebarOpen = false;
    this.userInteracted = false;
    
    this.init();
  }

  init() {
    this.registerFirstInteraction();
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

    // Sidebar toggles
    if (this.sidebarToggles.length) {
      this.sidebarToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
          event.preventDefault();
          this.toggleSidebar();
        });
      });
    }

    if (this.sidebarOverlay) {
      this.sidebarOverlay.addEventListener('click', () => this.closeSidebar());
    }

    if (this.sidebarCloseButtons.length) {
      this.sidebarCloseButtons.forEach(button => {
        button.addEventListener('click', () => this.closeSidebar());
      });
    }

    if (this.sidebar) {
      this.sidebar.addEventListener('keydown', this.handleSidebarKeydown);
      const sidebarLinks = this.sidebar.querySelectorAll('a[href]');
      sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
          if (window.innerWidth <= 1200) {
            this.closeSidebar();
          }
        });
      });
    }

    // User dropdown (desktop)
    if (this.userBtn) {
      this.userBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleUserDropdown();
      });
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
      if (!this.header) {
        return;
      }
      
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

      if (window.innerWidth <= 1024) {
        this.header.style.transform = 'translateY(0)';
        lastScrollTop = scrollTop;
        return;
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
        // keep sidebar state on mobile/tablet unless manually toggled
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
    this.maybeVibrate(50);
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
    this.maybeVibrate(30);
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
      this.maybeVibrate(30);
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

  registerFirstInteraction() {
    const markInteraction = () => {
      this.userInteracted = true;
      window.removeEventListener('pointerdown', markInteraction, true);
      window.removeEventListener('keydown', markInteraction, true);
      window.removeEventListener('touchstart', markInteraction, true);
    };
    window.addEventListener('pointerdown', markInteraction, true);
    window.addEventListener('keydown', markInteraction, true);
    window.addEventListener('touchstart', markInteraction, true);
  }

  maybeVibrate(duration = 30) {
    if (!this.userInteracted) {
      return;
    }
    if (navigator && typeof navigator.vibrate === 'function') {
      try {
        navigator.vibrate(duration);
      } catch (error) {
        // ignore vibration errors
      }
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

  toggleSidebar() {
    if (this.isSidebarOpen) {
      this.closeSidebar();
    } else {
      this.openSidebar();
    }
  }

  openSidebar() {
    if (!this.sidebar) {
      return;
    }
    if (this.isSidebarOpen) {
      return;
    }
    this.lastFocusedBeforeSidebar = document.activeElement;
    document.body.classList.add('sidebar-open');
    this.sidebar.setAttribute('aria-hidden', 'false');
    this.sidebar.setAttribute('tabindex', '-1');
    this.updateSidebarToggleState(true);
    this.focusFirstSidebarElement();
    this.isSidebarOpen = true;
    this.maybeVibrate(30);
  }

  closeSidebar() {
    if (!this.sidebar || !this.isSidebarOpen) {
      return;
    }
    document.body.classList.remove('sidebar-open');
    this.sidebar.classList.remove('user-mode');
    this.sidebar.setAttribute('aria-hidden', 'true');
    this.sidebar.removeAttribute('tabindex');
    this.updateSidebarToggleState(false);
    this.isSidebarOpen = false;
    if (this.lastFocusedBeforeSidebar && typeof this.lastFocusedBeforeSidebar.focus === 'function') {
      this.lastFocusedBeforeSidebar.focus();
    }
    this.lastFocusedBeforeSidebar = null;
  }

  updateSidebarToggleState(expanded) {
    if (this.sidebarToggles.length) {
      this.sidebarToggles.forEach(toggle => toggle.setAttribute('aria-expanded', String(expanded)));
    }
  }

  focusFirstSidebarElement() {
    if (!this.sidebar) {
      return;
    }
    const focusable = this.getSidebarFocusableElements();
    if (focusable.length) {
      focusable[0].focus();
    } else {
      this.sidebar.focus();
    }
  }

  getSidebarFocusableElements() {
    if (!this.sidebar) {
      return [];
    }
    const selectors = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])'
    ];
    return Array.from(this.sidebar.querySelectorAll(selectors.join(','))).filter((el) => {
      return el.offsetParent !== null;
    });
  }

  handleSidebarKeydown(event) {
    if (!this.isSidebarOpen) {
      return;
    }
    if (event.key === 'Tab') {
      const focusable = this.getSidebarFocusableElements();
      if (!focusable.length) {
        event.preventDefault();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
    if (event.key === 'Escape') {
      event.preventDefault();
      this.closeSidebar();
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
    this.closeSidebar();
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
      link.classList.toggle('active', this.linkMatches(link, url));
    });

    const sidebarItems = document.querySelectorAll('.sidebar-item, .sidebar-subitem');
    sidebarItems.forEach(item => item.classList.remove('active'));

    const sidebarLinks = document.querySelectorAll('.sidebar-link, .sidebar-sublink');
    sidebarLinks.forEach(link => {
      if (this.linkMatches(link, url)) {
        const parent = link.closest('.sidebar-subitem, .sidebar-item');
        if (parent) {
          parent.classList.add('active');
        }
        const ancestor = link.closest('.sidebar-subitem')?.closest('.sidebar-item');
        if (ancestor) {
          ancestor.classList.add('active');
        }
      }
    });
  }

  linkMatches(link, url) {
    if (!link) {
      return false;
    }
    const href = link.getAttribute('href');
    if (!href) {
      return false;
    }
    const normalize = (value) => {
      if (!value) {
        return '/';
      }
      if (value.length > 1 && value.endsWith('/')) {
        return value.slice(0, -1);
      }
      return value;
    };
    const normalizedHref = normalize(href);
    const normalizedUrl = normalize(url);
    if (normalizedHref === '/') {
      return normalizedUrl === '/';
    }
    return normalizedUrl.startsWith(normalizedHref);
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
