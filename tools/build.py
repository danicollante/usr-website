#!/usr/bin/env python3
"""Build the static site. Copy is taken verbatim from the investor deck."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shell import head, header, footer, footer as foot, img, write, MAP, EMAIL, SITE

BRAND = "U.S. Strategic Resources"


def rebase(html):
    """Rewrite root-relative links for pages one directory deep."""
    return re.sub(r'(href|src|srcset)="(?!https?:|mailto:|#|/|\.\.)', r'\1="../', html)


def rebase_srcset(html):
    """srcset holds several comma-separated URLs; fix the ones after the first."""
    def fix(m):
        parts = [p.strip() for p in m.group(2).split(",")]
        out = []
        for p in parts:
            if p.startswith(("http", "../", "/")):
                out.append(p)
            else:
                out.append("../" + p)
        return f'{m.group(1)}="{", ".join(out)}"'
    return re.sub(r'(srcset)="([^"]+)"', fix, html)


# Outbound PubChem links on chemical symbols — restored from the pre-rebuild
# site's tools/element-symbols.py convention (same base URL, same element
# names), scoped to the new .element / .metal card markup rather than the
# old touch-popover widget: these cards already show the full name and note
# beside the symbol, so only the symbol itself needs to become a link.
PUBCHEM_BASE = "https://pubchem.ncbi.nlm.nih.gov/element/"
PUBCHEM_NAMES = {
    "Au": "Gold", "Co": "Cobalt", "Cu": "Copper", "Ga": "Gallium",
    "Ti": "Titanium", "Sn": "Tin", "Zr": "Zirconium", "Mn": "Manganese",
    "Nb": "Niobium", "Ni": "Nickel", "V": "Vanadium", "Ta": "Tantalum",
}


def pubchem_link(sym):
    name = PUBCHEM_NAMES[sym]
    return (f'<a class="element-link" href="{PUBCHEM_BASE}{name}" '
            f'target="_blank" rel="noopener">{sym}'
            f'<span class="visually-hidden"> &mdash; {name}, on PubChem '
            f'(opens in a new tab)</span></a>')


# ══════════════════════════════════════════════════════════════════════════
# index.html — deck slide 01
# ══════════════════════════════════════════════════════════════════════════
def build_index():
    hero_img = img(
        "terrain-sandstone",
        "",
        "100vw",
        loading="eager",
        fetchpriority="high",
    )
    band = img("drill-rig",
               "Exploration drill rig on site in Nimba County, Liberia",
               "100vw")

    html = head(
        f"{BRAND} — Securing U.S.-aligned critical minerals supply",
        "An American-backed mining investment vehicle formed to explore for "
        "critical minerals and rare earths in Nimba County, Liberia.",
        "index.html",
    )
    html += f"""<main id="main">

  <!-- ═══ Hero — deck slide 01 ═══ -->
  <section class="hero">
    {hero_img}
    <div class="hero__inner">
{header('index.html')}
      <div class="hero__grid">
        <div class="reveal">
          <p class="label label--rule hero__eyebrow">Nimba County, Liberia</p>
          <h1 class="display">Securing U.S.-aligned critical minerals supply</h1>
          <p class="lede hero__sub">U.S. Strategic Resources is an American-backed
             mining investment vehicle formed to explore for critical minerals and
             rare earths in West Africa.</p>
          <div class="btn-row hero__actions">
            <a class="btn" href="about.html#assets">The assets</a>
            <a class="btn-quiet" href="leadership.html">Leadership</a>
          </div>
          <p class="hero__disclaimer">Exploration stage. No mineral resource or
             reserve has been defined on either license.</p>
        </div>
{MAP}
      </div>
    </div>
  </section>

  <!-- ═══ Mission / Execution — deck slide 01, verbatim ═══ -->
  <section class="section section--ink">
    <div class="wrap">
      <div class="section-head reveal">
        <div>
          <p class="label section-head__eyebrow">Who we are</p>
          <h2 class="h2">An American-backed vehicle for allied supply security</h2>
        </div>
        <p class="section-head__note">Formed to explore for critical minerals and
           rare earths in West Africa, on two contiguous license areas in a
           jurisdiction aligned with the United States and its allies.</p>
      </div>
      <div class="cards cards--2 cards--equal reveal-group">
        <article class="card">
          <p class="label">Mission</p>
          <h3 class="h4">Delivering critical minerals to allied supply chains</h3>
          <p>Our objective is to deliver critical minerals production to U.S. and
             allied supply chains, providing the key resources that will define and
             power the 21st century global economy.</p>
        </article>
        <article class="card">
          <p class="label">Execution</p>
          <h3 class="h4">A team that has built mines in West Africa</h3>
          <p>We are backed by a world-class team of U.S. foreign diplomacy experts
             and mineral exploration executives who have made discoveries, built
             mines, and operated across West Africa for decades.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- ═══ Full-bleed duotone band ═══ -->
  <div class="band duo duo--band">
    {band}
    <div class="duo__content">
      <div class="wrap">
        <p class="label">Exploration, not production</p>
        <p class="body t-soft measure" style="margin-top:12px">Drilling and
           prospectivity work across two contiguous license areas on the
           gold-prospective Cestos shear zone.</p>
      </div>
    </div>
  </div>

  <!-- ═══ Teasers — no section head. The prior copy here ("Three things to
       look at" / "the people" standfirst) was invented, not sourced from the
       deck, and was internally inconsistent (it named three destinations
       including "the people" while only three of the site's four sections
       were linked, and Leadership wasn't one of them). Four cards, one per
       destination, stand alone rather than being introduced by writing new
       marketing copy for a section the deck doesn't supply a line for. ═══ -->
  <section class="section section--ink">
    <div class="wrap">
      <div class="cards cards--4 cards--equal reveal-group">
        <a class="teaser" href="about.html#assets">
          <p class="label">About us &mdash; Assets</p>
          <h3 class="h4">The assets</h3>
          <p>Two contiguous license areas in Nimba County with coincident
             multi-element anomalies across gold and six critical minerals.</p>
          <span class="link-arrow">The assets &rarr;</span>
        </a>
        <a class="teaser" href="about.html#jurisdiction">
          <p class="label">About us &mdash; Jurisdiction</p>
          <h3 class="h4">The jurisdiction</h3>
          <p>Liberia: U.S. dollar legal tender, English-language common law, and
             a 243 km railway already running to deep water.</p>
          <span class="link-arrow">Jurisdiction &rarr;</span>
        </a>
        <a class="teaser" href="leadership.html">
          <p class="label">Leadership</p>
          <h3 class="h4">The team</h3>
          <p>A world-class team of U.S. foreign diplomacy experts and mineral
             exploration executives who have made discoveries, built mines, and
             operated across West Africa for decades.</p>
          <span class="link-arrow">Board &amp; management &rarr;</span>
        </a>
        <a class="teaser" href="metals.html">
          <p class="label">Metals &amp; markets</p>
          <h3 class="h4">The metals</h3>
          <p>Technology metals are moving into a structural supply deficit — a
             setup that favors them over the broader commodity complex.</p>
          <span class="link-arrow">Metals &amp; markets &rarr;</span>
        </a>
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("index.html", html)


# ══════════════════════════════════════════════════════════════════════════
# about.html — deck slides 02, 03, 04
# ══════════════════════════════════════════════════════════════════════════

NIMBA_1 = [
    ("Au", "Gold",      "NE"),
    ("Co", "Cobalt",    "E"),
    ("Cu", "Copper",    "S"),
    ("Ga", "Gallium",   "S"),
    ("Ti", "Titanium",  "S"),
    ("Sn", "Tin",       "NE/S"),
    ("Zr", "Zirconium", "SW"),
]

NIMBA_2 = [
    ("Co", "Cobalt",    "Battery"),
    ("Cu", "Copper",    "Base"),
    ("Mn", "Manganese", "Battery"),
    ("Nb", "Niobium",   "Defense"),
    ("Sn", "Tin",       "Tech"),
    ("Ti", "Titanium",  "Defense"),
]

FACTS = [
    ("Tenure",
     "5-year Exploration License, convertible to a Mineral Development "
     "Agreement of up to 25 years."),
    ("Surveyed",
     "National survey data: 69 elements analysed, 20 flagged strategic across "
     "the license areas."),
    ("Nearology",
     "On the gold-prospective Cestos shear zone, west of the world-class Ity "
     "gold mine."),
    ("Upside",
     "Gold exploration potential intended to complement the critical-minerals "
     "program."),
]

JURISDICTION = [
    ("Strong U.S. ties",
     "Founded with American backing in 1847, Liberia uses the U.S. dollar as "
     "legal tender and runs an English-language common-law system modeled on "
     "the United States."),
    ("Proven mining jurisdiction",
     "ArcelorMittal, Bea Mountain and Bao Chico all operate at scale under "
     "Mineral Development Agreements of up to 25 years — a tested, bankable "
     "tenure framework rather than an untested frontier regime."),
    ("Infrastructure in place",
     "The 243 km Yekepa&ndash;Buchanan railway runs from Nimba County to a "
     "deep-water port, and Government policy is opening it to multi-user "
     "access. Export logistics already exist."),
]

DIFFERENTIATION = [
    ("01", "Project Delivery &amp; Exploration Acumen",
     "A leadership team with repeated exploration success in frontier "
     "jurisdictions, including discoveries developed into commissioned, "
     "producing mines."),
    ("02", "U.S. Government Financing",
     "Experience navigating the U.S. federal funding ecosystem, with the "
     "relationships and process knowledge to access sovereign-backed capital."),
    ("03", "Strategic Asset Origination",
     "Sourcing and securing critical mineral assets in jurisdictions that "
     "matter to Western supply security, underwritten by full technical and "
     "legal diligence."),
]


def elements_grid(items, pad_to):
    cells = []
    for sym, name, note in items:
        cells.append(
            f'<div class="element"><div class="element__sym">{pubchem_link(sym)}</div>'
            f'<div class="element__name">{name}</div>'
            f'<div class="element__note">{note}</div></div>')
    for _ in range(pad_to - len(items)):
        cells.append('<div class="element element--empty"></div>')
    return "\n            ".join(cells)


def build_about():
    html = head(
        f"About — {BRAND}",
        "Two contiguous exploration licenses in Nimba County, Liberia: the "
        "assets, the jurisdiction, and what sets USR apart.",
        "about.html",
    )
    html += f"""<main id="main">

{header('about.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">About us</p>
        <h1 class="h1">Two contiguous licenses in a U.S.-aligned jurisdiction</h1>
      </div>
      <p class="section-head__note">Nimba County, Liberia. Exploration stage,
         with prospectivity mapping across gold and the critical minerals
         Washington is funding.</p>
    </div>
  </div>

  <!-- ═══ Assets — deck slide 02 ═══ -->
  <section class="section section--paper" id="assets">
    <div class="wrap">
      <div class="section-head section-head--wide reveal">
        <div>
          <p class="label section-head__eyebrow">About us &mdash; Assets</p>
          <h2 class="h2">World-Class West African Critical Minerals Opportunity</h2>
        </div>
        <p class="section-head__note">Two contiguous license areas in Nimba
           County, Liberia: a mining-friendly, underexplored jurisdiction
           aligned with the U.S. and its allies.</p>
      </div>

      <div class="unit reveal">
        <div class="unit__split">
          <div class="unit__col">
            <div class="unit__head">
              <div class="unit__name">Nimba 1</div>
              <div class="unit__rank">High</div>
            </div>
            <h3 class="h4">Coincident multi-element anomalies</h3>
            <p class="body-sm measure-sm">Prospectivity mapping outlines gold plus
               the critical minerals Washington is funding — inside one license
               boundary.</p>
            <div class="elements">
            {elements_grid(NIMBA_1, 8)}
            </div>
          </div>

          <div class="unit__col">
            <div class="unit__head">
              <div class="unit__name">Nimba 2</div>
              <div class="unit__rank">Anomalous</div>
            </div>
            <h3 class="h4">Six metals, one coherent anomaly</h3>
            <p class="body-sm measure-sm">Cobalt, copper, manganese, niobium, tin
               and titanium models each place the license within a strong regional
               anomaly — unusual multi-commodity overlap on a single tenement.</p>
            <div class="elements">
            {elements_grid(NIMBA_2, 8)}
            </div>
          </div>
        </div>

        <div class="facts">
          {"".join(f'''
          <div class="fact">
            <div class="fact__term">{t}</div>
            <p class="fact__value">{v}</p>
          </div>''' for t, v in FACTS)}
        </div>

        <div class="unit__disclaimer">
          <p class="label">Interpretive models</p>
          <p>Prospectivity models are interpretive and conceptual; no mineral
             resource or reserve has been defined on either license.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ═══ Full-bleed band — the one patriotic image, on Jurisdiction, kept
       in native colour. Scoped exception to the site's duotone convention:
       the flag reads better in colour and colour is doing work here. ═══ -->
  <div class="band photo--band">
    {img("us-flag", "The flag of the United States", "100vw")}
    <div class="duo__content">
      <div class="wrap">
        <p class="label">Strong U.S. ties</p>
        <p class="body t-soft measure" style="margin-top:12px">Founded with
           American backing in 1847, Liberia uses the U.S. dollar as legal tender
           and runs an English-language common-law system modeled on the United
           States.</p>
      </div>
    </div>
  </div>

  <!-- ═══ Jurisdiction — deck slide 03 ═══ -->
  <section class="section section--ink" id="jurisdiction">
    <div class="wrap">
      <div class="section-head reveal">
        <div>
          <p class="label section-head__eyebrow">About us &mdash; Jurisdiction</p>
          <h2 class="h2">Liberia: a proven, U.S.-aligned mining jurisdiction</h2>
        </div>
        <p class="section-head__note">A tested, bankable tenure framework rather
           than an untested frontier regime.</p>
      </div>

      <div class="split" style="align-items:start">
        <dl class="rows reveal-group">
          {"".join(f'''
          <div class="row">
            <dt><span class="label row__label">{t}</span></dt>
            <dd>{v}</dd>
          </div>''' for t, v in JURISDICTION)}
        </dl>
        <figure style="margin:0">
          <div class="duo ratio-4-5">
            {img("rail-corridor",
                 "Ore train on the Yekepa to Buchanan railway, Liberia",
                 "(max-width: 1100px) 100vw, 380px")}
          </div>
          <figcaption class="figcap">
            <span>Yekepa&ndash;Buchanan</span>
            <span class="t-lift">243 km to deep water</span>
          </figcaption>
          <div class="map__caption" style="margin-top:26px">
            <span>License areas</span>
            <span class="t-lift">Nimba 1 &middot; Nimba 2</span>
          </div>
        </figure>
      </div>
    </div>
  </section>

  <!-- ═══ Differentiation — deck slide 04 ═══ -->
  <section class="section section--alt" id="differentiation">
    <div class="wrap">
      <div class="section-head reveal">
        <div>
          <p class="label section-head__eyebrow">About us &mdash; Differentiation</p>
          <h2 class="h2">What sets USR apart</h2>
        </div>
        <p class="section-head__note">Three capabilities that are difficult to
           assemble in one vehicle.</p>
      </div>
      <div class="cards cards--3 reveal-group">
        {"".join(f'''
        <article class="card">
          <div class="card__index">{n}</div>
          <h3 class="h4">{t}</h3>
          <p>{b}</p>
        </article>''' for n, t, b in DIFFERENTIATION)}
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("about.html", html)


# ══════════════════════════════════════════════════════════════════════════
# leadership.html — deck slides 05, 06, 07
# ══════════════════════════════════════════════════════════════════════════

PEOPLE = [
    ("David Kol", "CEO &amp; Board member",
     "david-kol-ceo-us-strategic-resources.webp",
     ["A serial entrepreneur with more than 20 years of experience in capital "
      "markets, M&amp;A, and executive management across the mineral resource, "
      "media and entertainment, and technology sectors, David has raised over "
      "US$100 million in equity and debt financing across a range of ventures. "
      "He is the Founder and CEO of Zodiac Gold Inc. (TSXV: ZAU | OTCQB: ZAUIF), "
      "a West Africa gold exploration company, and a founding partner of Global "
      "Frontier Advisors L.P.",
      "David has spent more than 17 years working throughout West Africa and "
      "serves as Co-Chair of the Overseas Security Advisory Council &ndash; "
      "Liberia and Vice President of the Liberia Chamber of Mines."]),

    ("Lt. Gen. David Bellon (Ret.)", "Board member",
     "david-bellon-board-us-strategic-resources.webp",
     ["A retired three-star general who served among the most senior leaders of "
      "the U.S. armed forces. David culminated a 35-year Marine Corps career as "
      "Commander of Marine Forces South and Commander of the Marine Corps "
      "Reserve where he held responsibility for Marine Corps equities across 32 "
      "countries in Latin America and the Caribbean. As Managing Director of "
      "Global Frontier Advisors L.P., David brings deep reach throughout the "
      "U.S. government and national security enterprise.",
      "David currently serves as Chairman of the Board for the Marine Toys for "
      "Tots Foundation, Advisory Board Member at Aftermath Silver Inc., and as "
      "an Advisor to the Geopolitical Intelligence Group at Academy Securities "
      "Inc. where he counsels several leading U.S. investment firms on "
      "geopolitics and foreign policy."]),

    ("Samantha A. Carl-Yoder", "Board member",
     "samantha-carl-yoder-board-us-strategic-resources.webp",
     ["Samantha Carl-Yoder is co-chair of Brownstein Hyatt Farber Schreck's "
      "international and critical minerals practices, where she advises global "
      "mining and energy companies on market entry, bilateral partnerships, and "
      "project financing, helping clients secure capital for greenfield projects "
      "and build durable mineral supply chains. She previously led international "
      "government relations for a global LNG company across Asia, the Middle "
      "East, and South America. Before entering the private sector, Samantha "
      "served nearly twenty years as a U.S. foreign service officer, with "
      "postings in Indonesia, Peru, Myanmar, and Brazil, and held senior State "
      "Department roles in both the Obama and Trump administrations, including "
      "chief of staff to the Under Secretary for Political Affairs. She is an "
      "independent board member of Ivanhoe Atlantic and serves on the boards of "
      "the Atlantic Council and the U.S. Chamber of Commerce's U.S.-Africa "
      "Business Council."]),

    ("Brett Richards", "Board member",
     "brett-richards-board-us-strategic-resources.webp",
     ["Brett Richards is a mining executive, investor, and entrepreneur with "
      "nearly 40 years of experience leading private and publicly listed mining "
      "companies, from micro-cap explorers to large-scale multi-asset producers, "
      "across five continents and more than 30 countries. He was part of the "
      "five-person founding team of Katanga Mining in the DRC, prior to its "
      "acquisition by Glencore, and held earlier senior executive roles at "
      "Kinross Gold and Co-Steel. Over his career he has built three mines, "
      "rehabilitated two more, and raised substantial capital across market "
      "cycles. Deeply experienced in West Africa, Brett is Chief Executive "
      "Officer of Pasofino Gold, developer of Liberia's largest undeveloped gold "
      "project, Chair of Zodiac Gold, and a director of Gold X2 Mining, Sherritt "
      "International, Nickel 28 Capital, and Midnight Sun Mining."]),

    ("Peter Granata, CA", "CFO",
     "peter-granata-cfo-us-strategic-resources.webp",
     ["Peter is a Chartered Accountant with 18+ years of experience working in "
      "the African natural resource sector. He currently serves as CFO of a "
      "Liberian-based gold exploration company and previously held senior roles "
      "at public mineral exploration companies including East Africa Metals and "
      "Canaco Resources. Peter was previously an Audit Manager in the Global "
      "Mining &amp; Metals practice at PwC Canada."]),

    ("Robin McWatt", "VP, Corporate Development",
     "robin-mcwatt-corporate-development-us-strategic-resources.webp",
     ["A seasoned corporate development executive with over a decade of "
      "experience in capital markets and M&amp;A advisory in metals and mining. "
      "Robin began his career as a buy-side equity analyst with Sionna "
      "Investment Managers, a Canadian institutional asset manager with over "
      "US$2 billion in AUM. He later went on to serve as Vice President at FMI "
      "Capital Advisory, a Toronto-based boutique investment bank, where he "
      "advised on various debt and equity offerings, public listings, and "
      "cross-border M&amp;A transactions."]),
]


def build_leadership():
    cards = []
    for name, role, photo, paras in PEOPLE:
        bios = "\n          ".join(f'<p class="person__bio">{p}</p>' for p in paras)
        cards.append(f"""        <article class="person">
          <div class="person__head">
            <div class="person__portrait">
              <img src="assets/team/{photo}" alt="{re.sub('&amp;', 'and', name)}"
                   width="132" height="165" loading="lazy" decoding="async">
            </div>
            <div>
              <h3 class="h5">{name}</h3>
              <div class="person__role">{role}</div>
            </div>
          </div>
          {bios}
        </article>""")

    html = head(
        f"Leadership — {BRAND}",
        "Board and management: U.S. foreign diplomacy experts and mineral "
        "exploration executives who have made discoveries and built mines "
        "across West Africa.",
        "leadership.html",
    )
    html += f"""<main id="main">

{header('leadership.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">Leadership</p>
        <h1 class="h1">Board &amp; management</h1>
      </div>
      <p class="section-head__note">A world-class team of U.S. foreign diplomacy
         experts and mineral exploration executives who have made discoveries,
         built mines, and operated across West Africa for decades.</p>
    </div>
  </div>

  <section class="section section--ink">
    <div class="wrap">
      <div class="people cards--equal">
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("leadership.html", html)


# ══════════════════════════════════════════════════════════════════════════
# metals.html — deck slides 08, 09, 10
# ══════════════════════════════════════════════════════════════════════════

CONTEXT = [
    ("Increasing demand",
     "The world is in the first phase of exponential demand growth for electric "
     "vehicles, energy storage, AI and robotics. On the IEA's Stated Policies "
     "Scenario, lithium demand more than triples and graphite demand doubles by "
     "2040, with nickel up around 65% and copper up more than 25%."),
    ("Limited supply",
     "Supply cannot respond quickly. A new mine in the U.S. takes roughly 16 "
     "years to move from discovery to production, and a decade of industry "
     "underinvestment has left the pipeline thin."),
    ("Strategic concentration",
     "Production and processing sit overwhelmingly in a handful of non-allied "
     "jurisdictions. Recent export bans on critical minerals, battery and "
     "processing technology have already turned that concentration into "
     "strategic leverage."),
]

BATTERY = [
    ("Co", "Cobalt",
     "Essential to high-performance lithium-ion batteries, giving thermal "
     "stability and longer EV range."),
    ("Cu", "Copper",
     "The backbone of electrification: grid build-out, data centers and EV "
     "wiring drive relentless demand."),
    ("Ni", "Nickel",
     "Raises battery energy density, delivering greater range at a lower cost "
     "per kWh than cobalt."),
    ("V", "Vanadium",
     "Strengthens high-performance steel and is the key input to redox flow "
     "batteries for long-duration storage."),
    ("Sn", "Tin",
     "The solder underpinning all electronics: the more the world automates, "
     "the more tin it needs."),
]

TECH = [
    ("Ga", "Gallium",
     "Used in semiconductors for high-frequency, high-power communications, "
     "radar and defense systems."),
    ("Ti", "Titanium",
     "High strength-to-weight and corrosion resistance make it critical to "
     "aerospace and defense."),
    ("Zr", "Zirconium",
     "Corrosion- and heat-resistant, and vital to nuclear fuel cladding and "
     "advanced ceramics."),
    ("Ta", "Tantalum",
     "Tantalum capacitors are central to miniaturized electronics and guided "
     "munitions."),
    ("Nb", "Niobium",
     "A micro-alloying agent that makes steel lighter and stronger, cutting "
     "material use."),
]


def metal_cards(items):
    return "".join(f'''
        <article class="metal">
          <div class="metal__sym">{pubchem_link(s)}</div>
          <div class="metal__name">{n}</div>
          <p>{d}</p>
        </article>''' for s, n, d in items)


def build_metals():
    html = head(
        f"Metals &amp; Markets — {BRAND}",
        "Technology metals are moving into a structural supply deficit. The "
        "battery, base, technology and defense metals present across the USR "
        "license areas.",
        "metals.html",
    )
    html += f"""<main id="main">

{header('metals.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">Metals &amp; markets</p>
        <h1 class="h1">Market context</h1>
      </div>
      <p class="section-head__note">Technology metals are moving into a
         structural supply deficit &mdash; a setup that favors them over the
         broader commodity complex.</p>
    </div>
  </div>

  <!-- ═══ Market context — deck slide 08 ═══ -->
  <section class="section section--ink" id="context">
    <div class="wrap">
      <dl class="rows reveal-group">
        {"".join(f'''
        <div class="row">
          <dt><span class="label row__label">{t}</span></dt>
          <dd>{v}</dd>
        </div>''' for t, v in CONTEXT)}
      </dl>
      <p class="body-xs t-quiet" style="margin-top:32px">Source: IEA, Global
         Critical Minerals Outlook &mdash; demand projections to 2040, Stated
         Policies Scenario.</p>
    </div>
  </section>

  <!-- ═══ Full-bleed duotone band ═══ -->
  <div class="band band--short duo duo--band">
    {img("earth-at-night",
         "The United States at night, seen from orbit",
         "100vw")}
    <div class="duo__content">
      <div class="wrap">
        <p class="label">Electrification</p>
        <p class="body t-soft measure" style="margin-top:12px">Grid build-out,
           data centers and EV wiring drive relentless demand.</p>
      </div>
    </div>
  </div>

  <!-- ═══ Battery & base metals — deck slide 09 ═══ -->
  <section class="section section--ink" id="battery">
    <div class="wrap">
      <div class="section-head reveal">
        <div>
          <p class="label section-head__eyebrow">Metals &amp; markets</p>
          <h2 class="h2">Metals in the USR footprint &mdash; Battery &amp; Base Metals</h2>
        </div>
        <p class="section-head__note">Battery and base metals present across the
           USR license areas. Technology and defence metals follow below.</p>
      </div>
      <div class="metals reveal-group">{metal_cards(BATTERY)}
      </div>
    </div>
  </section>

  <!-- ═══ Tech & defense metals — deck slide 10 ═══ -->
  <section class="section section--alt" id="tech">
    <div class="wrap">
      <div class="section-head reveal">
        <div>
          <p class="label section-head__eyebrow">Metals &amp; markets</p>
          <h2 class="h2">Metals in the USR footprint &mdash; Tech. &amp; Defense Metals</h2>
        </div>
        <p class="section-head__note">Technology and defense metals present
           across the USR license areas, alongside the battery and base metals
           above.</p>
      </div>
      <div class="metals reveal-group">{metal_cards(TECH)}
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("metals.html", html)


# ══════════════════════════════════════════════════════════════════════════
# news.html + the post — deck slide 11
# ══════════════════════════════════════════════════════════════════════════
def build_news():
    html = head(
        f"News — {BRAND}",
        "Announcements from U.S. Strategic Resources.",
        "news.html",
    )
    html += f"""<main id="main">

{header('news.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">News</p>
        <h1 class="h1">Featured news</h1>
      </div>
      <p class="section-head__note">Company announcements and updates from the
         license areas.</p>
    </div>
  </div>

  <section class="section section--ink">
    <div class="wrap">
      <div class="news-list reveal-group">
        <a class="news-item" href="news/company-formation-announcement.html">
          <div>
            <p class="label">Company</p>
            <p class="body-xs t-quiet mono" style="margin-top:10px">
              <span class="pending">[pending: publication date]</span></p>
          </div>
          <div>
            <h3 class="h4">Company formation announcement</h3>
            <p>U.S. Strategic Resources formed to explore for critical minerals
               and rare earths on two contiguous license areas in Nimba County,
               Liberia.</p>
            <span class="link-arrow">Read the announcement &rarr;</span>
          </div>
        </a>
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("news.html", html)

    # ---- the post -------------------------------------------------------
    post = head(
        f"Company formation announcement — {BRAND}",
        "U.S. Strategic Resources formed to explore for critical minerals and "
        "rare earths in Nimba County, Liberia.",
        "news.html",
    )
    post += f"""<main id="main">

{header('news.html')}
  <div class="page-head">
    <div class="wrap">
      <p class="label page-head__eyebrow">News &mdash; Company</p>
      <h1 class="h1" style="max-width:20ch">Company formation announcement</h1>
    </div>
  </div>

  <section class="section section--ink">
    <div class="wrap">
      <div class="article">
        <div class="article__meta">
          <div>
            <p class="label">Category</p>
            <p class="body-sm t-soft" style="margin-top:8px">Company</p>
          </div>
          <div>
            <p class="label">Date</p>
            <p class="body-sm" style="margin-top:8px"><span class="pending">[pending: month / year]</span></p>
          </div>
          <div>
            <p class="label">Source</p>
            <p class="body-sm t-soft" style="margin-top:8px">{BRAND}</p>
          </div>
        </div>

        <p class="lede t-soft">U.S. Strategic Resources has been formed to explore
           for critical minerals and rare earths on secured ground in Nimba
           County, Liberia.</p>

        <p><span class="pending">[pending: full announcement text — incorporation
           details, license references and quotes must match the approved
           release]</span></p>

        <p>The company holds two contiguous license areas in Nimba County,
           Liberia, on the gold-prospective Cestos shear zone. Prospectivity
           models are interpretive and conceptual; no mineral resource or reserve
           has been defined on either license.</p>

        <p><a class="link-arrow" href="about.html#assets">Read about the assets &rarr;</a></p>
      </div>

      <div class="subsection">
        <div class="subsection__head">
          <h2 class="h3">The asset</h2>
          <p class="label label--quiet">Nimba County, Liberia</p>
        </div>
        <figure style="margin:0;max-width:760px">
          <div class="photo ratio-3-2">
            {img("core-samples",
                 "Core samples in trays from the license areas",
                 "(max-width: 860px) 100vw, 760px")}
          </div>
          <figcaption class="figcap">
            <span class="t-lift">Full-colour accent</span>
            <span>Core samples &mdash; colour is evidence</span>
          </figcaption>
        </figure>
      </div>

      <p style="margin-top:48px">
        <a class="btn-quiet" href="news.html">&larr; All announcements</a>
      </p>
    </div>
  </section>

</main>
"""
    post += footer()
    post = rebase_srcset(rebase(post))
    write("news/company-formation-announcement.html", post)


# ══════════════════════════════════════════════════════════════════════════
# contact.html — deck slide 12
# ══════════════════════════════════════════════════════════════════════════
def build_contact():
    html = head(
        f"Contact — {BRAND}",
        "Rare earths. Prospective ground. American alignment. Speak with the "
        "U.S. Strategic Resources team.",
        "contact.html",
    )
    html += f"""<main id="main">

{header('contact.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">Rare earths &middot; Prospective ground &middot; American alignment</p>
        <h1 class="h1">Contact</h1>
      </div>
      <p class="section-head__note">For investor materials, partnership enquiries
         or media, write to the team directly.</p>
    </div>
  </div>

  <section class="section section--ink">
    <div class="wrap">
      <div class="split">
        <!-- Markup only: no backend is wired. The form opens the visitor's own
             mail client addressed to the company. -->
        <form class="form" action="mailto:{EMAIL}" method="post"
              enctype="text/plain">
          <div class="field">
            <label for="name">Name</label>
            <input id="name" name="name" type="text" placeholder="Full name" required>
          </div>
          <div class="field">
            <label for="org">Organization</label>
            <input id="org" name="organization" type="text" placeholder="Company or institution">
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" placeholder="you@organization.com" required>
          </div>
          <div class="field">
            <label for="msg">How can we help?</label>
            <textarea id="msg" name="message" rows="3"
                      placeholder="Briefly describe your objective or inquiry" required></textarea>
          </div>
          <div>
            <button class="btn btn--lg" type="submit">Send message</button>
          </div>
        </form>

        <div class="spec">
          <p class="label spec__title">Direct</p>
          <div class="spec__list">
            <div class="spec__row"><span>Email</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
            <div class="spec__row"><span>Operations</span><span>Monrovia, Liberia</span></div>
            <div class="spec__row"><span>Licenses</span><span>Nimba 1 &middot; Nimba 2</span></div>
            <div class="spec__row"><span>Stage</span><span>Exploration</span></div>
          </div>
          <p class="spec__note">This presentation and this site are for
             information purposes only; they do not constitute an offer to sell
             or a solicitation of an offer to buy any securities.</p>
        </div>
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("contact.html", html)


# ══════════════════════════════════════════════════════════════════════════
# legal.html
# ══════════════════════════════════════════════════════════════════════════
def build_legal():
    html = head(
        f"Legal — {BRAND}",
        "Legal notice, forward-looking statements and exploration-stage "
        "disclosure for U.S. Strategic Resources.",
        "legal.html",
    )
    html += f"""<main id="main">

{header('legal.html')}
  <div class="page-head">
    <div class="wrap page-head__grid">
      <div>
        <p class="label page-head__eyebrow">Legal</p>
        <h1 class="h1">Legal notice</h1>
      </div>
      <p class="section-head__note">Disclosure governing the information
         published on this site.</p>
    </div>
  </div>

  <section class="section section--ink">
    <div class="wrap">
      <div class="prose">
        <h2>No offer of securities</h2>
        <p>The information on this site is confidential and for information
           purposes only; it does not constitute an offer to sell or a
           solicitation of an offer to buy any securities.</p>

        <h2>Forward-looking statements</h2>
        <p>Forward-looking statements are subject to risks and may not be
           realized. Such statements reflect management's current expectations
           regarding future events and operating performance and speak only as of
           the date on which they are made.</p>

        <h2>Exploration stage</h2>
        <p>U.S. Strategic Resources is an exploration-stage company. No mineral
           resource or reserve has been defined on either license. Prospectivity
           models referred to on this site are interpretive and conceptual, and
           are derived from regional survey data rather than from drilling on the
           license areas.</p>

        <h2>Third-party information</h2>
        <p>Market and demand projections are attributed to the IEA Global
           Critical Minerals Outlook (demand projections to 2040, Stated Policies
           Scenario). References to neighbouring operations and to companies
           operating in Liberia are included as jurisdictional context and imply
           no relationship with, or endorsement by, those parties.</p>

        <h2>Contact</h2>
        <p>Questions regarding this notice may be directed to
           <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </div>
    </div>
  </section>

</main>
"""
    html += footer()
    write("legal.html", html)


# ══════════════════════════════════════════════════════════════════════════
# Redirect stubs at the four retired URLs
# ══════════════════════════════════════════════════════════════════════════
REDIRECTS = {
    "cestos-project.html":    ("about.html#assets", "The assets"),
    "why-liberia.html":       ("about.html#jurisdiction", "Jurisdiction"),
    "critical-minerals.html": ("metals.html", "Metals &amp; Markets"),
    "company.html":           ("leadership.html", "Leadership"),
}


def build_redirects():
    for src, (dest, label) in REDIRECTS.items():
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved &mdash; {BRAND}</title>
<link rel="canonical" href="{dest}">
<meta http-equiv="refresh" content="0; url={dest}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="assets/logo/favicon-USR-new.svg">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
  <main id="main" class="section section--ink" style="min-height:60vh">
    <div class="wrap">
      <p class="label">This page has moved</p>
      <p class="body t-soft" style="margin-top:16px">Redirecting to
         <a href="{dest}">{label}</a>.</p>
    </div>
  </main>
</body>
</html>
"""
        write(src, html)


if __name__ == "__main__":
    print("Building site/ …")
    build_index()
    build_about()
    build_leadership()
    build_metals()
    build_news()
    build_contact()
    build_legal()
    build_redirects()
    print("Done.")
