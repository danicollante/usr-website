#!/usr/bin/env python3
"""Shared page shell: head, header, footer, image helpers.

Header/footer live here once so the logo, nav and disclaimer cannot drift
between pages. Output is plain static HTML — no runtime dependency.
"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "site")
MANIFEST = json.load(open(os.path.join(ROOT, "assets", "img", "manifest.json")))

SITE = "U.S. Strategic Resources"
EMAIL = "info@usstrategicresources.com"

NAV = [
    ("about.html",      "About"),
    ("leadership.html", "Leadership"),
    ("metals.html",     "Metals &amp; Markets"),
    ("news.html",       "News"),
]

# The exploration-stage constraint. Present on every page, clearly legible.
DISCLAIMER = ("Exploration stage. Prospectivity models are interpretive and "
              "conceptual; no mineral resource or reserve has been defined on "
              "either license.")


def img(slug, alt, sizes, cls="", ratio_class="", loading="lazy",
        fetchpriority=None, decoding="async"):
    """<picture> with WebP + JPEG fallback, srcset/sizes, explicit w/h."""
    m = MANIFEST[slug]
    widths = m["widths"]
    big = max(widths)
    w, h = m["native"]
    out_h = round(big * h / w)
    webp = ", ".join(f"assets/img/{slug}-{x}.webp {x}w" for x in widths)
    jpg = ", ".join(f"assets/img/{slug}-{x}.jpg {x}w" for x in widths)
    fp = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    return (
        f'<picture>'
        f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
        f'<img src="assets/img/{slug}-{big}.jpg" srcset="{jpg}" sizes="{sizes}" '
        f'alt="{alt}" width="{big}" height="{out_h}" '
        f'loading="{loading}" decoding="{decoding}"{fp}{cls}>'
        f'</picture>'
    )


def head(title, desc, current, extra=""):
    nav = []
    for href, label in NAV:
        aria = ' aria-current="page"' if href == current else ""
        nav.append(f'<a href="{href}"{aria}>{label}</a>')
    nav.append('<a class="nav__cta" href="contact.html">Contact</a>')
    nav_html = "\n            ".join(nav)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="assets/logo/favicon-USR-new.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500;6..72,600&amp;family=Public+Sans:wght@300;400;500;600;700&amp;family=JetBrains+Mono:wght@300;400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(current, inside_hero=False):
    nav = []
    for href, label in NAV:
        aria = ' aria-current="page"' if href == current else ""
        nav.append(f'<a href="{href}"{aria}>{label}</a>')
    nav.append('<a class="nav__cta" href="contact.html">Contact</a>')
    nav_html = "\n          ".join(nav)
    return f"""    <header class="site-header">
      <div class="site-header__inner">
        <a class="site-header__logo" href="index.html" aria-label="{SITE} — home">
          <img src="assets/logo/USR-logo-on-dark-new.svg" alt="{SITE}" width="291" height="83">
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
        <nav class="nav" id="nav" aria-label="Primary">
          {nav_html}
        </nav>
      </div>
    </header>
"""


def footer():
    return f"""
  <div class="disclaimer-bar">
    <div class="wrap disclaimer-bar__inner">
      <p class="label">Exploration stage</p>
      <p>{DISCLAIMER}</p>
    </div>
  </div>

  <footer class="site-footer">
    <div class="wrap">
      <div class="site-footer__grid">
        <div>
          <div class="site-footer__logo">
            <img src="assets/logo/USR-logo-on-dark-new.svg" alt="{SITE}" width="291" height="83">
          </div>
          <p>An American-backed mining investment vehicle exploring for critical
             minerals and rare earths in Nimba County, Liberia.</p>
        </div>
        <div>
          <p class="footer-nav__title">Company</p>
          <ul class="footer-nav">
            <li><a href="about.html">About</a></li>
            <li><a href="leadership.html">Leadership</a></li>
            <li><a href="metals.html">Metals &amp; Markets</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-nav__title">More</p>
          <ul class="footer-nav">
            <li><a href="news.html">News</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="legal.html">Legal</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-nav__title">Contact</p>
          <ul class="footer-nav">
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Monrovia, Liberia</li>
          </ul>
        </div>
      </div>
      <div class="site-footer__legal">
        <span>&copy; 2026 {SITE}. All rights reserved.</span>
        <span>Nimba County, Liberia &middot; Exploration stage</span>
      </div>
    </div>
  </footer>

  <script src="js/interactions.js" defer></script>
