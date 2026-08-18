# U.S. Strategic Resources — Website Content Map & Copy (v1)

Working document. Maps the Q3 2026 pitch deck to public website pages and drafts web copy with the full SEO layer applied. All copy in English. Items pending client input are marked **[PENDING: …]**.

---

## 1. Site architecture

| Page | URL | Source slides | Search intent |
|---|---|---|---|
| Home | `/` | 1, 2, 3, 4 (teasers) | Navigational / branded |
| Company | `/company` | 5, 15 | Branded — "who is behind this" |
| Cestos Project | `/cestos-project` | 6, 7, 8, 9, 14 | Informational — asset due diligence |
| Why Liberia | `/why-liberia` | 6, 13 | Informational — jurisdiction risk |
| Critical Minerals & Strategy | `/critical-minerals` | 3, 4, 10, 11, 12 | Informational — market thesis |
| News | `/news` | — (new) | Navigational |
| Contact | `/contact` | 17 | Transactional |
| Legal & Disclaimer | `/legal` | 17 (footer text) | — (noindex optional) |

**Primary nav:** 6 items, flat, no dropdowns — Company, Cestos Project, Why Liberia, Critical Minerals & Strategy, News, Contact. Home is not a nav item; the logo (header and footer) links to `/`, matching the zodiac-gold.com pattern. Legal & Disclaimer lives in the footer only, never in primary nav.

**Omitted from the public site (deliberately):**
- Slide 16 "The Ask" — round size, structure and valuation stay in the private deck.
- Agency-by-agency federal funding pipeline (slide 12) — summarized, not detailed. Application status is competitive information.
- All cap table / ownership placeholders.

