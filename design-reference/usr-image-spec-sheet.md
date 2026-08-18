# USR Website — Image Specification Sheet

Consolidated reference for every image slot across the 9 pages (8 site pages + 1 news post). Use this when briefing USR for real photography, when exporting final assets, and when writing `<img>` markup in code. Naming convention: `{subject}-{context}.webp`, all lowercase, hyphens, no spaces.

---

## 1. Real assets — already sourced, in production

| Filename | Used on | Dimensions (source) | Alt text |
|---|---|---|---|
| `06-nimba-79-adj-licence-map-regional-geology.webp` | Home ("The asset"), Cestos Project (Fig. 1) | ~2550×1560px (4:2.4 landscape) | "Map of the Nimba 79 Resources and ADJ Exploration licence areas on the Cestos shear zone, Nimba County, Liberia" |
| `07-nimba-79-gold-prospectivity.webp` | Cestos Project (Fig. 2, left panel) | ~1340×1060px (~5:4) | "Gold mineralisation prospectivity surface, Nimba 79 licence area" |
| `07-nimba-79-cobalt-prospectivity.webp` | Cestos Project (Fig. 2, right panel) | ~1340×1060px (~5:4) | "Cobalt mineralisation prospectivity surface, Nimba 79 licence area" |
| `08-adj-licence-six-metal-anomaly.webp` | Cestos Project (Fig. 3) | ~2570×1440px (6-panel grid, 3×2) | "Cobalt, copper, manganese, niobium, tin and titanium prospectivity models over the ADJ licence" |
| `usr-logo-light.png` / `.svg` | Header (all pages), footer | Vector preferred | "U.S. Strategic Resources" |
| `usr-logo-dark.png` / `.svg` | Dark-background contexts (Cestos geology band, footer if dark) | Vector preferred | "U.S. Strategic Resources" |
| `favicon.png` | All pages `<head>` | 32×32, 180×180 (apple-touch), 512×512 (manifest) | — |

**Display rule (all figure images above):** `object-fit: contain`, never stretched or cropped to fill — preserves coordinates, legend and licence boundary as real information. Lightbox on tap/click for full-size viewing in an in-page overlay (not a new tab).

---

## 2. Pending — real photography needed from USR

| Filename | Used on | Recommended dimensions | Alt text | Brief for USR |
|---|---|---|---|---|
| `usr-hero-liberia-terrain.webp` | Home (hero background band) | 1920×1080 min, landscape, wide shot | "Exploration terrain in Nimba County, Liberia" | Wide shot of terrain/vegetation — needs to work with a dark overlay behind hero text; avoid busy skies or high-contrast midground that competes with type |
| `monrovia-liberia-operations-base.webp` | Why Liberia (operating platform section) | 1600×1000, landscape | "U.S. Strategic Resources operations base in Monrovia, Liberia" | Exterior or interior of the office, people working — not a generic stock office |
| `liberia-field-team-sampling.webp` | Why Liberia (field teams) | 1600×1000, landscape | "Field geologists conducting soil sampling in Nimba County, Liberia" | Geologists actively sampling in the field — most humanizing image on the site, prioritize if USR can only supply a few |

## 3. Pending — headshots (5, consistent framing required)

| Filename | Person | Recommended dimensions | Alt text |
|---|---|---|---|
| `david-kol-ceo-us-strategic-resources.webp` | David Kol | 800×800 (square, consistent crop across all 5) | "David Kol, CEO of U.S. Strategic Resources" |
| `peter-granata-cfo-us-strategic-resources.webp` | Peter Granata | 800×800 | "Peter Granata, CFO of U.S. Strategic Resources" |
| `robin-mcwatt-corporate-development-us-strategic-resources.webp` | Robin McWatt | 800×800 | "Robin McWatt, Corporate Development, U.S. Strategic Resources" |
| `brett-richards-board-member-us-strategic-resources.webp` | Brett Richards | 800×800 | "Brett Richards, Board Member, U.S. Strategic Resources" |
| `david-bellon-board-member-us-strategic-resources.webp` | Lt. Gen. David Bellon (Ret.) | 800×800 | "Lt. Gen. David Bellon (Ret.), Board Member, U.S. Strategic Resources" |

**Brief for USR:** same framing, lighting and background across all 5 — headshots that look like they came from 5 different sources undercut the institutional tone. Square crop, shoulders-up, neutral background.

**Note:** no dedicated page per person — bios live inline on the Company page (H3 blocks). Not building individual bio landing pages; not requested and adds thin-content pages with no SEO or investor value beyond what's already on Company.

---

## 4. Social & meta images (one per page, required before indexing)

| Page | OG image filename (suggested) | Dimensions | Notes |
|---|---|---|---|
| Home | `og-usr-home.webp` | 1200×630 | Licence map or hero terrain + logo lockup |
| Company | `og-usr-company.webp` | 1200×630 | Leadership group or logo on brand background |
| Cestos Project | `og-usr-cestos-project.webp` | 1200×630 | Licence map (file `06-...`) |
| Why Liberia | `og-usr-why-liberia.webp` | 1200×630 | Terrain/field photo once available |
| Critical Minerals & Strategy | `og-usr-critical-minerals.webp` | 1200×630 | Stat-forward graphic (90% / 98% / $30B) or logo on brand background |
| News | `og-usr-news.webp` | 1200×630 | Logo on brand background |
| Contact | `og-usr-contact.webp` | 1200×630 | Logo on brand background |
| Legal | *(inherit sitewide default, no dedicated OG image needed)* | — | — |

All OG images: JPEG or WebP, under 1MB, safe margin from edges (some platforms crop corners).

---

## 5. Naming & metadata checklist (apply to every image before it goes live)

- [ ] Filename follows `{subject}-{context}.webp` — lowercase, hyphens, descriptive (never `image1.png`, `final_v2.jpg`)
- [ ] Alt text written (see tables above) — descriptive, not keyword-stuffed, never empty for content images
- [ ] `width`/`height` attributes set in HTML to prevent layout shift
- [ ] `loading="lazy"` on every image below the fold
- [ ] File size optimized — WebP preferred, target under 200KB for photos, under 400KB for dense multi-panel figures
- [ ] Source/original stored in Drive; only optimized export enters the repo under `site/assets/`

---

## 6. Open questions for USR (blockers, not design decisions)

1. Can the field photography brief (terrain, Monrovia base, field team) be fulfilled from an existing photo library, or does it require new photography?
2. Headshots — same-session studio shoot for consistency, or can existing individual headshots be color/crop-matched afterward?
3. Confirm whether "Cestos Project" branding (used in filenames and copy) is approved, since image filenames referencing it would need renaming otherwise.
