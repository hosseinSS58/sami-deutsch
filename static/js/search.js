document.addEventListener('DOMContentLoaded', function() {
  // ===== SEARCH MODAL FUNCTIONALITY =====
  
  const searchModal = document.querySelector('.search-modal');
  const searchModalClose = document.querySelector('.search-modal-close');
  const searchInput = document.querySelector('.search-modal-input');
  const searchResults = document.querySelector('.search-results');
  
  // Search Toggle Button
  const searchToggle = document.querySelector('.search-toggle');
  if (searchToggle) {
    searchToggle.addEventListener('click', function() {
      if (searchModal) {
        searchModal.classList.add('show');
        if (searchInput) {
          searchInput.focus();
        }
      }
    });
  }
  
  // Close Search Modal
  if (searchModalClose) {
    searchModalClose.addEventListener('click', function() {
      searchModal.classList.remove('show');
    });
  }
  
  // Close on backdrop click
  if (searchModal) {
    searchModal.addEventListener('click', function(e) {
      if (e.target === searchModal) {
        searchModal.classList.remove('show');
      }
    });
  }
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && searchModal && searchModal.classList.contains('show')) {
      searchModal.classList.remove('show');
    }
  });
  
  // Search Input Functionality
  if (searchInput) {
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
      clearTimeout(searchTimeout);
      const query = this.value.trim();
      
      if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
      }
      
      // Show loading state
      searchResults.innerHTML = `
        <div class="search-loading">
          <i class="fas fa-spinner fa-spin"></i>
          <p>در حال جستجو...</p>
        </div>
      `;
      
      searchTimeout = setTimeout(() => {
        performSearch(query);
      }, 300);
    });
    
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const query = this.value.trim();
        if (query) {
          performSearch(query);
        }
      }
    });
  }
  
  // ===== SEARCH FUNCTION =====
  
  async function performSearch(query) {
    try {
      // Try to fetch real search results from Django backend
      const response = await fetch(`/search/suggest/?q=${encodeURIComponent(query)}`);
      
      if (response.ok) {
        const data = await response.json();
        
        if (data.suggestions && data.suggestions.length > 0) {
          // Show suggestions from backend
          displaySuggestions(data.suggestions, query);
        } else {
          // No suggestions found, show search options
          displaySearchOptions(query);
        }
      } else {
        // Fallback to search options
        displaySearchOptions(query);
      }
    } catch (error) {
      console.error('Search error:', error);
      // Fallback to search options
      displaySearchOptions(query);
    }
  }
  
  // ===== DISPLAY FUNCTIONS =====
  
  // Display search suggestions from backend
  function displaySuggestions(suggestions, query) {
    searchResults.innerHTML = `
      <div class="search-suggestions-results">
        <div class="search-results-header mb-3">
          <h6 class="mb-2">پیشنهادات برای: "${query}"</h6>
          <p class="text-muted small mb-0">نتایج یافت شده در محتوای سایت</p>
        </div>
        <div class="search-suggestions-list">
          ${suggestions.map(suggestion => `
            <div class="search-suggestion-item">
              <div class="suggestion-content">
                <i class="fas fa-lightbulb text-warning me-2"></i>
                <span class="suggestion-text">${suggestion}</span>
              </div>
              <button class="btn btn-sm btn-outline-primary" onclick="searchForSuggestion('${suggestion}')">
                <i class="fas fa-search me-1"></i>جستجو
              </button>
            </div>
          `).join('')}
        </div>
        <div class="search-actions mt-3">
          <a href="/search/?q=${encodeURIComponent(query)}" class="btn btn-primary">
            <i class="fas fa-search me-1"></i>جستجوی کامل
          </a>
        </div>
      </div>
    `;
  }
  
  // Display search options when no specific results found
  function displaySearchOptions(query) {
    searchResults.innerHTML = `
      <div class="search-options">
        <div class="search-results-header mb-3">
          <h6 class="mb-2">جستجو برای: "${query}"</h6>
          <p class="text-muted small mb-0">انتخاب کنید کجا جستجو کنید</p>
        </div>
        
        <div class="search-categories">
          <div class="search-category-item" onclick="searchInCategory('videos', '${query}')">
            <div class="category-icon">
              <i class="fas fa-video fa-2x text-primary"></i>
            </div>
            <div class="category-content">
              <h6 class="category-title">ویدیوها</h6>
              <p class="category-description">جستجو در ویدیوها، تگ‌ها و موضوعات</p>
            </div>
            <div class="category-arrow">
              <i class="fas fa-chevron-left"></i>
            </div>
          </div>
          
          <div class="search-category-item" onclick="searchInCategory('blog', '${query}')">
            <div class="category-icon">
              <i class="fas fa-newspaper fa-2x text-success"></i>
            </div>
            <div class="category-content">
              <h6 class="category-title">مقالات</h6>
              <p class="category-description">جستجو در مقالات و دسته‌بندی‌ها</p>
            </div>
            <div class="category-arrow">
              <i class="fas fa-chevron-left"></i>
            </div>
          </div>
          
          <div class="search-category-item" onclick="searchInCategory('shop', '${query}')">
            <div class="category-icon">
              <i class="fas fa-shopping-bag fa-2x text-warning"></i>
            </div>
            <div class="category-content">
              <h6 class="category-title">فروشگاه</h6>
              <p class="category-description">جستجو در محصولات و منابع آموزشی</p>
            </div>
            <div class="category-arrow">
              <i class="fas fa-chevron-left"></i>
            </div>
          </div>
        </div>
        
        <div class="search-actions mt-3">
          <a href="/search/?q=${encodeURIComponent(query)}" class="btn btn-primary">
            <i class="fas fa-search me-1"></i>جستجوی کامل در همه بخش‌ها
          </a>
        </div>
      </div>
    `;
  }
  
  // ===== SEARCH CATEGORY FUNCTIONS =====
  
  // Search in specific category
  window.searchInCategory = function(category, query) {
    let url = '';
    let title = '';
    
    switch (category) {
      case 'videos':
        url = `/videos/?search=${encodeURIComponent(query)}`;
        title = 'ویدیوها';
        break;
      case 'blog':
        url = `/blog/?q=${encodeURIComponent(query)}`;
        title = 'مقالات';
        break;
      case 'shop':
        url = `/shop/?search=${encodeURIComponent(query)}`;
        title = 'فروشگاه';
        break;
    }
    
    if (url) {
      // Show confirmation before redirecting
      searchResults.innerHTML = `
        <div class="search-redirect-confirmation text-center">
          <div class="redirect-icon mb-3">
            <i class="fas fa-external-link-alt fa-3x text-primary"></i>
          </div>
          <h6 class="mb-2">انتقال به ${title}</h6>
          <p class="text-muted mb-3">جستجو برای "${query}" در بخش ${title}</p>
          <div class="redirect-actions">
            <a href="${url}" class="btn btn-primary">
              <i class="fas fa-external-link-alt me-1"></i>انتقال
            </a>
            <button class="btn btn-outline-secondary ms-2" onclick="displaySearchOptions('${query}')">
              <i class="fas fa-arrow-left me-1"></i>بازگشت
            </button>
          </div>
        </div>
      `;
    }
  };
  
  // Search for specific suggestion
  window.searchForSuggestion = function(suggestion) {
    // Redirect to full search with the suggestion
    window.location.href = `/search/?q=${encodeURIComponent(suggestion)}`;
  };
  
  // ===== SEARCH SUGGESTIONS =====
  
  // Add quick search suggestions
  function addQuickSearchSuggestions() {
    const suggestions = [
      { text: 'زبان آلمانی', category: 'videos', icon: 'video' },
      { text: 'گرامر', category: 'videos', icon: 'video' },
      { text: 'مکالمه', category: 'videos', icon: 'video' },
      { text: 'واژگان', category: 'videos', icon: 'video' },
      { text: 'تلفظ', category: 'videos', icon: 'video' },
      { text: 'آموزش', category: 'blog', icon: 'newspaper' },
      { text: 'نکات', category: 'blog', icon: 'newspaper' },
      { text: 'کتاب', category: 'shop', icon: 'shopping-bag' },
      { text: 'آزمون', category: 'assessments', icon: 'clipboard-check' }
    ];
    
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-quick-suggestions mt-3';
    suggestionsContainer.innerHTML = `
      <p class="text-muted small mb-2">جستجوهای سریع:</p>
      <div class="search-quick-suggestions-tags">
        ${suggestions.map(suggestion => 
          `<span class="search-quick-suggestion-tag" data-text="${suggestion.text}" data-category="${suggestion.category}">
            <i class="fas fa-${suggestion.icon} me-1"></i>
            ${suggestion.text}
          </span>`
        ).join('')}
      </div>
    `;
    
    // Add suggestions after search input
    const searchInputContainer = document.querySelector('.search-input-container');
    if (searchInputContainer) {
      searchInputContainer.appendChild(suggestionsContainer);
    }
    
    // Add click events for quick suggestions
    const quickSuggestionTags = document.querySelectorAll('.search-quick-suggestion-tag');
    quickSuggestionTags.forEach(tag => {
      tag.addEventListener('click', function() {
        const text = this.getAttribute('data-text');
        const category = this.getAttribute('data-category');
        
        // Set search input value
        if (searchInput) {
          searchInput.value = text;
        }
        
        // Search in specific category
        searchInCategory(category, text);
      });
    });
  }
  
  // Initialize quick search suggestions when modal opens
  function initializeSearchModal() {
    if (searchModal) {
      searchModal.addEventListener('show', function() {
        // Clear previous results
        if (searchResults) {
          searchResults.innerHTML = '';
        }
        
        // Add suggestions if not already added
        if (!document.querySelector('.search-quick-suggestions')) {
          addQuickSearchSuggestions();
        }
      });
    }
  }
  
  // Call initialization
  initializeSearchModal();
  
  // ===== MOBILE NAVIGATION ANIMATIONS =====
  
  // Mobile Navigation Toggle
  const mobileToggle = document.querySelector('.navbar-toggler');
  const mobileMenu = document.querySelector('#mobileMenu');
  
  if (mobileToggle && mobileMenu) {
    // Prevent double animation
    let isAnimating = false;
    
    mobileToggle.addEventListener('click', function() {
      if (isAnimating) return;
      
      isAnimating = true;
      
      if (mobileMenu.classList.contains('show')) {
        // Closing animation
        mobileMenu.classList.add('closing');
        setTimeout(() => {
          mobileMenu.classList.remove('show', 'closing');
          isAnimating = false;
        }, 300);
      } else {
        // Opening animation
        mobileMenu.classList.add('show');
        
        // Ensure all items are visible
        const mobileItems = mobileMenu.querySelectorAll('.mobile-nav li');
        mobileItems.forEach((item, index) => {
          item.style.opacity = '1';
          item.style.visibility = 'visible';
          item.style.transform = 'translateY(0)';
        });
        
        setTimeout(() => {
          isAnimating = false;
        }, 300);
      }
    });
    
    // Close on backdrop click
    const backdrop = document.querySelector('.offcanvas-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', function() {
        if (!isAnimating) {
          isAnimating = true;
          mobileMenu.classList.add('closing');
          setTimeout(() => {
            mobileMenu.classList.remove('show', 'closing');
            isAnimating = false;
          }, 300);
        }
      });
    }
    
    // Reset items visibility when menu opens
    mobileMenu.addEventListener('show.bs.offcanvas', function() {
      const mobileItems = mobileMenu.querySelectorAll('.mobile-nav li');
      mobileItems.forEach((item, index) => {
        item.style.opacity = '1';
        item.style.visibility = 'visible';
        item.style.transform = 'translateY(0)';
      });
      
      // Force scroll to work
      const offcanvasBody = mobileMenu.querySelector('.offcanvas-body');
      const mobileNav = mobileMenu.querySelector('.mobile-nav');
      
      if (offcanvasBody) {
        offcanvasBody.style.overflowY = 'auto';
        offcanvasBody.style.overflowX = 'hidden';
        offcanvasBody.style.webkitOverflowScrolling = 'touch';
      }
      
      if (mobileNav) {
        mobileNav.style.overflowY = 'auto';
        mobileNav.style.overflowX = 'hidden';
        mobileNav.style.webkitOverflowScrolling = 'touch';
      }
    });
  }
  
  // ===== MOBILE USER ACCOUNT BUTTON FUNCTIONALITY =====
  
  // Mobile User Account Dropdown
  const mobileUserAccountDropdown = document.querySelector('.mobile-user-account-dropdown');
  if (mobileUserAccountDropdown) {
    const dropdownToggle = mobileUserAccountDropdown.querySelector('.mobile-user-account-toggle');
    const dropdownMenu = mobileUserAccountDropdown.querySelector('.mobile-user-account-menu');
    
    // Toggle dropdown
    dropdownToggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      mobileUserAccountDropdown.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!mobileUserAccountDropdown.contains(e.target)) {
        mobileUserAccountDropdown.classList.remove('show');
      }
    });
    
    // Close dropdown on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && mobileUserAccountDropdown.classList.contains('show')) {
        mobileUserAccountDropdown.classList.remove('show');
      }
    });
    
    // Add hover effect for dropdown items
    const dropdownItems = dropdownMenu.querySelectorAll('.mobile-user-account-action, .mobile-user-account-action-btn');
    dropdownItems.forEach(item => {
      item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(-3px)';
      });
      
      item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
      });
    });
  }
  
  // ===== GLOBAL SEARCH MODAL FUNCTION =====
  
  // Function to open search modal (for mobile search button)
  window.openSearchModal = function() {
    const searchModal = document.querySelector('.search-modal');
    if (searchModal) {
      searchModal.classList.add('show');
      const searchInput = searchModal.querySelector('.search-modal-input');
      if (searchInput) {
        searchInput.focus();
      }
      
      // Initialize suggestions when modal opens
      if (!document.querySelector('.search-quick-suggestions')) {
        addQuickSearchSuggestions();
      }
    }
  };
});
