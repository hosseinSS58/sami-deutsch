/**
 * Standardized Header JavaScript
 * Modern, accessible, and performant header functionality
 */

class StandardHeader {
  constructor() {
    this.header = document.querySelector('.header');
    this.mobileToggle = document.querySelector('.header-mobile-toggle');
    this.mobileNav = document.querySelector('.header-mobile-nav');
    this.searchBtn = document.querySelector('.header-search-btn');
    this.dropdowns = document.querySelectorAll('[data-dropdown]');
    this.userProfile = document.querySelector('.header-user-profile');
    
    this.isScrolled = false;
    this.isMobileMenuOpen = false;
    this.lastScrollTop = 0;
    
    this.init();
  }

  init() {
    this.bindEvents();
    this.setupIntersectionObserver();
    this.setupResizeObserver();
    this.initializeAccessibility();
  }

  bindEvents() {
    // Scroll events
    window.addEventListener('scroll', this.handleScroll.bind(this), { passive: true });
    
    // Mobile menu toggle
    if (this.mobileToggle) {
      this.mobileToggle.addEventListener('click', this.toggleMobileMenu.bind(this));
    }
    
    // Search functionality
    if (this.searchBtn) {
      this.searchBtn.addEventListener('click', this.openSearch.bind(this));
    }
    
    // Dropdown management
    this.setupDropdowns();
    
    // Click outside to close dropdowns
    document.addEventListener('click', this.handleClickOutside.bind(this));
    
    // Keyboard navigation
    document.addEventListener('keydown', this.handleKeyboard.bind(this));
    
    // Touch events for mobile
    this.setupTouchEvents();
  }

  handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollDelta = scrollTop - this.lastScrollTop;
    
    // Add scrolled class for styling
    if (scrollTop > 50 && !this.isScrolled) {
      this.header.classList.add('scrolled');
      this.isScrolled = true;
    } else if (scrollTop <= 50 && this.isScrolled) {
      this.header.classList.remove('scrolled');
      this.isScrolled = false;
    }
    
    // Auto-hide header on mobile (scroll down)
    if (window.innerWidth <= 768 && scrollTop > 100) {
      if (scrollDelta > 10) {
        this.header.style.transform = 'translateY(-100%)';
      } else if (scrollDelta < -10) {
        this.header.style.transform = 'translateY(0)';
      }
    }
    
