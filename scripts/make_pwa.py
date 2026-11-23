#!/usr/bin/env python3
"""Inject PWA/iOS meta tags and service-worker registration into the source HTML."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/nigga/Загрузки/gemini-code-1795445316832.html")
DST = ROOT / "www" / "index.html"

html = SRC.read_text(encoding="utf-8")

html = html.replace("<title>Larp Keeper</title>", "<title>Keeper</title>", 1)

head_inject = """<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Keeper">
<meta name="application-name" content="Keeper">
<meta name="theme-color" content="#0d131c">
<meta name="description" content="Keeper — демо-кошелёк">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="180x180" href="icons/icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="manifest" href="manifest.json">
"""
needle = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
assert needle in html, "viewport meta not found"
html = html.replace(needle, needle + head_inject, 1)

sw_inject = """
<script>
if ('serviceWorker' in navigator) {
  addEventListener('load', function () {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  });
}
</script>
"""
assert "</body>" in html
html = html.replace("</body>", sw_inject + "</body>", 1)

DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(html, encoding="utf-8")
print(f"Wrote {DST} ({len(html)} bytes)")
