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
- Skip `premium_photo-1661963968707-cf062e54725b.avif` — replaced by the client, same filename/folder,
  1920px square. Confirm before use that the replacement, not the watermarked original, is in place.

## Contact form
- Styled to match Global Frontier Advisors' form conventions, translated to the dark palette.
- Submits to info@usstrategicresources.com.
- Ships as markup only — no working backend in this static build. The form must not silently
  fail-looking-functional; either disable submit with a note, or leave it clearly wired for
  Marcel's PHP layer to complete. Don't fake a success state.
- LinkedIn link: linkedin.com/company/usstrategicresources (unconfirmed whether live — don't remove
  this caveat when you use the link).

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
