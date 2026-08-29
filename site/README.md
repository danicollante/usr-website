# USR website — static build (`site/`)

Nine hand-authored HTML pages (eight top-level plus one example news post)
and one shared stylesheet. No framework, no
build step, no JavaScript. Open any `.html` file directly in a browser and it
works. This folder is the deliverable for the WordPress/PHP translation.

```
site/
├── css/style.css          ← the whole design system, ~1,100 lines, commented by section
├── index.html             Home
├── company.html           Company
├── cestos-project.html    Cestos Project
├── why-liberia.html       Why Liberia
├── critical-minerals.html Critical Minerals & Strategy
├── news.html              News
├── contact.html           Contact
├── legal.html             Legal & Disclaimer
├── news/
│   └── company-formation-announcement.html   example single post
└── assets/
    ├── maps/              4 final-resolution geology/prospectivity maps (.webp)
    ├── logo/              usr-logo-black.png, usr-logo-white.png
    └── favicon.png
```

---

## Before this goes live — two find-and-replace tokens

Both are deliberate placeholders, not URLs. Search every `.html` file:

| Token | Replace with | Appears in |
|---|---|---|
| `{{SITE_URL}}` | production origin, no trailing slash (e.g. `https://usstrategicresources.com`) | `<link rel="canonical">`, `og:url`, all JSON-LD blocks |
| `{{FORM_ENDPOINT}}` | Formspree / Netlify Forms endpoint | `<form action>` on Contact (enquiry + newsletter) and News (newsletter) |

Then remove `<meta name="robots" content="noindex, nofollow">` from every page
**except** `legal.html`, which stays `noindex` by design. The site is noindex
sitewide until USR approves launch (content map §2.5).

---

## The CSS system

Everything lives in `css/style.css`, organised in ten commented sections:
tokens → reset → page shell & sections → typography → buttons & links →
tables → figures → components → header/footer → utilities.

All colour, type, and spacing values are CSS custom properties on `:root`.
Change `--blue-300` once and every accent link, rule and button follows.

**Layout primitives**

- `.page` — the fixed 1440px page container.
- `.section` — full-width section, 88px vertical / 72px horizontal (used on Home).
- `.section-indexed` — the numbered-rail section used on every inner page:
  a 120px mono index rail plus content. Add `.band-dark` for an inverted band,
  `.section-indexed--last` to drop the bottom rule when no CTA band follows.
- `.grid-2`, `.grid-3`, `.grid-hero`, `.grid-2-wide`, `.grid-aside` — the five
  column splits the design uses. Nothing else.

**Components** — `.facts`, `.takeaways`, `.table`, `.figure`, `.faq`,
`.stats`, `.chips`, `.person`, `.news`, `.form`, `.cta-band`, `.placeholder`.
Each is commented in the stylesheet with the rule it implements.

**No JavaScript.** The FAQ accordion is `<details name="faq">` — native HTML.
`name` keeps one row open at a time where supported and degrades to
independent toggles elsewhere. Closed row shows a gold plus, open row a gold
minus, per the design spec. If WordPress needs a different accordion, the
markup is `.faq > details.faq__item > summary.faq__summary + .faq__answer`.

**Element symbols.** Every chemical symbol in a table or in body copy is one
component: `.element-symbol`. A `data-element` attribute carries the full
element name — it renders the tooltip via `attr()` and is the same value that
builds the PubChem href. 76 symbols are wired across Home, Cestos Project and
Critical Minerals.

```html
<a class="element-symbol" data-element="Neodymium"
   href="https://pubchem.ncbi.nlm.nih.gov/element/Neodymium"
   target="_blank" rel="noopener">Nd<span class="visually-hidden">Neodymium</span></a>
```

The hidden span makes the accessible name "Nd Neodymium" instead of two
letters. In WordPress, generate the href, the tooltip and the hidden name from
one symbol→name map (the 27-entry map lives in `tools/element-symbols.py`) —
don't hand-write instances. All 27 PubChem URLs were verified live (HTTP 200
plus a title match) before wiring; the slug is the standard English name, so
`Cesium`, not `Caesium`.

