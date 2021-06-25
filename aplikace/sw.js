const ver = "0.1";
const cacheName = "brzdenka-${ver}";
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(cacheName).then(cache => {
      return cache.addAll([
        '/',
        'favicon.ico',
        'index.html',
        'logika.py',
        'manifest.webmanifest',
        'styl.css',
        'fonty/Montserrat-Regular.woff2',
        'fonty/RobotoSlab-Regular.woff2',
        // 'knihovny/brython/brython_stdlib.js',
        'knihovny/brython/brython.js',
        'knihovny/brython/unicode.txt',
        // 'obrazky/zob-popka.jpg',
        // 'obrazky/zob-popka.webp',
        'obrazky/zob-txtgrafika.png',
        'obrazky/zob-txtgrafika-cerna.png',
        'obrazky/ikony/android-chrome-192x192.png',
        'obrazky/ikony/android-chrome-512x512.png',
        'obrazky/ikony/apple-touch-icon.png',
        'obrazky/ikony/browserconfig.xml',
        'obrazky/ikony/favicon-16x16.png',
        'obrazky/ikony/favicon-32x32.png',
        'obrazky/ikony/favicon.ico',
        'obrazky/ikony/logo.svg',
        'obrazky/ikony/mstile-70x70.png',
        'obrazky/ikony/mstile-144x144.png',
        'obrazky/ikony/mstile-150x150.png',
        'obrazky/ikony/mstile-310x150.png',
        'obrazky/ikony/mstile-310x310.png',
        'obrazky/ikony/safari-pinned-tab.svg'
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
