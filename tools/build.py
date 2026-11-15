#!/usr/bin/env python3
"""Builds index.html (and the shared header and footer of the plain pages) from tools/home.html and tools/frags.json.
The fragments are the approved board X8's scenes (pin positions on the globe pictures), cut from the design reference page."""
import json, pathlib, re
R = pathlib.Path(__file__).resolve().parent.parent
APP = 'https://apps.apple.com/us/app/pinr-travel-made-social/id6757422507'
PLAY = 'https://play.google.com/store/apps/details?id=com.builtbylee.app80days'
NAV = f'''<header class="nav"><div class="nav-in">
  <a class="brand" href="/" aria-label="Pinr home"><img class="l" src="/assets/v2/logo.webp" alt="" width="38" height="38"><img class="w" src="/assets/v2/word.webp" alt="Pinr" width="70" height="27"></a>
  <nav class="links" aria-label="Main"><a href="/#features">Features</a><a href="/#games">Games</a><a href="/faq.html">FAQ</a></nav>
  <a class="btn fill" href="/#get" data-get>Get the app</a>
</div></header>'''
STORES = f'''<div class="stores">
        <a class="store" href="{APP}"><img src="/assets/v2/badge-app-store.svg" alt="Download on the App Store" width="144" height="48"></a>
        <a class="store" href="{PLAY}"><img src="/assets/v2/badge-google-play.webp" alt="Get it on Google Play" width="161" height="48"></a>
      </div>'''
FOOT = '''<footer class="foot"><div class="foot-in">
  <nav aria-label="Footer"><a href="/faq.html">FAQ</a><a href="/privacy-policy.html">Privacy</a><a href="/terms-of-service.html">Terms</a><a href="mailto:lee@getpinr.com">Contact</a></nav>
  <span>&copy; 2026 Pinr. Built by Lee.</span>
</div></footer>'''
def page(t):
    return t.replace('{{nav}}', NAV).replace('{{stores}}', STORES).replace('{{footer}}', FOOT)
if __name__ == '__main__':
    f = json.loads((R / 'tools/frags.json').read_text())
    # the print in "Drop a pin" holds a real photo (CC0, Wikimedia Commons: Tranvia en Lisboa)
    f['sc1'] = re.sub(r'<div class="ph">.*?</div>', '<div class="ph"><img src="/assets/v2/photo-lisbon.webp" alt="" width="240" height="271"></div>', f['sc1'], count=1, flags=re.S)
    f['lb'] = f['lb'].replace('/assets/v2/MISSING-img/a3d4dc8f21.png.webp', '/assets/v2/pin-m.webp').replace('/assets/v2/MISSING-img/f2eae246ca.png.webp', '/assets/v2/pin-t.webp')
    t = page((R / 'tools/home.html').read_text())
    for k, v in f.items(): t = t.replace('{{' + k + '}}', v)
    assert '{{' not in t and 'MISSING' not in t, 'unfilled placeholder'
    (R / 'index.html').write_text(t)
    print('index.html', len(t))