**Naming note:** "Cestos Project" is a proposed project name (mirrors Zodiac's "Todi Project" convention; the deck never names the combined asset). Needs USR sign-off before build. Fallback URL: `/projects`.

---

## 2. Global rules (apply to every page)

1. One H1 per page. H1 ≠ meta title, always.
2. TL;DR / Key Takeaways block immediately after the intro paragraph.
3. Primary CTA after the first paragraph; closing CTA at page bottom; sticky mobile CTA ("Request the investor presentation") — mobile layout itself still pending a dedicated design pass (see Handoff Notes).
4. URLs: lowercase, hyphens, no numbers, no stopwords.
5. `noindex` sitewide until client approval. Then: GA4, GSC, sitemap submission.
6. Schema: `Organization` sitewide (JSON-LD in layout), `Person` on Company, `FAQPage` on Cestos Project and Critical Minerals, `BreadcrumbList` on all inner pages. No LocalBusiness.
7. Internal linking cluster:
   - Home → all pages.
   - Cestos Project ↔ Why Liberia ↔ Critical Minerals (the content cluster; link in-body, not only nav).
   - Every page closes with CTA → Contact.
   - News posts (future) link back to Cestos Project.
8. Share button on News posts and on the Cestos Project page.
9. Voice: sober, declarative, filing-adjacent. No triads, no "rapidly evolving landscape", no inflated adjectives. Numbers carry the argument.

---

## 3. Page copy

### 3.1 Home — `/`

- **Meta title:** U.S. Strategic Resources | Critical Minerals in Liberia
- **Meta description:** American exploration company proving rare earth and critical mineral supply on two licence areas in Liberia, West Africa, for U.S. supply chains.
- **H1:** Securing America's critical mineral supply

**Hero (H1 + subline):**

> # Securing America's critical mineral supply
> Critical minerals and rare earths exploration on Liberia's Cestos shear zone.

**Intro paragraph:**

U.S. Strategic Resources is an American exploration and development company formed with a single mandate: prove critical mineral and rare-earth supply on secured ground in West Africa and deliver it into U.S. supply chains. The company holds two contiguous licence areas in Nimba County, Liberia, with government-surveyed anomalies across rare earths, battery, base, technology and strategic metals — plus gold.

**[CTA]** Request the investor presentation →

**Key takeaways:**
- Two contiguous licence areas on Liberia's Cestos shear zone, west of the Ity gold mine.
- National survey data covering 69 elements; 20 flagged as strategic.
- Positioned for the widest U.S. federal funding window for critical minerals in decades — $30B+ deployed to date.
- Experienced in-country operating platform in Monrovia. Zero mobilization lead time.

**H2: Why now**

One nation controls the inputs of modern power. Roughly 90% of global rare-earth refining capacity runs through China, along with 98% of refined gallium and germanium. Since April 2025, seven rare earths — including samarium — sit under Chinese export controls. Washington is deploying capital to change that: five executive orders on minerals security, a $12B national stockpile, and six federal funding channels open to companies operating on allied ground.

*Link in-body → `/critical-minerals`*

**H2: The asset**

Two licence areas — Nimba 79 Resources and ADJ Exploration — sit on the gold-prospective Cestos shear zone. Government survey data outlines coincident multi-element anomalies inside both licence boundaries: gold, cobalt, copper, gallium, titanium, tin and zirconium on Nimba 79; six metals anomalous on ADJ.

*Link in-body → `/cestos-project`*

**H2: Commodity exposure**

| Class | Examples | Demand driver |
|---|---|---|
| Rare earths | Nd · Sm · La · Pr · Eu | Permanent magnets — EVs, wind, defence |
| Battery metals | Li · Co · Ni · Mn | EV batteries and storage |
| Base metals | Cu · Zn · Sn | Electrification backbone |
| Technology metals | Ga · Ge · Zr | Semiconductors, solar, displays |
| Strategic metals | Nb · Ta · Ti · V | Aerospace and defence alloys |
| + Gold | Au | Cestos-shear discovery upside |

**H2: Leadership** — 3-up teaser (Kol, Granata, Richards) → `/company`

**H2: Latest news** — 3 most recent posts → `/news`

**Closing CTA:** Speak with the team → `/contact`

**Images:**
- `cestos-shear-zone-licence-map.webp` — alt: "Map of the Nimba 79 Resources and ADJ Exploration licence areas on the Cestos shear zone, Nimba County, Liberia"
- `usr-hero-liberia-terrain.webp` — alt: "Exploration terrain in Nimba County, Liberia" **[PENDING: real field photography from USR]**

---

### 3.2 Company — `/company`

- **Meta title:** About U.S. Strategic Resources | Team & Leadership
- **Meta description:** Purpose-built and independent. Meet the team behind U.S. Strategic Resources — capital markets, African mining operations and U.S. defence experience.
- **H1:** Purpose-built. Independent. One mandate.

**Intro paragraph:**

U.S. Strategic Resources was founded as a standalone company with a single mandate: prove and deliver U.S.-aligned critical mineral supply from West Africa's most underexplored terrane. The company combines an experienced in-country operating platform in Liberia with leadership drawn from capital markets, African mining operations and the U.S. defence establishment.

**[CTA]** Request the investor presentation →

**Key takeaways:**
- Standalone company, independent of any parent group.
- Operations base in Monrovia, Liberia. **[PENDING: HQ city, jurisdiction and incorporation date]**
- Board and management with 100+ combined years across mining, finance and defence.

**H2: The company**

- Incorporated: **[PENDING]**
- Headquarters: **[PENDING]** · Operations: Monrovia, Liberia
- One asset base. One flag. Built to move at the speed of the federal window.

**H2: Leadership**

*(H3 per person; bios rewritten as prose, 40–60 words each. `Person` schema per bio.)*

**H3: David Kol — Chief Executive Officer & Board Member**
David Kol brings more than 20 years in capital markets and M&A, including 17+ years operating in West Africa. He is the founder and CEO of Zodiac Gold (TSXV: ZAU), an exploration company advancing a district-scale gold project in Liberia.

**H3: Peter Granata, CA — Chief Financial Officer**
Peter Granata has spent 18+ years in African natural resources. A former audit manager in PwC's Global Mining & Metals practice, he has served as CFO across multiple TSXV-listed issuers.

**H3: Robin McWatt — Corporate Development**
Robin McWatt has over a decade of experience in capital markets and M&A advisory, including roles as Vice President at FMI Capital Advisory and analyst at Sionna.

**H3: Head of Exploration — search underway**
Target profile: a chartered geologist with a West African greenstone gold and critical-minerals field record. Technical and government-affairs advisory appointments to be announced.

**H2: Board of Directors**

**H3: Brett Richards — Board Member**
A 40-year mining executive who has built three mines in Africa. Former CEO of Katanga Mining and Avocet plc.

**H3: Lt. Gen. David Bellon (Ret.) — Board Member**
A 35-year career in the United States Marine Corps, including command of Marine Forces South and the Marine Corps Reserve.

**Closing CTA:** See the asset → `/cestos-project` · Speak with the team → `/contact`

**Images:**
- `david-kol-ceo-us-strategic-resources.webp` — alt: "David Kol, CEO of U.S. Strategic Resources" *(same pattern per person)* **[PENDING: headshots]**

---

### 3.3 Cestos Project — `/cestos-project`

- **Meta title:** Cestos Project | Critical Minerals Licences in Liberia
- **Meta description:** Two contiguous licence areas on Liberia's Cestos shear zone with government-surveyed anomalies across rare earths, battery, base and strategic metals, plus gold.
- **H1:** District-scale ground on the Cestos shear zone

**Intro paragraph:**

The Cestos Project comprises two contiguous licence areas — the Nimba 79 Resources Licence and the ADJ Exploration Licence — in Nimba County, Liberia. Both sit on the gold-prospective Cestos shear zone, west of the world-class Ity gold mine. National geochemical survey data covering 69 elements outlines coincident multi-element anomalies inside both licence boundaries.

**[CTA]** Request the technical overview →

**Key takeaways:**
- Two contiguous licences, combined area **[PENDING: km²]**.
- Government survey: 69 elements analysed, 20 flagged strategic.
- Nimba 79: high prospectivity for gold, cobalt, copper, gallium, titanium, tin and zirconium.
- ADJ: six metals — cobalt, copper, manganese, niobium, tin, titanium — anomalous within a single tenement.

**H2: The licences**

| | Nimba 79 Resources | ADJ Exploration |
|---|---|---|
| Location | Nimba County, Cestos shear zone | Contiguous with Nimba 79 |
| Licence no. / grant / expiry | **[PENDING]** | **[PENDING]** |
| Headline anomalies | Au, Co, Cu, Ga, Ti, Sn, Zr | Co, Cu, Mn, Nb, Sn, Ti |

**H2: Geology**

Melanocratic and leucocratic gneiss intruded by diorite and deformed by the Cestos shear zone — host geology for both orogenic gold and critical mineral systems. The shear zone is the same structural corridor that hosts the Ity gold mine to the east.

**H2: Exploration targets**

**H3: Nimba 79 — coincident multi-element anomalies**
Prospectivity mapping outlines a strong gold anomaly in the licence north-east and a strong cobalt anomaly across the east, with high-prospectivity surfaces for copper, gallium and titanium in the south, tin in the north-east and south, and zirconium in the south-west. Moderate prospectivity: nickel, vanadium, tantalum, niobium. **[PENDING: model methodology, data source & year]**

**H3: ADJ — six metals, one coherent anomaly**
Cobalt, copper, manganese, niobium, tin and titanium prospectivity models each place the ADJ licence within a strong regional anomaly — a rare degree of multi-commodity overlap on a single tenement.

**H2: Commodity portfolio** *(reuse Home table, expanded with the demand notes from slide 9)*

**H2: Roadmap — anomalies to drill-tested targets in 24 months**

| Phase | Window | Duration | Deliverable |
|---|---|---|---|
| I — Desktop compilation & target ranking | Q4 2026 | 3 months | Ranked target portfolio, drill-ready recommendations |
| II — Field verification & sampling | Q1–Q3 2027 | 9 months | Drill-permitted, geophysically defined targets |
| III — Drill testing & resource development | Q4 2027–Q3 2028 | 12 months | Drill-tested targets, initial resource estimates |

**H2: Frequently asked questions** *(FAQPage schema)*

- **Where is the Cestos Project located?** In Nimba County, Liberia, on the Cestos shear zone, west of the Ity gold mine.
- **What minerals has the project been surveyed for?** National survey data covers 69 elements; 20 are flagged as strategic, spanning rare earths, battery, base, technology and strategic metals, plus gold.
- **Is the project drill-ready?** Not yet. Phase I (target ranking) and Phase II (field verification) are designed to take ranked targets to drill-permitted status within 12 months.
- **Who holds the licences?** **[PENDING: tenure structure — answer must match licence documentation]**
- **How does gold fit a critical minerals strategy?** The Cestos shear zone is gold-prospective; gold potential acts as a discovery engine that carries the critical-minerals program.

**Closing CTA:** Why Liberia → `/why-liberia` · Request the investor presentation → `/contact`

**Images:**
- `nimba-79-adj-licence-map-regional-geology.webp` — alt: "Nimba 79 Resources and ADJ Exploration licences over regional geology, Nimba County, Liberia"
- `nimba-79-gold-cobalt-prospectivity.webp` — alt: "Interpolated gold and cobalt prospectivity surfaces across the Nimba 79 licence area"
- `adj-licence-six-metal-anomaly.webp` — alt: "Cobalt, copper, manganese, niobium, tin and titanium prospectivity models over the ADJ licence"

---

### 3.4 Why Liberia — `/why-liberia`

- **Meta title:** Why Liberia | Mining Exploration in West Africa
- **Meta description:** Underexplored terrane, national survey data and an established in-country platform: the case for critical minerals exploration in Liberia, West Africa.
- **H1:** Why we operate in Liberia

**Intro paragraph:**

Liberia hosts one of West Africa's most underexplored terranes — Birimian-age geology on trend with some of the region's largest gold discoveries, yet with a fraction of the drilling. The government's national geochemical survey gives explorers a data foundation that most frontier jurisdictions lack. U.S. Strategic Resources operates here through an established platform built over years of in-country work.

**[CTA]** See the project →

**Key takeaways:**
- Underexplored geology on the Cestos shear zone, west of the Ity gold mine.
- National survey: 69 elements analysed countrywide — rare data depth for a frontier jurisdiction.
- Established Monrovia operating base; zero mobilization lead time.

**H2: The operating platform**

- **Monrovia office** — established base with logistics, procurement and administration in place.
- **Field teams** — geologists and crews with seasons of terrane-specific fieldwork.
- **Drill operations** — drilling capability and contractor relationships ready to mobilize.
- **Drone & geophysics** — survey capability for rapid, low-cost target refinement.
- **Government access** — working relationships with the Ministry of Mines & Energy and regulators.
- **Community trust** — long-standing local relationships and social licence to operate.

**H2: Community & responsibility**

*(Short section for the mockup; flag to USR that this should grow into a standalone ESG page — sector standard, and Zodiac has one.)* **[PENDING: community programs, environmental commitments, local employment figures]**

**Closing CTA:** The market case → `/critical-minerals` · Contact the team → `/contact`

**Images:**
- `monrovia-liberia-operations-base.webp` — alt: "U.S. Strategic Resources operations base in Monrovia, Liberia" **[PENDING: real photography]**
- `liberia-field-team-sampling.webp` — alt: "Field geologists conducting soil sampling in Nimba County, Liberia" **[PENDING: real photography]**

---

### 3.5 Critical Minerals & Strategy — `/critical-minerals`

- **Meta title:** Critical Minerals Supply Gap & U.S. Federal Funding
- **Meta description:** China refines ~90% of rare earths. Washington has deployed $30B+ to change that. How U.S. Strategic Resources is positioned for the federal funding window.
- **H1:** The case for U.S.-aligned critical mineral supply

**Intro paragraph:**

Roughly 90% of global rare-earth refining capacity runs through China — end-to-end leverage from mine to magnet — along with 98% of refined gallium and germanium, the backbone of semiconductors and defence electronics. Since April 2025, seven rare earths, including samarium, sit under Chinese export controls. Export licences now decide who builds. The United States is deploying capital to change that.

**[CTA]** See how the project fits →

**Key takeaways:**
- Five executive orders on minerals security: direct equity, price floors and offtake authorities now in force.
- $30B+ in U.S. government capital deployed across equity stakes, loans and stockpiling.
- Project Vault: a $12B national critical-minerals stockpile — a standing federal buyer.
- $500M U.S.–Africa Strategic Investment Program, Critical Minerals as Focus Area 1; $5–50M per award.

**H2: The problem — concentration**
*(90% / 98% / 7 stats as large figures; two short paragraphs.)*

**H2: The moment — the federal window**
*(Executive orders, FORGE and the 54-nation Ministerial, Project Vault, U.S.–Africa program. Two paragraphs + stat row.)*

**H2: Demand outruns supply**

| Signal | Figure | Source |
|---|---|---|
| Lithium demand by 2040 | 3× | IEA projection |
| Copper deficit, 2026 | 150–330 kt | Structural shortfall forecast |
| Federal stockpile buying | $12B | Project Vault |
| Permanent-magnet market by 2030 | $30B | MarketsandMarkets (~$22B in 2025, 6.4% CAGR) |

**H2: Business model — explore, prove, partner, deliver**
*(4-step numbered sequence from slide 11, one sentence each.)*

**H2: Federal funding channels**

Six channels pursued in parallel: State Department APS programs (the lead vehicle), DFC development finance, EXIM supply-chain facilities, USTDA feasibility grants, DoD industrial-base programs, and the 54-nation FORGE platform. Precedent transactions show juniors on allied ground getting funded. *(No application-status detail on the public site.)*

**H2: Frequently asked questions** *(FAQPage schema)*

- **What are critical minerals?** Minerals designated essential to economic and national security — including rare earths, battery metals like lithium and cobalt, and technology metals like gallium — where supply is concentrated or at risk.
- **Why does Chinese export control matter?** With ~90% of rare-earth refining and 98% of refined gallium and germanium, export licences effectively decide which countries can build magnets, semiconductors and defence systems.
- **What is Project Vault?** A $12B U.S. national critical-minerals stockpile that creates a standing federal buyer for strategic supply.
- **How does U.S. Strategic Resources access federal funding?** Through six parallel channels open to companies proving supply on allied ground — from State Department programs to DFC equity and USTDA technical grants.

**Closing CTA:** The asset → `/cestos-project` · Request the investor presentation → `/contact`

---

### 3.6 News — `/news`

- **Meta title:** News & Announcements | U.S. Strategic Resources
- **Meta description:** Company announcements, exploration updates and media coverage from U.S. Strategic Resources.
- **H1:** News & announcements
- Launches with 1 placeholder-free item if possible (e.g., company formation announcement) — otherwise a clean empty state: "Announcements will be published here. Subscribe for updates."
- Post URLs: `/news/company-formation-announcement` (no dates/numbers in slugs).
- Each post: share button, author = Organization, `NewsArticle` schema, link back to `/cestos-project`.
- **Deindex `/news/page/2` etc. (checklist item 19) — applies here.**

---

### 3.7 Contact — `/contact`

- **Meta title:** Contact U.S. Strategic Resources
- **Meta description:** Reach the U.S. Strategic Resources team — investor enquiries, partnership discussions and media requests.
- **H1:** Speak with the team
- Intro line + form: name, organization, email, enquiry type (Investor / Partner / Media / Other), message. No `<form>`-to-nowhere: wire to Formspree/Netlify Forms for the mockup.
- Operations: Monrovia, Liberia · HQ: **[PENDING]** · Email: **[PENDING]** · Phone: **[PENDING]**
- Optional: newsletter signup (Zodiac pattern).

---

### 3.8 Legal & Disclaimer — `/legal`

- **H1:** Legal notice & forward-looking statements
- Base text from slide 17, expanded: no offer of securities; forward-looking statements involve risks and uncertainties; exploration results are preliminary; information subject to verification.
- Add: website terms of use, privacy note (needed once GA4 is live — cookie/analytics disclosure). **[PENDING: legal review by USR counsel]**
- Linked from footer sitewide. Candidate for `noindex`.

---

## 4. Image inventory & naming convention

Pattern: `{subject}-{context}.webp`, all lowercase, hyphens. Every image gets descriptive alt text (drafted per page above). Source files stay in Drive; only optimized WebP/AVIF exports enter the repo under `/public/assets/`.

**To extract from the deck:** licence/geology map (slide 6), Nimba 79 prospectivity surfaces (slide 7), ADJ prospectivity surfaces (slide 8).
**To request from USR:** field photography (terrain, teams, Monrovia base), leadership headshots, logo files (SVG), any drone footage.

---

## 5. Pending from USR (blockers before public launch)

1. Incorporation details: jurisdiction, date, HQ city.
2. Licence numbers, grant dates, expiry, terms; combined km².
3. Survey source, date and prospectivity model methodology.
4. Project name approval ("Cestos Project" proposed).
5. Contact details: email, phone, HQ address.
6. Field photography + headshots + logo in SVG.
7. ESG/community content.
8. Legal review of disclaimer text.
9. Domain name + confirmation of what stays private (Ask, pipeline status, cap table).

*None of these block the mockup — placeholders render as design elements. All of them block indexing.*

---

## 6. Copy voice rules (for every future edit)

- Declarative sentences. Numbers first, adjectives last.
- Banned: "rapidly evolving", "unlock", "leverage" (as verb), "world-class" (except quoting the deck's Ity reference), "cutting-edge", stacked triads, em-dash chains.
- Every claim traceable to the deck or a **[PENDING]** flag. No invented facts on a securities-adjacent site.
- U.S. spelling. "U.S. Strategic Resources" on first mention per page; "USR" thereafter is acceptable in body copy, never in headings.
