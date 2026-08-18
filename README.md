# usr-website

Static site for U.S. Strategic Resources — nine pages of pure HTML/CSS, no
framework and no build step, authored for page-by-page translation into
PHP/WordPress.

```
usr-website/
├── site/               ← THE DELIVERABLE: 8 pages + one shared style.css + assets
│   ├── news/              example single post page (/news/{slug})
│   └── README.md          handoff notes: launch tokens, SEO map, pending inventory
├── design-reference/   design-system spec and the two originally designed pages
├── content/            the copy and SEO rules (usr-website-content-map.md)
└── tools/              check-site.py (validator) · build-pages.py (generator)
                        element-symbols.py (PubChem element links)
```

`design-reference/` and `content/` are inputs and are not touched by the build.
`site/` is what gets handed over.

## Working on it

Open `site/index.html` in a browser — that's the whole workflow. After edits:

```
python3 tools/check-site.py
```

Validates markup, headings, SEO tags, class coverage, links, ids and JSON-LD
across all nine pages, plus the four responsive markup requirements (mobile
menu present, current page marked in both navs, `data-label` on every table
cell, every checkbox-hack label pointing at a real checkbox). Exits non-zero
on any problem.

`tools/build-pages.py` generated the pages that had no design reference,
lifting the header/footer markup verbatim from the two hand-built pages so the
shared chrome is identical everywhere. `tools/element-symbols.py` wires every
chemical symbol to PubChem from a single verified symbol→name map, and
`build-pages.py` re-runs it automatically. Neither is a build step — the HTML
files are the source of truth from here on.

## Publishing a preview

GitHub Pages: **Settings → Pages**, source branch `main`, folder `/site`.
The site is `noindex` sitewide until USR approves launch, so a public preview
URL is safe to share.

## Read next

`site/README.md` — the two find-and-replace tokens that have to be resolved
before launch, the per-page schema map, the 54 `[pending]` markers that are
blocked on USR, and the design decisions made during the translation.

**Mobile is built.** The responsive system lives in §11 of `site/css/style.css`
(fluid ≤1439px, tablet ≤1023px, mobile ≤767px) and is applied across all nine
pages — audited at 375px and 768px with no horizontal overflow. The design
rationale and the per-page markup checklist are in
`design-reference/USR System - Breakpoint Notes.md`.
