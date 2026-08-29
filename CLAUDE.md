# USR website — project constraints

Static HTML/CSS site. A developer (Marcel) converts this to PHP/WordPress by hand.
Everything below exists to keep that conversion clean — don't optimize away from these constraints.

## Source of truth
- `site/` is the only source. There is no `docs/` folder — it was removed; GitHub Pages
  deploys `site/` directly via `.github/workflows/pages.yml` (upload-pages-artifact + deploy-pages).
- There is no page generator. `tools/build-pages.py` was a one-shot scaffolder and has been
  removed from the repo (still in git history if ever needed). `site/*.html` are hand-maintained
  source files, edited directly, one page at a time. Never write or reintroduce a script that
  regenerates page content — it will silently overwrite hand-added content (this happened once
  already: a prior scaffold run wiped real headshot markup and stripped animation classes).
- OPEN QUESTION from the 2026-08-29 rebuild: `tools/build.py` + `tools/shell.py` scaffolded all 8
  pages once from the design file and the deck. They hold the page copy as literals, which the
  "Script rule, clarified" section below disallows as an ongoing mechanism. They are still in the
  working tree, uncommitted, pending a decision: either commit-then-delete them (the precedent set
  by `tools/build-pages.py`), or keep them and relax the rule. Until that is decided, treat
  `site/*.html` as the source of truth and do NOT re-run `build.py` over hand-edited pages.
- `tools/process-images.py` is NOT a page generator and stays — it derives the responsive image
  set from the Drive originals and touches no markup.

## Structure — 7 pages, matching the investor deck's own hierarchy
- `index.html` — Home
- `about.html` — sections `#assets`, `#jurisdiction`, `#differentiation` (merged from the old
  cestos-project.html + why-liberia.html, plus new differentiation content)
- `leadership.html` — was `company.html`
- `metals.html` — was `critical-minerals.html`; sections `#context`, `#battery`, `#tech`
- `news.html` — unchanged, one post is fine
- `contact.html` — unchanged
- `legal.html` — unchanged
Old URLs `cestos-project.html`, `why-liberia.html`, `critical-minerals.html`, `company.html` need
thin redirect stubs (meta-refresh + canonical link) pointing at the new page/anchor.

## Do not remove
- `reveal` / `reveal-group` classes on section blocks — these drive the existing scroll-triggered
  animations. Preserve them on every page you touch; don't refactor them away.

## Photography
- Treatment: grayscale → `#2D4A73` colour-blend → ink gradient overlay, applied in CSS, not baked
  into image files, so it stays tunable.
- Hero image is terrain (exploration-stage), not an operating open-pit mine — deliberate choice,
  don't swap it for a "punchier" mining photo later.
- Leadership headshots exist at `site/assets/team/` (all 6, including Samantha) — reference them
  directly, no placeholder markup.
- Skip `premium_photo-1661963968707-cf062e54725b.jpg` — replaced by the client, same filename/folder,
  1920px square. Confirmed 2026-08-29: the licensed replacement is the one in the folder (checked
  the centre and lower band at full resolution — no Unsplash+ watermark).
- The three-layer treatment must stay three layers: `<img>` filter, then a colour-blend layer,
  then the ink gradient, as separate pseudo-elements. Collapsing the blend and the gradient into
  one pseudo-element breaks it — `mix-blend-mode: color` then blends the gradient, not the photo.
- `<picture>` must be stretched to its box (`position:absolute; inset:0`). It is an inline wrapper,
  so without that the inner `object-fit: cover` has no box to fill and the photo collapses to its
  intrinsic width. This shipped broken once on the about-page band.

## Contact form
- Styled to match Global Frontier Advisors' form conventions, translated to the dark palette.
- Submits to info@usstrategicresources.com.
- Ships as markup only — no working backend in this static build. The form must not silently
  fail-looking-functional; either disable submit with a note, or leave it clearly wired for
  Marcel's PHP layer to complete. Don't fake a success state.
- LinkedIn link: linkedin.com/company/usstrategicresources (unconfirmed whether live — don't remove
  this caveat when you use the link).

## Content authority
- The most recent deck/pptx is the source of truth for any naming or content conflict with older
  site copy (e.g. the deck's "Nimba 1"/"Nimba 2" superseding the older "Nimba 79"/"ADJ" license
  names — same underlying areas, same element profiles, just renamed). When older site content
  conflicts with the current deck, follow the deck without asking first.

## Content decisions already made — do not relitigate
- Metals pages keep the deck's content as-is (Ni/V/Ta are profiled even though they're not in the
  Assets slide's anomaly list; Mn is in the anomaly list but not profiled). This is intentional
  pending a future client decision. Do not add a disclaimer or reconcile the lists unilaterally.
- "RARE EARTHS" opens the closing tagline — confirmed correct, keep as-is.
- No `PRIVATE & CONFIDENTIAL` marking anywhere (that's the internal deck's footer, not for the
  public site). The exploration-stage / no-resource-defined disclaimer IS required and must stay
  clearly legible — see contrast rule below.

## Non-negotiable build rules
- No frameworks, no build step, no npm dependencies. Plain HTML/CSS/vanilla JS only.
- One shared stylesheet (`site/css/style.css`). Never per-page CSS, never inline `<style>`.
- Semantic HTML5 (`header`, `nav`, `main`, `section`, `article`, `footer`). One `<h1>` per page.
- Header and footer byte-identical across all 7 pages. Active nav state = a class on `<body>`,
  never edited nav markup per page.
- Repeating blocks (leadership card, element card, news card, teaser card) use one consistent
  class structure each — each maps to a single future PHP template part.
