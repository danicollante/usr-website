#!/usr/bin/env python3
"""Apply the element-symbol component to every chemical symbol on the site.

One symbol -> name map drives everything: the desktop tooltip (`data-element`),
the PubChem href, the accessible name, and the touch popover. Every URL in the
map was verified live (HTTP 200 + the served page title identifying the
element) before wiring.

Two passes per page:

  1. Wrap bare " · "-separated element lists in <a class="element-symbol">.
     Only known symbols inside known containers are touched, and a cell is
     rewritten only if EVERY token in it is a known symbol — so data cells like
     "Q4 2026", "3 months", "150-330 kt" or "$12B" are left alone.
     `.facts__term` is skipped on purpose: CSS uppercases it, which would
     render "Ga" as "GA", not a chemical symbol.

  2. Upgrade each anchor into the full touch unit — checkbox + tap overlay +
     popover — with ids unique per page. On a pointer device the overlay and
     popover are display:none and behaviour is exactly as before.

Idempotent per file: a page that already contains `element__state` is skipped,
so re-running after tools/build-pages.py cannot double-wrap.
"""
import glob, os, re

ELEMENTS = {
    'Nd': 'Neodymium',  'Sm': 'Samarium',   'La': 'Lanthanum',  'Pr': 'Praseodymium',
    'Eu': 'Europium',   'Li': 'Lithium',    'Co': 'Cobalt',     'Ni': 'Nickel',
    'Mn': 'Manganese',  'Cs': 'Cesium',     'Cu': 'Copper',     'Zn': 'Zinc',
    'Pb': 'Lead',       'Ag': 'Silver',     'Ga': 'Gallium',    'Ge': 'Germanium',
    'Te': 'Tellurium',  'In': 'Indium',     'Zr': 'Zirconium',  'Nb': 'Niobium',
    'Ta': 'Tantalum',   'Ti': 'Titanium',   'V':  'Vanadium',   'Be': 'Beryllium',
    'Bi': 'Bismuth',    'Au': 'Gold',       'Sn': 'Tin',
}
BASE = 'https://pubchem.ncbi.nlm.nih.gov/element/'
SEP = ' &middot; '


def anchor(sym):
    """Pass 1 output: the plain link, which is all a pointer device needs."""
    name = ELEMENTS[sym]
    return (f'<a class="element-symbol" data-element="{name}" href="{BASE}{name}" '
            f'target="_blank" rel="noopener">{sym}'
            f'<span class="visually-hidden">{name}</span></a>')


def unit(sym, ident):
    """Pass 2 output: the anchor plus its touch popover.

    Two elements added, not four. .element__tap does double duty: closed, it
    is the small hit area over the bare symbol; once its checkbox is
    :checked, CSS restyles that SAME element into the full-viewport dimming
    backdrop — a <label for> toggles its checkbox the same way regardless of
    the label's size, so "tap outside closes" needs no second element.
    .element__link is the only other one: it IS the popover card (its own
    padding/border/background do that job), and its displayed name comes from
    its own data-element via CSS ::before (see style.css), the same
    attr()-driven approach used for the desktop tooltip, rather than a
    written-out second element.
    """
    name = ELEMENTS[sym]
    return (
        f'<span class="element">'
        f'<input class="element__state visually-hidden" id="{ident}" type="checkbox">'
        f'{anchor(sym)}'
        f'<label class="element__tap" for="{ident}" aria-label="Toggle element name"></label>'
        f'<a class="element__link" data-element="{name}" href="{BASE}{name}" target="_blank" rel="noopener">View on PubChem &rarr;</a>'
        f'</span>'
    )


# --- pass 1: bare element lists -> anchors ---------------------------------

TARGETS = [
    r'(?P<open><td class="[^"]*table__data[^"]*"[^>]*>)(?P<inner>[^<]+)(?P<close></td>)',
    r'(?P<open><div class="elements[^"]*">)(?P<inner>[^<]+)(?P<close></div>)',
    r'(?P<open><li class="chip">)(?P<inner>[^<]+)(?P<close></li>)',
]


def link_lists(s):
    n = 0

    def repl(m):
        nonlocal n
        inner = m.group('inner')
        tokens = [t.strip() for t in inner.split('&middot;')]
        if not tokens or not all(t in ELEMENTS for t in tokens):
            return m.group(0)
        n += len(tokens)
        return m.group('open') + SEP.join(anchor(t) for t in tokens) + m.group('close')

    for pat in TARGETS:
        s = re.sub(pat, repl, s)

    # stat caption naming two symbols in running text
    old = '<div class="stats__label">refined Ga and Ge</div>'
    if old in s:
        s = s.replace(old, f'<div class="stats__label">refined {anchor("Ga")} and {anchor("Ge")}</div>')
        n += 2
    return s, n


# --- pass 2: anchors -> touch units ----------------------------------------

ANCHOR_RE = re.compile(
    r'<a class="element-symbol" data-element="(?P<name>[^"]+)" href="[^"]+" '
    r'target="_blank" rel="noopener">(?P<sym>[A-Za-z]{1,2})'
    r'<span class="visually-hidden">[^<]*</span></a>')


def add_popovers(s, slug):
    counter = [0]

    def repl(m):
        counter[0] += 1
        return unit(m.group('sym'), f'es-{slug}-{counter[0]}')

    return ANCHOR_RE.sub(repl, s), counter[0]


total_links = 0
total_units = 0

for f in sorted(glob.glob('site/*.html') + glob.glob('site/news/*.html')):
    s = open(f, encoding='utf-8').read()
    if 'element__state' in s:
        continue                      # already migrated
    before = s
    s, linked = link_lists(s)
    slug = os.path.splitext(os.path.basename(f))[0]
    s, wrapped = add_popovers(s, slug)
    if s != before:
        open(f, 'w', encoding='utf-8').write(s)
        print(f'  {f}: {wrapped} symbols ({linked} newly linked)')
    total_links += linked
    total_units += wrapped

print(f'\n{total_units} element symbols carry the tooltip + touch popover '
      f'({total_links} newly linked this run)')
