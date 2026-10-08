/* Muzej vasi Griblje — servisni delavec za namestitev in delovanje brez povezave.
   Strategija:
   - navigacije: mreža najprej, ob napaki predpomnjen odbit (SPA lupina)
   - /_next/static, /icons, /qr: cache-first (nezvezno / različno zgoščeno)
   - /images, /models, /atlas, /audio, /panoramas: stale-while-revalidate (osvežitev v ozadju)
   - /api/*: samo mreža (odprti podatki za zunanje uporabnike)
   - zunanji viri (OSM ploščice): pustimo brskalniku
   Dvigom različice VERSION se stare predpomnilnice očistijo samodejno. */

const VERSION = "mvg-v16";
const PAGE_CACHE = `${VERSION}-pages`;
const STATIC_CACHE = `${VERSION}-static`;
const ASSET_CACHE = `${VERSION}-assets`;

const PRECACHE = [
  "/",
  "/manifest.webmanifest",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/icons/icon-maskable-512.png",
  "/icons/apple-touch-icon.png",
];

const CACHE_FIRST =
  /^\/(_next\/static|icons|qr)\//;
const SWR =
  /^\/(images|models|atlas|audio|panoramas)\//;

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(PAGE_CACHE);
      await cache.addAll(PRECACHE);
      await self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))
      );
      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/api/")) return;

  /* navigacije: mreža najprej, odbit ob prekinitvi */
  if (request.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(request);
          const cache = await caches.open(PAGE_CACHE);
          cache.put("/", fresh.clone());
          return fresh;
        } catch {
          const cached =
            (await caches.match(request, { cacheName: PAGE_CACHE })) ||
            (await caches.match("/", { cacheName: PAGE_CACHE }));
          return (
            cached ||
            new Response("<h1>Muzej vasi Griblje — ni povezave</h1>", {
              status: 503,
              headers: { "Content-Type": "text/html; charset=utf-8" },
            })
          );
        }
      })()
    );
    return;
  }

  /* statika: cache-first */
  if (CACHE_FIRST.test(url.pathname)) {
    event.respondWith(
      (async () => {
        const cached = await caches.match(request);
        if (cached) return cached;
        try {
          const fresh = await fetch(request);
          if (fresh.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, fresh.clone());
          }
          return fresh;
        } catch {
          return cached || Response.error();
        }
      })()
    );
    return;
  }

  /* viri zbirke: stale-while-revalidate */
  if (SWR.test(url.pathname)) {
    event.respondWith(
      (async () => {
        const cached = await caches.match(request);
        const refresh = fetch(request)
          .then(async (fresh) => {
            if (fresh.ok) {
              const cache = await caches.open(ASSET_CACHE);
              cache.put(request, fresh.clone());
            }
            return fresh;
          })
          .catch(() => null);
        return cached || (await refresh) || Response.error();
      })()
    );
    return;
  }
});
