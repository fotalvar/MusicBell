const CACHE_NAME = "musicbell-v1";
const ASSETS_TO_CACHE = [
  "/",
  "/index.html",
  "/style.css",
  "/script.js",
  "/manifest.json",
  "/images/icon-192.png",
  "/images/icon-512.png",
];

// Instalar service worker
self.addEventListener("install", (event) => {
  console.log("🔧 Service Worker instalando...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("📦 Cacheando archivos...");
      return cache.addAll(ASSETS_TO_CACHE);
    }),
  );
  self.skipWaiting();
});

// Activar service worker
self.addEventListener("activate", (event) => {
  console.log("✅ Service Worker activado");
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log("🗑️ Borrando cache antigua:", cacheName);
            return caches.delete(cacheName);
          }
        }),
      );
    }),
  );
  self.clients.claim();
});

// Interceptar requests
self.addEventListener("fetch", (event) => {
  // Solo cachear GET requests
  if (event.request.method !== "GET") {
    return;
  }

  // Estrategia: Cache first, fallback to network
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        if (response) {
          console.log("📚 Desde cache:", event.request.url);
          return response;
        }

        return fetch(event.request).then((response) => {
          // No cachear requests fallidas
          if (
            !response ||
            response.status !== 200 ||
            (response.type === "basic" && event.request.url.includes("/api/"))
          ) {
            return response;
          }

          // Clonar la response
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });

          return response;
        });
      })
      .catch(() => {
        console.log("❌ Request fallido:", event.request.url);
        // Fallback a página offline si existe
        if (event.request.destination === "document") {
          return caches.match("/index.html");
        }
      }),
  );
});

// Sincronización en background (cuando vuelve la conexión)
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-data") {
    event.waitUntil(
      fetch("/api/estado")
        .then(() => console.log("✅ Datos sincronizados"))
        .catch(() => console.log("❌ Error sincronizando")),
    );
  }
});
