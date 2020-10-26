const version = '0.A.3'
const cacheName = 'brzdenka-${version}';
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(cacheName).then(cache => {
      return cache.addAll([
        '/',
        'brython/brython.js',
        // 'brython/brython_stdlib.js',
        'brython/unicode.txt',
        'fonty/Montserrat-Regular.woff2',
        'fonty/RobotoSlab-Regular.woff2',
        'obrazky/favicon/browserconfig.xml',
        'obrazky/favicon/site.webmanifest',
        'obrazky/favicon/safari-pinned-tab.svg',
        'obrazky/favicon/favicon.ico',
        'obrazky/favicon/android-chrome-192x192.png',
        'obrazky/favicon/android-chrome-512x512.png',
        'obrazky/favicon/apple-touch-icon.png',
        'obrazky/favicon/favicon-16x16.png',
        'obrazky/favicon/favicon-32x32.png',
        'obrazky/favicon/mstile-70x70.png',
        'obrazky/favicon/mstile-144x144.png',
        'obrazky/favicon/mstile-150x150.png',
        'obrazky/favicon/mstile-310x150.png',
        'obrazky/favicon/mstile-310x310.png',
        'obrazky/vystraha-safari.svg',
        'obrazky/vystraha.svg',
        'obrazky/zob-popka.jpg',
        'favicon.ico',
        'index.html',
        'logika.py',
        'styly.css'
      ])
          .then(() => self.skipWaiting());
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.open(cacheName)
      .then(cache => cache.match(event.request, {ignoreSearch: true}))
      .then(response => {
      return response || fetch(event.request);
    })
  );
});
