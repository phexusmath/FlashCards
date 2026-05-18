const CACHE_NAME = 'flashcards-v1';
const ASSETS = [
  '/',
  '/index.html',
  'a1_combined.json',
  'a2_combined.json',
  'b1_combined.json',
  'b2_combined.json',
  'c1_combined.json',
  'c2_combined.json'
];

// Install the service worker and cache assets
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Fetch assets from cache if offline
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});