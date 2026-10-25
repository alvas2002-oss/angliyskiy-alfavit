#!/usr/bin/env python3
"""Build the standalone phone copy of «Тося и английский алфавит».

Source of truth: /root/tosya-academy/work/lessons/angliyskiy-alfavit.html (an artifact page fragment
without <html>/<head>/<body>). This script wraps it into a full page with an install manifest, home-screen
icons and a service worker, so the lesson opens from the phone's home screen and works offline after the first visit.
"""
from pathlib import Path

SRC = Path("/root/tosya-academy/work/lessons/angliyskiy-alfavit.html")
OUT = Path(__file__).parent

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#ffd43b">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Алфавит">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)} body{margin:0} [hidden]{display:none!important}</style>
"""

SW = """<script>
if ('serviceWorker' in navigator) window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
</script>
"""

page = SRC.read_text(encoding="utf-8")
page = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
style_end = page.index("</style>") + len("</style>")
html = HEAD + page[:style_end] + "\n</head>\n<body>\n" + page[style_end:] + "\n" + SW + "</body>\n</html>\n"
(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / ".nojekyll").write_text("")
print(f"index.html: {len(html)} bytes")