- Relative paths only.
- All text content lives in the HTML, never injected by JS.
- Every colour value comes from a CSS custom property. No hard-coded hex outside the token block.

## Accessibility floor
- Every text/background pair actually used must reach 4.5:1 (3:1 for 24px+/19px+ bold), with one
  approved exception below.
- Approved exception: the low-opacity dark-ground caption/label text (`rgba(242,245,248, .42)` and
  similar) is accepted at ~3.8:1 — client-approved trade-off for a refined, quiet type hierarchy.
  Do not "fix" this by silently raising opacity across the board; it was a deliberate call.
  Brand blues (#5B9BD5, #89B8E1) are never used as small text color on the paper/light ground —
  confirmed too low contrast (2.71:1 / ~2:1). On light grounds, emphasis text uses --ink or --grey.
- Visible keyboard focus on every interactive element. Skip-to-content link. `prefers-reduced-motion`
  disables all transitions and the map's rail-line draw animation.

## Motion
- One orchestrated signature moment on the Home hero: the Liberia map's rail corridor draws in
  once, plus a pulsing node animation at the Yekepa endpoint. That's the showcase animation — don't
  add competing scroll effects elsewhere without a specific reason.
- A small number of additional micro-interactions may be proposed per page (e.g. metals-card hover,
  element-card reveal stagger) using the same restrained logic as the map — subtle, purposeful, tied
  to something the user is already doing (hover, scroll into view). Not decoration for its own sake.

## Script rule, clarified
"Never write a script that regenerates page content" means: never write a script whose output is
hardcoded/invented markup standing in for real content. Permitted: a script that reads existing
real markup and moves, merges, or replaces it mechanically — content always comes from what's
already in the files, never from a literal in the script. Required when using this kind of
script: verify afterward that nothing was silently dropped (reveal-hook counts, real asset
references, prior content still present) and report the verification. If in doubt, ask before
running, not after.

## Filing CSS — deleted, do not resurrect (2026-08-29 rebuild)
The incremental migration failed: old structure survived with new colours bolted on. `style.css`
was deleted and rewritten wholesale from `USR Rebrand - Four Screens.dc.html`. There is no
`--forest`, `--mono`, `--gold`, `.band-dark`, or Filing-era `.section` rule left. `.section` now
means the design's own section primitive (ink / alt / panel / paper grounds), not the old one.
If a page needs something the four screens don't define, extrapolate from the design's vocabulary
— never reach back into the Filing stylesheet or the `design-reference/` archive for it.

## Nav active state — aria-current only
`aria-current="page"` on the current page's nav link is the whole mechanism: it is the
accessibility signal and it drives the visual active state via `.nav a[aria-current="page"]`.
The earlier `<body>` nav-state class is gone — it was a second source of truth for the same fact.
Don't reintroduce it.

## Documented exception — nested news post
`site/news/{slug}.html` sits one directory below the other 7 pages. Header/footer markup is
identical in structure and content; only relative path depth differs (`../css/style.css` instead
of `css/style.css`). This is a sanctioned exception to "byte-identical." Don't invent a second
exception shape for future posts — they follow this same pattern.

## Documented exception — aria-current
Header/footer are byte-identical except the current page's nav link carries
`aria-current="page"`. Body class drives visual active state; `aria-current` is the accessibility
signal and is never dropped or JS-generated. Second sanctioned exception to "byte-identical."

## Verification backlog

- ~~`about.html` at 375px unconfirmed for horizontal overflow~~ — **RESOLVED 2026-08-29.**
  The headless-Chrome quirk is real and now diagnosed: on this macOS setup `--window-size=375,N`
  is silently clamped to a 500px viewport, so the screenshot shows content "clipped" that is in
  fact laid out at 500px and cropped to 375. Measuring `window.innerWidth` inside the page proves
  it (`VIEWPORT=500` for a requested 375).
  Working technique: load each page in a same-origin `<iframe>` of the exact target width and read
  `documentElement.scrollWidth` vs `clientWidth` from the parent. An iframe gets a true viewport
  regardless of the window clamp. All 8 pages measured clean at 375 / 414 / 768 / 1024 —
  `scroll == client` everywhere, no overflowing element. Don't re-litigate this with screenshots;
  use the iframe probe.

## Contrast — one deviation from the design file, on purpose
The design sets tertiary micro-labels on light grounds (`.unit__rank`, `.element__note`, paper
`.figcap`) in `#8A94A6`, which measures 3.06:1 on white — below the 4.5:1 floor for 10-12px type.
`--muted` is therefore pointed at the locked `--grey` `#626E82` (4.71-5.16:1 across paper / tint /
card) rather than adding a ninth value to the palette. Everything else in the built site measures
at or above its floor; the ramp was checked pair-by-pair, not by eye.

- ~~`--gold` (the `.label` eyebrow color) measures 2.45:1 on the `--paper` background~~ —
  **RESOLVED**. `--gold`/`--gold-hover` removed entirely (not patched): every reference swapped to
  `--blue-300` on dark grounds or `--ink`/`--grey` on light, in one coordinated commit across all
  ~50 usages (buttons, hovers, focus rings, current-state indicators, the CTA band background).
  Confirmed via `grep -rn "\-\-gold" site/` returning zero references before commit. Two second-
  order breaks caught in the same pass: the sitewide `:focus-visible` ring (now `--ink`) needed a
  dark-context override to stay visible against navy/`.band-dark`, and `.table__data`'s default
  needed `--grey` rather than `--ink` to stay distinct from its own `.table__data--ink` modifier.
  RUN 9 should spot-check a couple of pages to confirm — nothing left to discover here, just verify.