**On touch there is no hover**, so each anchor is wrapped in a popover unit —
same checkbox-hack family as the FAQ, the mobile menu and the lightbox. Just
two elements are added, kept deliberately flat (no wrapping card/popover
element): a checkbox, and a transparent `<label class="element__tap">` over
the symbol. Closed, that label is a small hit area that takes the tap instead
of the link, so the first tap opens the popover rather than navigating. Once
its checkbox is `:checked`, the *same* label is restyled by CSS into the
full-viewport dimming backdrop — a `<label for>` toggles its checkbox the
same way regardless of the label's own size, so "tap outside closes" costs no
second element. The only other addition is `.element__link`: it IS the
popover card (its own padding/border/background do that job, no wrapper
spent just to hold a box), and the name it displays is generated from its own
`data-element` via CSS `::before` — the same `attr()` approach already used
for the desktop tooltip — rather than written out as a separate element. Only
the real "View on PubChem →" text is light-DOM content, since generated
content isn't reliably read as part of an accessible name.

The overlay and popover are `display: none` on pointer devices — mouse and
keyboard behaviour is untouched, and since the overlay only intercepts
*pointer* events, Enter on the focused link still navigates on any device.
Ids are `es-{page}-{n}`, unique per page. Per instance this is 540 bytes
(186 for the bare anchor + 354 for the popover), down from an initial
753-byte four-element version — cut by cutting elements, not by shortening
class names or trimming security/accessibility attributes, both of which stay
exactly as they were.

Two deliberate exclusions: cells whose contents are not all element symbols
are left alone (`Q4 2026`, `3 months`, `150–330 kt`, `$12B`), and
`.facts__term` is skipped because CSS uppercases it — "Ga" would render "GA",
which is not a chemical symbol.

**Sticky header.** `.site-header` is `position: sticky; top: 0` with
`z-index: var(--z-header)` and an explicit `background: var(--paper)` — a
sticky bar is transparent by default and the dark bands would otherwise scroll
straight through it. The layer scale is in the tokens: tooltip 20, header 50,
skip link 100.

**Eyebrow size** is the `--label-size` token, now 13px (up from the original
11px). `.label` and `.section-indexed__rail` — the section eyebrows and the
01-07 mono section numbers — both read from this one token, so they stay
locked at the same size. Change it once and both follow.

**Navigation is six items**, not seven: Company · Cestos Project · Why Liberia ·
Critical Minerals & Strategy · News · Contact. "Home" was dropped; the logo is
the home link and carries `aria-label="U.S. Strategic Resources — home"`. This
differs from the seven-item nav in the design handoff notes and content map.

**Newsroom.** The listing (`news.html`) is category tabs + post cards +
numbered pagination. Cards carry category, date, source, title and a one-line
excerpt. Each announcement is its **own indexable page** at `/news/{slug}` —
never a modal or an accordion — because the content map requires per-post
indexing and `NewsArticle` schema.
`news/company-formation-announcement.html` is the working example and confirms
the system holds at article level. Two things it changed:

- article headlines use `.h1--article` (56px, the existing statement step)
  rather than the 88px page H1, which is too heavy for a headline;
- the index rail on an article is left empty — it holds the 120px alignment,
  but a lone "01" would imply sections that never come.

Only one real announcement exists, so that is all the listing shows. No filler
cards were invented: the category tabs render inactive because no category
archive exists as a flat file, and pagination shows the one real page.

**Responsive.** The desktop page is a fixed 1440px; everything below that is
in **§11 of `style.css`**, additive — §01–§10 are the untouched desktop
design. Reflow is driven first by re-declaring the §01 tokens per breakpoint
(`--page-inset`, `--section-pad`, `--rail`, the gaps), so any new component
that uses them inherits the behaviour with no new rules.

| State | Width | What changes |
|---|---|---|
| Desktop | ≥1440px | the designed page, fixed width |
| Fluid | ≤1439px | same layout, 100% width, tighter insets |
| Tablet | ≤1023px | nav → menu; index rail collapses; media pairs stack |
| Mobile | ≤767px | everything single-column; tables become stacked cards |

Four things are markup, not CSS, and every page carries them:
`<details class="nav-mobile">` in the header, `site-header__cta` on the
desktop CTA, `data-label` on every `<td>` (it supplies the column heading
once the table becomes cards), and `.grid-2--media` on any two-column block
pairing a figure with text. Figures are wrapped in the zoomable/lightbox unit
so dense maps can be enlarged. Full detail:
`design-reference/USR System - Breakpoint Notes.md`.

Audited at 375px and 768px across all nine pages: no horizontal overflow, menu
active, every table cell labelled. `tools/check-site.py` enforces all four
markup requirements.

---

## SEO applied per page

Every page carries: one `<h1>`, a unique `<title>` and meta description from
the content map, canonical, Open Graph + Twitter card, favicon, and JSON-LD.