</body>
</html>
"""


# The signature map — Liberia, the two license areas, and the 243 km
# Yekepa–Buchanan rail corridor to deep water. Geometry and labels taken
# from the design file.
MAP = """      <figure class="map">
        <svg viewBox="0 0 440 450" role="img"
             aria-label="Map of Liberia showing the Nimba 1 and Nimba 2 exploration licenses and the 243 km Yekepa to Buchanan rail corridor to deep water">
          <defs>
            <radialGradient id="nimbaHalo" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#89B8E1" stop-opacity=".5"></stop>
              <stop offset="100%" stop-color="#89B8E1" stop-opacity="0"></stop>
            </radialGradient>
          </defs>
          <polygon class="map__outline" points="13,179 40,148 61,128 95,93 132,21 170,35 185,15 210,35 224,75 260,128 300,100 307,112 330,160 340,180 312,220 330,260 365,280 405,340 420,390 405,435 360,410 310,395 260,370 220,355 155,282 125,250 80,239 40,210"
                   fill="rgba(91,155,213,.07)" stroke="rgba(137,184,225,.5)" stroke-width="1.25" stroke-linejoin="round"></polygon>
          <g fill="none" stroke="rgba(242,245,248,.12)" stroke-width="1"><path d="M13,179 L40,210"></path></g>
          <!-- Soft halo on Nimba 1, centred on the licence, reusing the same
               pulseNode keyframe as the Yekepa node rather than a bespoke
               animation. -->
          <circle class="map__pulse" cx="308" cy="113" r="58" fill="url(#nimbaHalo)"></circle>
          <!-- Nimba 1 sits essentially at Yekepa, right where the rail
               corridor terminates; Nimba 2 is immediately south, sharing
               Nimba 1's lower edge so the pair reads as contiguous. -->
          <polygon points="280,95 330,88 336,130 286,140" fill="rgba(91,155,213,.28)" stroke="#5B9BD5" stroke-width="1.5"></polygon>
          <polygon points="286,140 336,130 342,172 292,182" fill="rgba(91,155,213,.14)" stroke="#5B9BD5" stroke-width="1.5" stroke-dasharray="4 3"></polygon>
          <path class="map__rail" d="M307,112 C296,158 258,192 222,224 C198,246 172,268 155,282"
                fill="none" stroke="#89B8E1" stroke-width="2" stroke-linecap="round"></path>
          <circle cx="307" cy="112" r="4" fill="#89B8E1"></circle>
          <circle class="map__pulse" cx="307" cy="112" r="4" fill="none" stroke="#89B8E1" stroke-width="1"></circle>
          <circle cx="155" cy="282" r="4" fill="#89B8E1"></circle>
          <circle cx="80" cy="239" r="3" fill="rgba(242,245,248,.55)"></circle>
          <text x="316" y="106" font-family="JetBrains Mono, monospace" font-size="11" fill="#F2F5F8">Yekepa</text>
          <text x="120" y="300" font-family="JetBrains Mono, monospace" font-size="11" fill="#F2F5F8" text-anchor="end">Buchanan</text>
          <text x="70" y="234" font-family="JetBrains Mono, monospace" font-size="10" fill="rgba(242,245,248,.55)" text-anchor="end">Monrovia</text>
          <text x="308" y="79" font-family="JetBrains Mono, monospace" font-size="10" fill="#5B9BD5" text-anchor="middle">Nimba 1</text>
          <text x="350" y="164" font-family="JetBrains Mono, monospace" font-size="10" fill="#5B9BD5">Nimba 2</text>
        </svg>
        <figcaption class="map__caption">
          <span>Two contiguous licenses</span>
          <span class="t-lift">243 km to deep water</span>
        </figcaption>
      </figure>"""


def write(name, html):
    path = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  wrote site/{name}  ({len(html):,} bytes)")
