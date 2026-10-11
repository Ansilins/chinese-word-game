// Keeps the Chinese word game working offline. Every cache name starts with "cwg-".
// The build fills in VERSION, VENDOR_VERSION and SHELL.
const VERSION = "__VERSION__";
const SHELL = __SHELL__;
const SHELL_CACHE = "cwg-shell-" + VERSION;
// the speech checker's engine: large, so it is saved only once someone uses speaking practice, and kept until it changes
const VENDOR_CACHE = "cwg-vendor-__VENDOR_VERSION__";
const PAGE = new URL("index.html", self.registration.scope).href;
const ROOT = new URL("./", self.registration.scope).href;

self.addEventListener("install", e => {
  e.waitUntil(caches.open(SHELL_CACHE)
    .then(c => c.addAll(SHELL.map(u => new Request(u, { cache: "reload" }))))
    .then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys
      // only this game's own old caches: the German game on the same address keeps its own
      .filter(k => (k.startsWith("cwg-shell-") && k !== SHELL_CACHE) || (k.startsWith("cwg-vendor-") && k !== VENDOR_CACHE))
      .map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// the game opens from the cache straight away, and a fresh copy is saved for the next launch
async function page(e) {
  const cache = await caches.open(SHELL_CACHE);
  const hit = await cache.match(PAGE);
  const fresh = fetch(PAGE, { cache: "no-cache", credentials: "same-origin" }).then(res => {
    if (res.ok && res.status === 200 && !res.redirected) return cache.put(PAGE, res.clone()).catch(() => {}).then(() => res);
    return res;
  });
  if (hit) { e.waitUntil(fresh.catch(() => {})); return hit; }
  return fresh.catch(() => new Response("You're offline and the game hasn't been saved on this device yet. Connect once and open it again.",
    { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } }));
}

async function vendor(req) {
  const cache = await caches.open(VENDOR_CACHE);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok && res.status === 200) await cache.put(req, res.clone()).catch(() => {}); // a full phone shouldn't break a good download
  return res;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return; // the speech model comes from elsewhere and is cached by the checker itself
  if (req.mode === "navigate") {
    const u = url.origin + url.pathname;
    if (u === ROOT || u === PAGE) e.respondWith(page(e)); // other files opened directly go to the network as they are
    return;
  }
  if (url.pathname.includes("/vendor/")) { e.respondWith(vendor(req)); return; }
  // look only in this game's own cache, never in the German game's
  e.respondWith(caches.open(SHELL_CACHE).then(c => c.match(req, { ignoreSearch: true })).catch(() => null).then(hit => hit || fetch(req)));
});