    this.lastScrollTop = scrollTop;
  }

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
    
    if (this.isMobileMenuOpen) {
      this.openMobileMenu();
    } else {
      this.closeMobileMenu();
    }
  }

  openMobileMenu() {
    this.mobileToggle.classList.add('active');
    this.mobileNav.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Animate menu items
    const menuItems = this.mobileNav.querySelectorAll('.header-mobile-item');
    menuItems.forEach((item, index) => {
      item.style.animationDelay = `${index * 0.1}s`;
      item.classList.add('animate-in');
    });
    
    // Focus management
    this.trapFocus(this.mobileNav);
  }

  closeMobileMenu() {
    this.mobileToggle.classList.remove('active');
    this.mobileNav.classList.remove('active');
    document.body.style.overflow = '';
    
    // Remove animation classes
    const menuItems = this.mobileNav.querySelectorAll('.header-mobile-item');
    menuItems.forEach(item => {
      item.classList.remove('animate-in');
      item.style.animationDelay = '';
    });
    
    // Return focus to toggle button
    this.mobileToggle.focus();
  }

  setupDropdowns() {
    this.dropdowns.forEach(dropdown => {
      const dropdownMenu = dropdown.querySelector('.header-dropdown');
      if (!dropdownMenu) return;
      
      // Mouse events
      dropdown.addEventListener('mouseenter', () => {
        this.showDropdown(dropdownMenu);
      });
      
      dropdown.addEventListener('mouseleave', () => {
        this.hideDropdown(dropdownMenu);
      });
      
      // Keyboard events
      dropdown.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.toggleDropdown(dropdownMenu);
        }
      });
    });
  }

  showDropdown(dropdownMenu) {
    dropdownMenu.style.opacity = '1';
    dropdownMenu.style.visibility = 'visible';
    dropdownMenu.style.transform = 'translateY(0)';
  }

  hideDropdown(dropdownMenu) {
    dropdownMenu.style.opacity = '0';
    dropdownMenu.style.visibility = 'hidden';
    dropdownMenu.style.transform = 'translateY(-8px)';
  }

  toggleDropdown(dropdownMenu) {
    const isVisible = dropdownMenu.style.visibility === 'visible';
    if (isVisible) {
      this.hideDropdown(dropdownMenu);
    } else {
      this.showDropdown(dropdownMenu);
    }
  }

  handleClickOutside(event) {
    // Close dropdowns when clicking outside
    if (!event.target.closest('.header-nav-item')) {
      this.dropdowns.forEach(dropdown => {
        const dropdownMenu = dropdown.querySelector('.header-dropdown');
        if (dropdownMenu) {
          this.hideDropdown(dropdownMenu);
        }
      });
    }
    
    // Close mobile menu when clicking outside
    if (this.isMobileMenuOpen && !event.target.closest('.header')) {
      this.closeMobileMenu();
    }
  }

  handleKeyboard(event) {
    // Escape key closes mobile menu and dropdowns
    if (event.key === 'Escape') {
      if (this.isMobileMenuOpen) {
        this.closeMobileMenu();
      }
      
      this.dropdowns.forEach(dropdown => {
        const dropdownMenu = dropdown.querySelector('.header-dropdown');
        if (dropdownMenu) {
          this.hideDropdown(dropdownMenu);
        }
      });
    }
    
    // Tab key management for mobile menu
    if (event.key === 'Tab' && this.isMobileMenuOpen) {
      this.handleTabNavigation(event);
    }
  }

  handleTabNavigation(event) {
    const focusableElements = this.mobileNav.querySelectorAll(
      'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (event.shiftKey && document.activeElement === firstElement) {
      event.preventDefault();
      lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  }

  trapFocus(container) {
    const focusableElements = container.querySelectorAll(
      'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    // Focus first element
    firstElement.focus();
    
    // Handle tab navigation within container
    container.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    });
  }

  setupTouchEvents() {
    // Touch-friendly dropdowns for mobile
    if ('ontouchstart' in window) {
      this.dropdowns.forEach(dropdown => {
        const dropdownMenu = dropdown.querySelector('.header-dropdown');
        if (!dropdownMenu) return;
        
        dropdown.addEventListener('touchstart', (e) => {
          e.preventDefault();
          this.toggleDropdown(dropdownMenu);
        });
      });
    }
    
    // Swipe gestures for mobile menu
    this.setupSwipeGestures();
    
    // Haptic feedback for touch interactions
    this.setupHapticFeedback();
  }
  
  setupSwipeGestures() {
    let startX, startY;
    
    this.mobileNav.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    });
    
    this.mobileNav.addEventListener('touchend', (e) => {
      if (!startX || !startY) return;
      
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const diffX = startX - endX;
      const diffY = startY - endY;
      
      // Swipe right to close (RTL)
      if (Math.abs(diffX) > Math.abs(diffY) && diffX < -50) {
        this.closeMobileMenu();
        this.provideHapticFeedback();
      }
      
      startX = startY = null;
    });
  }
  
  setupHapticFeedback() {
    // Add haptic feedback to touch interactions
    const touchElements = document.querySelectorAll('.header-mobile-link, .header-nav-link, .header-search-btn, .header-notification-btn');
    
    touchElements.forEach(element => {
      element.addEventListener('touchstart', () => {
        this.provideHapticFeedback();
      });
    });
  }
  
  provideHapticFeedback() {
    if ('vibrate' in navigator) {
      navigator.vibrate(50);
    }
  }

  setupIntersectionObserver() {
    // Observe header visibility for performance
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.header.classList.remove('header-hidden');
          } else {
            this.header.classList.add('header-hidden');
          }
        });
      },
      { threshold: 0.1 }
    );
    
    observer.observe(this.header);
  }

  setupResizeObserver() {
    // Handle responsive behavior
    const resizeObserver = new ResizeObserver((entries) => {
      entries.forEach(entry => {
        if (entry.contentRect.width > 768 && this.isMobileMenuOpen) {
          this.closeMobileMenu();
        }
      });
    });
    
    resizeObserver.observe(document.body);
  }

  initializeAccessibility() {
    // Add ARIA labels and roles
    if (this.mobileToggle) {
      this.mobileToggle.setAttribute('aria-label', 'Toggle navigation menu');
      this.mobileToggle.setAttribute('aria-expanded', 'false');
      this.mobileToggle.setAttribute('aria-controls', 'mobile-navigation');
    }
    
    if (this.mobileNav) {
      this.mobileNav.setAttribute('id', 'mobile-navigation');
      this.mobileNav.setAttribute('role', 'navigation');
      this.mobileNav.setAttribute('aria-label', 'Mobile navigation');
    }
    
    // Update ARIA states
    this.updateAriaStates();
  }

  updateAriaStates() {
    if (this.mobileToggle) {
      this.mobileToggle.setAttribute('aria-expanded', this.isMobileMenuOpen.toString());
    }
  }

  openSearch() {
    const searchModal = document.querySelector('.search-modal');
    if (searchModal) {
      searchModal.classList.add('active');
      searchModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      
      const searchInput = searchModal.querySelector('.search-input');
      if (searchInput) {
        setTimeout(() => searchInput.focus(), 300);
      }
    }
  }
  
  setupSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const suggestionTags = document.querySelectorAll('.suggestion-tag');
    const recentItems = document.querySelectorAll('.recent-search-item');
    
    if (searchInput) {
      // Real-time search suggestions
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        this.filterSearchSuggestions(query);
      });
      
      // Search on enter
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.performSearch(e.target.value);
        }
      });
    }
    
    // Suggestion tag clicks
    suggestionTags.forEach(tag => {
      tag.addEventListener('click', () => {
        const suggestion = tag.textContent;
        this.performSearch(suggestion);
      });
    });
    
    // Recent search clicks
    recentItems.forEach(item => {
      item.addEventListener('click', () => {
        const recentSearch = item.textContent;
        this.performSearch(recentSearch);
      });
    });
  }
  
  filterSearchSuggestions(query) {
    const suggestions = document.querySelectorAll('.suggestion-tag');
    suggestions.forEach(suggestion => {
      const text = suggestion.textContent.toLowerCase();
      if (text.includes(query)) {
        suggestion.style.display = 'inline-block';
        suggestion.style.opacity = '1';
      } else {
        suggestion.style.opacity = '0.5';
      }
    });
  }
  
  performSearch(query) {
    if (query.trim()) {
      // Store recent search
      this.storeRecentSearch(query);
      
      // Perform search (redirect to search page or show results)
      window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }
  }
  
  storeRecentSearch(query) {
    let recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    
    // Remove if already exists
    recentSearches = recentSearches.filter(item => item !== query);
    
    // Add to beginning
    recentSearches.unshift(query);
    
    // Keep only last 5 searches
    recentSearches = recentSearches.slice(0, 5);
    
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
    this.updateRecentSearches();
  }
  
  updateRecentSearches() {
    const recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    const recentContainer = document.querySelector('.recent-searches');
    
    if (recentContainer && recentSearches.length > 0) {
      recentContainer.innerHTML = recentSearches.map(search => 
        `<span class="recent-search-item">${search}</span>`
      ).join('');
      
      // Re-attach event listeners
      recentContainer.querySelectorAll('.recent-search-item').forEach(item => {
        item.addEventListener('click', () => {
          this.performSearch(item.textContent);
        });
      });
    }
  }

  // Public methods for external use
  showLoading() {
    this.header.classList.add('loading');
  }

  hideLoading() {
    this.header.classList.remove('loading');
  }

  setActiveLink(url) {
    // Remove all active states
    document.querySelectorAll('.header-nav-link').forEach(link => {
      link.classList.remove('active');
    });
    
    // Add active state to current page
    const currentLink = document.querySelector(`.header-nav-link[href="${url}"]`);
    if (currentLink) {
      currentLink.classList.add('active');
    }
  }

  updateUserInfo(userData) {
    // Update user profile information
    const userNameElement = document.querySelector('.header-user-name');
    const userAvatarElement = document.querySelector('.header-user-avatar');
    
    if (userNameElement && userData.name) {
      userNameElement.textContent = userData.name;
    }
    
    if (userAvatarElement && userData.avatar) {
      userAvatarElement.style.backgroundImage = `url(${userData.avatar})`;
      userAvatarElement.innerHTML = '';
    }
  }
  
}

// Initialize header when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const header = new StandardHeader();
  
  // Make header instance globally available
  window.standardHeader = header;
  
  // Set active link based on current page
  const currentPath = window.location.pathname;
  header.setActiveLink(currentPath);
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StandardHeader;
}
