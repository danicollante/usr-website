#!/usr/bin/env python3
"""Sanity checks for the static site in site/.

  - tag balance / parse errors
  - exactly one <h1>, heading order, title + meta description present
  - every class used in HTML exists in css/style.css
  - every local href/src resolves on disk
  - JSON-LD blocks parse as JSON (after stripping the {{SITE_URL}} token)
  - no inline style attributes (single shared stylesheet)
"""
import json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
ROOT = os.path.normpath(ROOT)
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

css = open(os.path.join(ROOT, 'css', 'style.css'), encoding='utf-8').read()
defined = set(re.findall(r'\.([A-Za-z][\w-]*)', re.sub(r'/\*.*?\*/', '', css, flags=re.S)))

class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []
        self.classes, self.links, self.headings = set(), [], []
        self.ids = []
        self.inline_styles = 0
        self.in_ld = False
        self.ld_blocks, self.buf = [], ''
        self.title = ''
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if 'class' in a:
            self.classes.update(a['class'].split())
        if 'style' in a:
            self.inline_styles += 1
        for k in ('href', 'src'):
            if k in a:
                self.links.append(a[k])
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_ld, self.buf = True, ''
        if tag == 'title':
            self.in_title = True
        if re.fullmatch(r'h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_ld:
            self.ld_blocks.append(self.buf)
            self.in_ld = False
        if tag == 'title':
            self.in_title = False
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'stray </{tag}> at line {self.getpos()[0]}')
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f'</{tag}> at line {self.getpos()[0]} closes <{open_tag}> opened at line {pos[0]}')

    def handle_data(self, data):
        if self.in_ld:
            self.buf += data
        if self.in_title:
            self.title += data

fails = 0
pages = []
for dirpath, _dirs, files in os.walk(ROOT):
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
pages.sort()

for name in pages:
    path = os.path.join(ROOT, name)
    src = open(path, encoding='utf-8').read()
    p = Check(); p.feed(src); p.close()
    problems = list(p.errors)

    if p.stack:
        problems += [f'unclosed <{t}> opened at line {pos[0]}' for t, pos in p.stack]

    h1s = [h for h in p.headings if h == 1]
    if len(h1s) != 1:
        problems.append(f'expected exactly one <h1>, found {len(h1s)}')
    if not p.title:
        problems.append('missing <title>')
    if 'name="description"' not in src:
        problems.append('missing meta description')
    if 'name="robots"' not in src:
        problems.append('missing robots meta (site is noindex until launch)')
    if p.inline_styles:
        problems.append(f'{p.inline_styles} inline style attribute(s) — must live in style.css')

    # --- mobile / responsive markup requirements (see §11 of style.css) ---
    if '<details class="nav-mobile">' not in src:
        problems.append('missing <details class="nav-mobile"> — no menu below 1023px')
    if 'site-header__cta' not in src:
        problems.append('header CTA missing the site-header__cta class (it must hide at <=1023px)')

    # the current page must be marked in BOTH navs, not just the desktop bar
    nav_current = re.search(r'nav__link--current" href="([^"]+)"', src)
    if nav_current:
        target = nav_current.group(1)
        menu = re.search(r'<nav class="nav-mobile__list".*?</nav>', src, re.S)
        if menu and f'href="{target}" aria-current="page"' not in menu.group(0):
            problems.append(f'"{target}" is current in the desktop nav but not in the mobile menu')

    # every <td> that becomes a card row on mobile needs its column label back
    for body in re.findall(r'<tbody>.*?</tbody>', src, re.S):
        for cell in re.findall(r'<td\b[^>]*>', body):
            if 'data-label=' not in cell:
                problems.append(f'table cell without data-label (unlabelled on mobile): {cell[:70]}')

    # checkbox-hack units: every state id must be unique and every label must
    # point at a state that exists
    states = re.findall(r'class="(?:lightbox|element)__state[^"]*" id="([^"]+)"', src)
    fors = set(re.findall(r'<label[^>]*\sfor="((?:lb|es)-[^"]+)"', src))
    for ident in sorted(fors - set(states)):
        problems.append(f'<label for="{ident}"> points at a checkbox that does not exist')
    for ident in sorted(set(states)):
        if ident not in fors:
            problems.append(f'checkbox "{ident}" has no <label for> to toggle it')

    dupes = {i for i in p.ids if p.ids.count(i) > 1}
    for d in sorted(dupes):
        problems.append(f'duplicate id "{d}"')

    for cls in sorted(p.classes):
        if cls not in defined:
            problems.append(f'class "{cls}" used but not defined in style.css')

    for link in p.links:
        if link.startswith(('http://', 'https://', '#', 'mailto:', 'tel:', 'data:', '{{')):
            continue
        target = link.split('#')[0].split('?')[0]
        base = os.path.dirname(path)
        if target and not os.path.exists(os.path.normpath(os.path.join(base, target))):
            problems.append(f'broken local link: {link}')

    for i, block in enumerate(p.ld_blocks, 1):
        ents = re.findall(r'&(amp|mdash|ndash|middot|rsquo|times|copy|rarr|sect);', block)
        if ents:
            problems.append(f'JSON-LD block {i} contains HTML entities ({", ".join(sorted(set(ents)))}) '
                            '— entities are not decoded inside <script>, use literal characters')
        try:
            json.loads(block.replace('{{SITE_URL}}', 'https://example.com'))
        except Exception as e:
            problems.append(f'JSON-LD block {i} does not parse: {e}')
    if not p.ld_blocks:
        problems.append('no JSON-LD schema block')

    status = 'OK  ' if not problems else 'FAIL'
    if problems:
        fails += 1
    print(f'{status} {name}  ({len(p.ld_blocks)} schema block(s))')
    for pr in problems:
        print(f'       - {pr}')

print(f'\n{len(pages)} page(s) checked, {fails} with problems')
sys.exit(1 if fails else 0)
