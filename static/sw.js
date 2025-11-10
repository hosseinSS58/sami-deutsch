/**
 * Service Worker for PWA functionality
 * Handles caching, offline support, and performance optimization
 */

const CACHE_NAME = 'sami-deutsch-v1';
const urlsToCache = [
  '/',
  '/static/css/app.css',
  '/static/css/header-standard.css',
  '/static/css/forms.css',
  '/static/css/animations.css',
  '/static/css/search-modal.css',
  '/static/css/home-mobile.css',
  '/static/css/mobile-input-fix.css',
  '/static/js/mobile-navigation.js',
  '/static/js/accessibility.js',
  '/static/js/search.js',
  '/static/js/header-standard.js',
  '/static/img/favicon.svg',
  '/static/img/logo.svg'
];

// Install event - cache resources
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
      .catch(function(error) {
        console.error('Cache installation failed:', error);
      })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(function(response) {
          // Check if valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then(function(cache) {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        }).catch(function() {
          // Return offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/offline.html');
          }
        });
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for offline actions
self.addEventListener('sync', function(event) {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Handle offline actions when connection is restored
  return new Promise(function(resolve) {
    // Implement background sync logic here
    console.log('Background sync completed');
    resolve();
  });
}

// Push notifications
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'پیام جدید از Sami Deutsch',
    icon: '/static/img/icon-192x192.png',
    badge: '/static/img/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'مشاهده',
        icon: '/static/img/icon-explore.png'
      },
      {
        action: 'close',
        title: 'بستن',
        icon: '/static/img/icon-close.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Sami Deutsch', options)
  );
});

// Notification click
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});



