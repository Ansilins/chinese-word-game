# Builds the home-screen web app (index.html, sw.js, manifest.webmanifest, asr-worker.js) from the game template and the HSK word lists.
# Run from the repository root: python3 src/build.py
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
read = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()

t = read("src/template.html")
for key, f in (("HSK1", "hsk1-words.json"), ("HSK2", "hsk2-words.json")):
    words = read("src/" + f)
    json.loads(words)
    marker = f"/*{key}WORDS*/[]"
    if t.count(marker) != 1: sys.exit("template marker missing: " + marker)
    t = t.replace(marker, words.strip())

FONTS = [("Bricolage Grotesque", "bricolage-grotesque", 500), ("Bricolage Grotesque", "bricolage-grotesque", 700),
         ("Bricolage Grotesque", "bricolage-grotesque", 800), ("Atkinson Hyperlegible", "atkinson-hyperlegible", 400),
         ("Atkinson Hyperlegible", "atkinson-hyperlegible", 700), ("Kalam", "kalam", 400), ("Kalam", "kalam", 700)]
font_files = [f"fonts/{f}-latin-{w}-normal.woff2" for _, f, w in FONTS]
faces = "".join(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:swap;src:url("{path}") format("woff2")}}'
                for (fam, _, w), path in zip(FONTS, font_files))

def swap(old, new, pattern=False):
    global t
    n = len(re.findall(old, t)) if pattern else t.count(old)
    if n < 1: sys.exit("not found in template: " + old[:80])
    t = re.sub(old, new, t) if pattern else t.replace(old, new)

# (the template has no preconnect links: nothing is fetched from Google)
swap(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>', '<style>' + faces + '</style>', pattern=True)
swap("Your progress stays in this browser.", "Your progress is saved on this device.")

# the template's title and styles go in the head, the rest is the page
cut = t.index("</style>\n", t.index("<style>\n")) + len("</style>\n")
head_part, body_part = t[:cut], t[cut:]

head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Learn Chinese HSK 1 and HSK 2 words in small units: flashcards, quizzes, listening, matching, tones and pronunciation practice, plus pinyin basics.">
<meta name="theme-color" content="#1f2c27">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="汉语">
<meta name="application-name" content="汉语 Word Game">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="preload" href="fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>
window.cwgPwa = true;
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").then(reg => {
  // a Home Screen app is usually resumed rather than reloaded, so look for a new version whenever it comes back
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") reg.update().catch(() => {}); });
}).catch(() => {}));
// in the Home Screen app, ask to keep the saved progress even when the phone is short of space
try { if (navigator.standalone === true || matchMedia("(display-mode: standalone)").matches) navigator.storage.persist().catch(() => {}); } catch (e) {}
</script>
<style>
html,body{margin:0}
img{max-width:100%}
/* full screen on a phone: the clock and battery sit over a chalkboard strip */
body::before{content:"";position:fixed;z-index:50;left:0;right:0;top:0;height:env(safe-area-inset-top,0px);background:#1f2c27;pointer-events:none}
</style>
"""
html = head + head_part + "</head>\n<body>\n" + body_part + "\n</body>\n</html>\n"
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)

icons = ["icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "icons/favicon-32.png"]
manifest = {
    "name": "Chinese Word Game · 汉语", "short_name": "汉语",
    "description": "Learn Chinese HSK 1 and HSK 2 words in small units, plus pinyin basics.",
    "id": "./", "start_url": "./", "scope": "./", "display": "standalone", "lang": "en",
    "background_color": "#1f2c27", "theme_color": "#1f2c27",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        {"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
    ],
}
open(os.path.join(ROOT, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

shell = ["./", "index.html", "manifest.webmanifest", "asr-worker.js", "lib/pinyin-pro.min.js"] + font_files + icons
open(os.path.join(ROOT, "asr-worker.js"), "w").write(read("src/asr-worker.js"))
h = hashlib.sha256()
for p in shell[1:]:
    h.update(open(os.path.join(ROOT, p), "rb").read())
hv = hashlib.sha256()
for f in sorted(os.listdir(os.path.join(ROOT, "vendor"))):
    hv.update(f.encode()); hv.update(open(os.path.join(ROOT, "vendor", f), "rb").read())
sw = (read("src/sw.js").replace("__VERSION__", h.hexdigest()[:12]).replace("__VENDOR_VERSION__", hv.hexdigest()[:12])
      .replace("__SHELL__", json.dumps(shell)))
open(os.path.join(ROOT, "sw.js"), "w").write(sw)
print("built index.html", len(html), "bytes, version", h.hexdigest()[:12])
