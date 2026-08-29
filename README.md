# usr-website

Static site for U.S. Strategic Resources — plain HTML/CSS/vanilla JS, no
framework and no build step, authored for page-by-page translation into
PHP/WordPress.

```
usr-website/
├── site/               ← THE DELIVERABLE
│   ├── *.html             7 pages + 4 redirect stubs at the retired URLs
│   ├── news/{slug}.html   single post page
│   ├── css/style.css      the one stylesheet
│   ├── js/interactions.js scroll reveals + mobile nav
│   └── assets/            img/ (responsive sets) · team/ · logo/ · maps/
├── design-reference/   the retired "Filing" system — archive only, do not reuse
├── content/            copy and SEO notes
└── tools/              check-site.py · process-images.py
```

`design-reference/` and `content/` are inputs. `site/` is what gets handed over.

## The design is the template

`site/css/style.css` is extracted wholesale from
`resources/feedback 0828/claude design run/USR Rebrand - Four Screens.dc.html`
— tokens, type scale, spacing rhythm, section grounds, photo treatment, card
patterns. The earlier "Filing" stylesheet was deleted, not migrated. Anything
the four screens don't define is extrapolated from the design's own vocabulary.

Content is the investor deck (`US-Strategic-Resources-Website Copy.pptx`),
verbatim. Where the deck and older site copy conflict, the deck wins.

## Working on it

```
cd site && python3 -m http.server 8000
```

Then, with the server running:

```
python3 tools/check-site.py      # every page, asset and internal link resolves
```

`site/*.html` are hand-maintained — edit them directly. There is deliberately
no page generator in the tree; see CLAUDE.md for why.

## Regenerating the image set

`tools/process-images.py` derives the responsive WebP + JPEG sets in
`site/assets/img/` from the originals in the Drive photo folder. It touches no
markup. Re-run it only if the source photos change:

```
python3 tools/process-images.py
```

Widths are 1920/1280/800/480, never upscaled past the source. It writes a
`manifest.json` alongside the images recording each slug's available widths and
native dimensions.

## Known gaps

- The news post is a real page with placeholder body copy. Every unresolved
  span is marked `<span class="pending">` and is visible on the page — nothing
  is silently faked.
- The contact form is markup only. It has no backend; it opens the visitor's
  mail client addressed to info@usstrategicresources.com. There is no fake
  success state. Wiring it up is part of the PHP conversion.