| Page | Schema blocks |
|---|---|
| Home | Organization |
| Company | Organization, BreadcrumbList, Person ×5 (`@graph`) |
| Cestos Project | Organization, BreadcrumbList, FAQPage |
| Why Liberia | Organization, BreadcrumbList |
| Critical Minerals | Organization, BreadcrumbList, FAQPage |
| News | Organization, BreadcrumbList, CollectionPage |
| Contact | Organization, BreadcrumbList, ContactPage |
| Legal | Organization, BreadcrumbList |
| News post | Organization, BreadcrumbList (3 levels), NewsArticle |

Notes for the WordPress templates:

- Organization is sitewide — move it to the layout/header template and drop
  the per-page copies. Everything else is per-template.
- **HTML entities do not decode inside `<script>`.** JSON-LD uses literal
  characters (`&`, `—`). Don't run schema strings through `esc_html()`.
- `news.html` carries template notes in an HTML comment: post slugs are
  `/news/{slug}` with no dates or numbers, category tabs become
  `/news/category/{slug}` links, and paginated archives (`/news/page/2` and
  beyond) must be `noindex`.
- The example post's `NewsArticle` has **no `datePublished`/`dateModified`** —
  the date is still `[pending]` and a fabricated one would be published as
  machine-readable fact. Add both at the same time as the on-page date.
- Share links are plain `<a>` (LinkedIn, email) built from `{{SITE_URL}}` — no
  third-party scripts or embeds.
- Cestos Project's FAQPage deliberately omits "Who holds the licences?" —
  its answer is still `[pending]` and must match licence documentation before
  it is published as a machine-readable answer. Add it to both the page and
  the schema at the same time.

---

## The `[pending]` convention

`[pending: …]` is a visible placeholder state, never blank space — muted grey,
and mono at 11px for standalone notes. It is styled by the `.pending` and
`.pending--note` classes so it is greppable:

```
grep -rn "pending" site/*.html
```

54 markers across the nine pages. They are the launch blockers:

| What's missing | Where |
|---|---|
| Incorporation jurisdiction + date, HQ city | Company, footer (all pages) |
| Contact email, phone, HQ address | Contact, footer (all pages) |
| Licence numbers / grant / expiry, combined km² | Cestos Project |
| Prospectivity model methodology, data source & year | Cestos Project |
| Tenure structure ("who holds the licences") | Cestos Project FAQ |
| Two paragraphs each for "The problem" and "The moment" | Critical Minerals |
| One sentence each for explore / prove / partner / deliver (deck slide 11) | Critical Minerals |
| Community programs, environmental commitments, employment figures | Why Liberia |
| Announcement date + full announcement text | News, news post |
| Terms of use, privacy/cookie note, counsel review | Legal |
| Field photography (terrain, Monrovia base, sampling) + 5 headshots | Home, Why Liberia, Company |

**No stand-in imagery is used anywhere.** Every unshot photo renders as a
hatched `.placeholder` block carrying the expected filename from the content
map's naming convention, so swapping in the real `.webp` is a one-line change.

---

## Decisions worth knowing about

1. **Assets live inside `site/`.** The repo checklist put `assets/` at the
   repo root, but relative paths have to resolve when GitHub Pages serves
   `/site` as the root, and `site/` has to be handed over self-contained.
2. **The dark band on Cestos Project was realigned.** In the design reference
   the "03 Geology" band's content started 72px further right than every other
   indexed section. All sections now align on the 120px rail.
3. **Copy that the content map specified as direction rather than text**
   (Critical Minerals §3.5's "two paragraphs", the four business-model
   sentences) is rendered as `[pending]`, not written. Content map §6: every
   claim traceable to the deck or a `[PENDING]` flag, no invented facts on a
   securities-adjacent site. The traceable numbers around those gaps *are*
   rendered — the stat rows carry the argument until the prose lands.
4. **Leadership vs. Board.** Home teases three people (Kol, Granata,
   Richards); Company splits Leadership (Kol, Granata, McWatt, plus the open
   Head of Exploration role) from Board of Directors (Richards, Bellon),
   per content map §3.2.
5. **Sticky mobile CTA** (content map §2.3) is not built — it needs the mobile
   layout that hasn't been designed yet.

---

## Checking your work

`tools/check-site.py` (repo root, needs only Python 3) validates all eight
pages: tag balance, exactly one `<h1>`, title/description/robots present,
every CSS class used is defined in `style.css`, no inline `style` attributes,
no broken local links, no duplicate ids, and every JSON-LD block parsing as
valid JSON with no HTML entities.

```
python3 tools/check-site.py
```

Run it after edits. It exits non-zero on any problem.

If you regenerate pages with `tools/build-pages.py`, it re-runs
`tools/element-symbols.py` automatically — regenerating a page would otherwise
wipe the element links written into it.
