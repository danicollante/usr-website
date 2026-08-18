# USR Website — Design → Code Handoff Notes

Plain-text supplement to `USR System — Filing.dc.html`. Read the spec sheet first; this covers decisions made in session that aren't captured there.

## Figures
- Real geology/prospectivity maps replace all placeholders as of this session. Filenames (in `/assets/`, keep as-is):
  - `06-nimba-79-adj-licence-map-regional-geology.webp` — licence boundaries over regional geology. Used on Home ("The asset") and Cestos Project (hero/licence section, Fig. 1).
  - `07-nimba-79-gold-prospectivity.webp` + `07-nimba-79-cobalt-prospectivity.webp` — Nimba 79 two-up pair (Cestos Project, Fig. 2).
  - `08-adj-licence-six-metal-anomaly.webp` — ADJ six-metal grid, one composed figure, don't split (Cestos Project, Fig. 3).
- **Two-up pairing convention**: when two related single-metal prospectivity maps cover the same licence, place them side by side inside one `<figure>` (a 2-col grid, 12px gap) under ONE shared caption — same visual unit as the six-metal grid, just 2 panels instead of 6. Established with the Nimba 79 gold+cobalt pair; reuse this pattern anywhere else two related maps need pairing (e.g. if a third Nimba 79 layer or an ADJ two-metal comparison comes later).
- Field photography (terrain band, headshots) is still placeholder — flagged inline in both pages, not yet supplied.

## `[pending]` convention
`[pending: ...]` is a typographic placeholder state, not blank space — IBM Plex Mono, 11px, `#6B6B64`, used inline wherever a fact is known to be missing (methodology notes, headquarters address, email). Never leave a table cell or line empty; use `[pending: what's missing]` so the gap reads as deliberate, not broken. Style it as a real component/utility class in code so it's easy to grep for and replace as real data lands.

## Table variants (confirmed against Cestos, the densest page)
- **Narrow key-value** — 2-column, label left (mono, uppercase, muted) / value right, used for stat blocks (hero facts).
- **Full-width comparison** — 3+ columns, Spectral serif for lead column, mono for codes/values, used for commodity tables and roadmap.
- **Stub-column comparison** — a narrow first column (mono label) plus full-bleed columns after, used when rows compare licence-level facts (jurisdiction, structure, survey).
- **Multi-column (4-col) table style** — used for the roadmap; same border/type rules as the full-width comparison, just more columns.

## Nav
Flat, 6 items, no dropdowns: Company, Cestos Project, Why Liberia, Critical Minerals & Strategy, News, Contact. "Home" is not a nav item — the logo (header + footer) links to `/` with an `aria-label`, matching the zodiac-gold.com pattern. Confirmed and built as of the round 2 pass (sticky nav, element-symbol component, News).

## Page shell
Fixed `width:1440px; margin:0 auto` container (not fluid) — matches how both built pages are authored. No responsive/mobile breakpoints were designed this session; if the WordPress build needs mobile, that's new design work, not a translation of existing intent — none of the fixed-width 1440px layout should be assumed to reflow.

## FAQ
Accordion pattern (collapsed by default, one open at a time is a reasonable default — not tested against a "many open at once" case). Cestos Project's FAQ has a `faqMode` tweak (accordion vs. flat) — accordion is the version to build from.

## Known gaps at handoff
- Headquarters address and email are `[pending]` in the footer on both pages.
- Headshots (3, Home leadership section) and hero terrain photography are unshot/unsupplied — currently a diagonal-stripe placeholder block.
- ~~6 of 7 nav pages... not yet designed~~ — superseded: all 9 pages (8 site pages + 1 news post) now exist as of the round 2 Claude Code pass, validated with 0 issues. This note is kept for history only.
- Mobile (375px/768px) remains undesigned — explicitly out of scope for the round 2 build, to be resolved in Claude Design against the current final Home + Cestos Project HTML before returning to Claude Code.
- Label token: eyebrow and the 01–07 index rail now share one size token, confirmed at 13px (updated from the original 11px/12px mismatch).
