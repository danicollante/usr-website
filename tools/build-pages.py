#!/usr/bin/env python3
"""One-off generator for the six pages that had no design reference.

This is process tooling, NOT a build step: it writes plain .html files into
site/ once, and those files are the deliverable. Header/footer markup is
lifted verbatim from the two hand-built reference pages so the shared chrome
is identical across all eight pages. Edit the HTML directly from here on.
"""
import os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

HEADER = re.search(r'( *<header class="site-header">.*?</header>)', home, re.S).group(1)
FOOTER = re.search(r'( *<footer class="site-footer">.*?</footer>)', home, re.S).group(1)

def header_for(page):
    """Move the current-page marker to `page`, in BOTH navs.

    The header carries two navigations: the desktop bar (.nav) and the
    <details class="nav-mobile"> menu that replaces it at <=1023px. Both need
    the marker, or the current page is unmarked on every small screen.
    """
    h = HEADER.replace(' nav__link--current', '').replace(' aria-current="page"', '')
    # desktop bar
    h = h.replace(f'<a class="nav__link" href="{page}">',
                  f'<a class="nav__link nav__link--current" href="{page}" aria-current="page">')
    # mobile menu panel — plain <a href> with no class
    h = h.replace(f'<a href="{page}">', f'<a href="{page}" aria-current="page">')
    return h

ORG_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "{{SITE_URL}}/#organization",
  "name": "U.S. Strategic Resources",
  "alternateName": "USR",
  "url": "{{SITE_URL}}/",
  "logo": "{{SITE_URL}}/assets/logo/usr-logo-black.png",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Monrovia",
    "addressCountry": "LR"
  }
}
</script>'''

def breadcrumb_schema(name):
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "{{SITE_URL}}/" },
    { "@type": "ListItem", "position": 2, "name": "%s" }
  ]
}
</script>''' % name.replace('&amp;', '&')

def breadcrumb(name):
    return f'''  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="index.html">Home</a> /</li>
      <li><span aria-current="page">{name}</span></li>
    </ol>
  </nav>'''

def descend(markup):
    """Rewrite root-relative chrome for a page one directory down."""
    markup = re.sub(r'href="(?!https?:|mailto:|#)([^"]+\.html)"', r'href="../\1"', markup)
    markup = markup.replace('src="assets/', 'src="../assets/')
    return markup


def page(file, slug, title, description, crumb, nav, schemas, body, og_type='article',
         crumbs=None, prefix='', crumb_trail=None):
    extra = '\n\n'.join([ORG_SCHEMA, crumbs or breadcrumb_schema(crumb)] + schemas)
    chrome_header = header_for(nav)
    chrome_footer = FOOTER
    crumb_markup = crumb_trail or breadcrumb(crumb)
    if prefix:
        chrome_header = descend(chrome_header)
        chrome_footer = descend(chrome_footer)
        crumb_markup = descend(crumb_markup)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- SEO — content map §2. noindex until launch; {{{{SITE_URL}}}} = production domain. -->
<meta name="robots" content="noindex, nofollow">

<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{{{{SITE_URL}}}}/{slug}">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="U.S. Strategic Resources">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{{{{SITE_URL}}}}/{slug}">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="{prefix}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Libre+Franklin:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">

{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="page">

{chrome_header}

{crumb_markup}

  <main id="main">

{body}

  </main>

{chrome_footer}

</div>
</body>
</html>
'''
    out = os.path.join(ROOT, file)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', file)


# ============================================================ COMPANY

PERSON_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "name": "David Kol",
      "jobTitle": "Chief Executive Officer & Board Member",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" }
    },
    {
      "@type": "Person",
      "name": "Peter Granata",
      "honorificSuffix": "CA",
      "jobTitle": "Chief Financial Officer",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" }
    },
    {
      "@type": "Person",
      "name": "Robin McWatt",
      "jobTitle": "Corporate Development",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" }
    },
    {
      "@type": "Person",
      "name": "Brett Richards",
      "jobTitle": "Board Member",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" }
    },
    {
      "@type": "Person",
      "name": "David Bellon",
      "honorificPrefix": "Lt. Gen. (Ret.)",
      "jobTitle": "Board Member",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" }
    }
  ]
}
</script>'''

company_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Company</p>
          <h1>Purpose-built. Independent. One mandate.</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Structure</dt><dd class="facts__value">Standalone company</dd></div>
          <div class="facts__row"><dt class="facts__term">Incorporated</dt><dd class="facts__value pending">[pending]</dd></div>
          <div class="facts__row"><dt class="facts__term">Headquarters</dt><dd class="facts__value pending">[pending]</dd></div>
          <div class="facts__row"><dt class="facts__term">Operations</dt><dd class="facts__value">Monrovia, Liberia</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 intro + takeaways -->
    <section class="section-indexed">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <p class="lead">U.S. Strategic Resources was founded as a standalone company with a single mandate: prove and deliver U.S.-aligned critical mineral supply from West Africa&rsquo;s most underexplored terrane. The company combines an experienced in-country operating platform in Liberia with leadership drawn from capital markets, African mining operations and the U.S. defence establishment.</p>
            <a class="btn btn--accent" href="contact.html">Request the investor presentation &rarr;</a>
          </div>
          <div class="stack">
            <p class="label mb-32">Key takeaways</p>
            <div class="takeaways takeaways--compact">
              <div class="takeaways__item">
                <span class="takeaways__n">01</span>
                <p class="takeaways__text">Standalone company, independent of any parent group.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">02</span>
                <p class="takeaways__text">Operations base in Monrovia, Liberia. <span class="pending">[pending: HQ city, jurisdiction and incorporation date]</span></p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">03</span>
                <p class="takeaways__text">Board and management with 100+ combined years across mining, finance and defence.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 02 the company -->
    <section class="section-indexed">
      <div class="section-indexed__rail">02</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">The company</h2>
        <div class="grid-2">
          <p class="lead">One asset base. One flag. Built to move at the speed of the federal window.</p>
          <dl class="list">
            <div class="list__item">
              <dt class="list__term">Incorporated</dt>
              <dd class="pending">[pending: jurisdiction and date]</dd>
            </div>
            <div class="list__item">
              <dt class="list__term">Headquarters</dt>
              <dd class="pending">[pending: HQ city]</dd>
            </div>
            <div class="list__item">
              <dt class="list__term">Operations</dt>
              <dd>Monrovia, Liberia</dd>
            </div>
          </dl>
        </div>
      </div>
    </section>

    <!-- 03 leadership -->
    <section class="section-indexed">
      <div class="section-indexed__rail">03</div>
      <div class="section-indexed__body">
        <h2 class="mb-40">Leadership</h2>
        <!-- .grid-3 becomes a ruled list of horizontal .person rows at <=1023px
             (§11.2) — no markup change. When real headshots arrive they replace
             the .placeholder--portrait blocks; portraits are not zoomable. -->
        <div class="grid-3">
          <div class="person">
            <div class="placeholder placeholder--portrait">david-kol-ceo-us-strategic-resources.webp<br>[ headshot pending ]</div>
            <div>
              <h3 class="person__name">David Kol</h3>
              <div class="person__role">Chief Executive Officer &amp; Board Member</div>
              <p class="person__bio">David Kol brings more than 20 years in capital markets and M&amp;A, including 17+ years operating in West Africa. He is the founder and CEO of Zodiac Gold (TSXV: ZAU), an exploration company advancing a district-scale gold project in Liberia.</p>
            </div>
          </div>
          <div class="person">
            <div class="placeholder placeholder--portrait">peter-granata-cfo-us-strategic-resources.webp<br>[ headshot pending ]</div>
            <div>
              <h3 class="person__name">Peter Granata, CA</h3>
              <div class="person__role">Chief Financial Officer</div>
              <p class="person__bio">Peter Granata has spent 18+ years in African natural resources. A former audit manager in PwC&rsquo;s Global Mining &amp; Metals practice, he has served as CFO across multiple TSXV-listed issuers.</p>
            </div>
          </div>
          <div class="person">
            <div class="placeholder placeholder--portrait">robin-mcwatt-corporate-development-us-strategic-resources.webp<br>[ headshot pending ]</div>
            <div>
              <h3 class="person__name">Robin McWatt</h3>
              <div class="person__role">Corporate Development</div>
              <p class="person__bio">Robin McWatt has over a decade of experience in capital markets and M&amp;A advisory, including roles as Vice President at FMI Capital Advisory and analyst at Sionna.</p>
            </div>
          </div>
        </div>

        <div class="grid-2 block-ruled mt-56">
          <h3>Head of Exploration &mdash; search underway</h3>
          <p class="body">Target profile: a chartered geologist with a West African greenstone gold and critical-minerals field record. Technical and government-affairs advisory appointments to be announced.</p>
        </div>
      </div>
    </section>

    <!-- 04 board -->
    <section class="section-indexed">
      <div class="section-indexed__rail">04</div>
      <div class="section-indexed__body">
        <h2 class="mb-40">Board of Directors</h2>
        <div class="grid-3">
          <div class="person">
            <div class="placeholder placeholder--portrait">brett-richards-board-us-strategic-resources.webp<br>[ headshot pending ]</div>
            <div>
              <h3 class="person__name">Brett Richards</h3>
              <div class="person__role">Board Member</div>
              <p class="person__bio">A 40-year mining executive who has built three mines in Africa. Former CEO of Katanga Mining and Avocet plc.</p>
            </div>
          </div>
          <div class="person">
            <div class="placeholder placeholder--portrait">david-bellon-board-us-strategic-resources.webp<br>[ headshot pending ]</div>
            <div>
              <h3 class="person__name">Lt. Gen. David Bellon (Ret.)</h3>
              <div class="person__role">Board Member</div>
              <p class="person__bio">A 35-year career in the United States Marine Corps, including command of Marine Forces South and the Marine Corps Reserve.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- closing CTA -->
    <section class="cta-band">
      <h2 class="h2--statement measure-24">One asset base. One flag.</h2>
      <div class="btn-row">
        <a class="btn btn--primary" href="cestos-project.html">See the asset &rarr;</a>
        <a class="btn btn--ghost" href="contact.html">Speak with the team &rarr;</a>
      </div>
    </section>'''

page(
    file='company.html', slug='company',
    title='About U.S. Strategic Resources | Team &amp; Leadership',
    description='Purpose-built and independent. Meet the team behind U.S. Strategic Resources — capital markets, African mining operations and U.S. defence experience.',
    crumb='Company', nav='company.html',
    schemas=[PERSON_SCHEMA], body=company_body)


# ============================================================ WHY LIBERIA

why_liberia_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Jurisdiction</p>
          <h1>Why we operate in Liberia</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Terrane</dt><dd class="facts__value">Birimian-age, underexplored</dd></div>
          <div class="facts__row"><dt class="facts__term">Structure</dt><dd class="facts__value">Cestos shear zone</dd></div>
          <div class="facts__row"><dt class="facts__term">National survey</dt><dd class="facts__value">69 elements, countrywide</dd></div>
          <div class="facts__row"><dt class="facts__term">Operating base</dt><dd class="facts__value">Monrovia</dd></div>
          <div class="facts__row"><dt class="facts__term">Mobilization</dt><dd class="facts__value">Zero lead time</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 intro + takeaways -->
    <section class="section-indexed">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <p class="lead">Liberia hosts one of West Africa&rsquo;s most underexplored terranes &mdash; Birimian-age geology on trend with some of the region&rsquo;s largest gold discoveries, yet with a fraction of the drilling. The government&rsquo;s national geochemical survey gives explorers a data foundation that most frontier jurisdictions lack. U.S. Strategic Resources operates here through an established platform built over years of in-country work.</p>
            <a class="btn btn--accent" href="cestos-project.html">See the project &rarr;</a>
          </div>
          <div class="stack">
            <p class="label mb-32">Key takeaways</p>
            <div class="takeaways takeaways--compact">
              <div class="takeaways__item">
                <span class="takeaways__n">01</span>
                <p class="takeaways__text">Underexplored geology on the Cestos shear zone, west of the Ity gold mine.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">02</span>
                <p class="takeaways__text">National survey: 69 elements analysed countrywide &mdash; rare data depth for a frontier jurisdiction.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">03</span>
                <p class="takeaways__text">Established Monrovia operating base; zero mobilization lead time.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 02 the operating platform -->
    <section class="section-indexed">
      <div class="section-indexed__rail">02</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">The operating platform</h2>
        <dl class="list">
          <div class="list__item">
            <dt class="list__term">Monrovia office</dt>
            <dd>Established base with logistics, procurement and administration in place.</dd>
          </div>
          <div class="list__item">
            <dt class="list__term">Field teams</dt>
            <dd>Geologists and crews with seasons of terrane-specific fieldwork.</dd>
          </div>
          <div class="list__item">
            <dt class="list__term">Drill operations</dt>
            <dd>Drilling capability and contractor relationships ready to mobilize.</dd>
          </div>
          <div class="list__item">
            <dt class="list__term">Drone &amp; geophysics</dt>
            <dd>Survey capability for rapid, low-cost target refinement.</dd>
          </div>
          <div class="list__item">
            <dt class="list__term">Government access</dt>
            <dd>Working relationships with the Ministry of Mines &amp; Energy and regulators.</dd>
          </div>
          <div class="list__item">
            <dt class="list__term">Community trust</dt>
            <dd>Long-standing local relationships and social licence to operate.</dd>
          </div>
        </dl>

        <!-- Media pair: stacks at tablet. When the real photography lands,
             swap each .placeholder for an <img> wrapped in the
             zoomable/lightbox unit (see §07 of style.css) with page-unique
             ids — lb-why-fig1 / lb-why-fig2. A lightbox is not wired now
             because there is no image to enlarge, only a hatched block. -->
        <div class="grid-2 grid-2--media mt-56">
          <div class="stack-12">
            <div class="placeholder placeholder--tall">monrovia-liberia-operations-base.webp<br>[ U.S. Strategic Resources operations base in Monrovia, Liberia &mdash; photography pending from USR ]</div>
            <span class="note">Photography: bleeds to the column edge, caption optional.</span>
          </div>
          <div class="stack-12">
            <div class="placeholder placeholder--tall">liberia-field-team-sampling.webp<br>[ field geologists conducting soil sampling in Nimba County, Liberia &mdash; photography pending from USR ]</div>
            <span class="note">Photography: bleeds to the column edge, caption optional.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 03 community & responsibility -->
    <!-- Flagged to USR: this should grow into a standalone ESG page — sector
         standard, and Zodiac has one. Kept as one short section for now. -->
    <section class="section-indexed">
      <div class="section-indexed__rail">03</div>
      <div class="section-indexed__body">
        <div class="grid-2-wide">
          <h2>Community &amp; responsibility</h2>
          <div class="stack-24">
            <p class="lead"><span class="pending">[pending: community programs, environmental commitments, local employment figures]</span></p>
            <a class="link" href="contact.html">Contact the team &rarr;</a>
          </div>
        </div>
      </div>
    </section>

    <!-- closing CTA -->
    <section class="cta-band">
      <h2 class="h2--statement measure-24">One of West Africa&rsquo;s most underexplored terranes.</h2>
      <div class="btn-row">
        <a class="btn btn--primary" href="critical-minerals.html">The market case &rarr;</a>
        <a class="btn btn--ghost" href="contact.html">Contact the team &rarr;</a>
      </div>
    </section>'''

page(
    file='why-liberia.html', slug='why-liberia',
    title='Why Liberia | Mining Exploration in West Africa',
    description='Underexplored terrane, national survey data and an established in-country platform: the case for critical minerals exploration in Liberia, West Africa.',
    crumb='Why Liberia', nav='why-liberia.html',
    schemas=[], body=why_liberia_body)


# ============================================================ CRITICAL MINERALS

CM_FAQ_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What are critical minerals?",
      "acceptedAnswer": { "@type": "Answer", "text": "Minerals designated essential to economic and national security — including rare earths, battery metals like lithium and cobalt, and technology metals like gallium — where supply is concentrated or at risk." }
    },
    {
      "@type": "Question",
      "name": "Why does Chinese export control matter?",
      "acceptedAnswer": { "@type": "Answer", "text": "With ~90% of rare-earth refining and 98% of refined gallium and germanium, export licences effectively decide which countries can build magnets, semiconductors and defence systems." }
    },
    {
      "@type": "Question",
      "name": "What is Project Vault?",
      "acceptedAnswer": { "@type": "Answer", "text": "A $12B U.S. national critical-minerals stockpile that creates a standing federal buyer for strategic supply." }
    },
    {
      "@type": "Question",
      "name": "How does U.S. Strategic Resources access federal funding?",
      "acceptedAnswer": { "@type": "Answer", "text": "Through six parallel channels open to companies proving supply on allied ground — from State Department programs to DFC equity and USTDA technical grants." }
    }
  ]
}
</script>'''

critical_minerals_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Market thesis</p>
          <h1>The case for U.S.-aligned critical mineral supply</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Rare-earth refining, China</dt><dd class="facts__value">~90%</dd></div>
          <div class="facts__row"><dt class="facts__term">Refined Ga and Ge</dt><dd class="facts__value">98%</dd></div>
          <div class="facts__row"><dt class="facts__term">REEs export-controlled</dt><dd class="facts__value">7, since April 2025</dd></div>
          <div class="facts__row"><dt class="facts__term">U.S. capital deployed</dt><dd class="facts__value">$30B+</dd></div>
          <div class="facts__row"><dt class="facts__term">Federal funding channels</dt><dd class="facts__value">Six, in parallel</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 intro + takeaways -->
    <section class="section-indexed">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <p class="lead">Roughly 90% of global rare-earth refining capacity runs through China &mdash; end-to-end leverage from mine to magnet &mdash; along with 98% of refined gallium and germanium, the backbone of semiconductors and defence electronics. Since April 2025, seven rare earths, including samarium, sit under Chinese export controls. Export licences now decide who builds. The United States is deploying capital to change that.</p>
            <a class="btn btn--accent" href="cestos-project.html">See how the project fits &rarr;</a>
          </div>
          <div class="stack">
            <p class="label mb-32">Key takeaways</p>
            <div class="takeaways takeaways--compact">
              <div class="takeaways__item">
                <span class="takeaways__n">01</span>
                <p class="takeaways__text">Five executive orders on minerals security: direct equity, price floors and offtake authorities now in force.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">02</span>
                <p class="takeaways__text">$30B+ in U.S. government capital deployed across equity stakes, loans and stockpiling.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">03</span>
                <p class="takeaways__text">Project Vault: a $12B national critical-minerals stockpile &mdash; a standing federal buyer.</p>
              </div>
              <div class="takeaways__item">
                <span class="takeaways__n">04</span>
                <p class="takeaways__text">$500M U.S.&ndash;Africa Strategic Investment Program, Critical Minerals as Focus Area 1; $5&ndash;50M per award.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 02 the problem — concentration -->
    <section class="section-indexed band-dark">
      <div class="section-indexed__rail">02</div>
      <div class="section-indexed__body">
        <div class="grid-2-wide">
          <h2 class="h2--statement">The problem &mdash; concentration</h2>
          <div class="stack-28">
            <p class="lead lead--dark"><span class="pending">[pending: two short paragraphs on supply concentration &mdash; content map &sect;3.5]</span></p>
            <div class="stats stats--3">
              <div><div class="stats__figure">90%</div><div class="stats__label">rare-earth refining, China</div></div>
              <div><div class="stats__figure">98%</div><div class="stats__label">refined Ga and Ge</div></div>
              <div><div class="stats__figure">7</div><div class="stats__label">REEs export-controlled</div></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 03 the moment — the federal window -->
    <section class="section-indexed">
      <div class="section-indexed__rail">03</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">The moment &mdash; the federal window</h2>
        <p class="lead measure-64"><span class="pending">[pending: two paragraphs &mdash; executive orders, FORGE and the 54-nation Ministerial, Project Vault, the U.S.&ndash;Africa program. Content map &sect;3.5]</span></p>
        <div class="mt-56">
          <div class="stats stats--light">
            <div><div class="stats__figure">5</div><div class="stats__label">executive orders on minerals security</div></div>
            <div><div class="stats__figure">$30B+</div><div class="stats__label">U.S. capital deployed to date</div></div>
            <div><div class="stats__figure">$12B</div><div class="stats__label">Project Vault stockpile</div></div>
            <div><div class="stats__figure">$500M</div><div class="stats__label">U.S.&ndash;Africa Strategic Investment Program</div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 04 demand outruns supply -->
    <section class="section-indexed">
      <div class="section-indexed__rail">04</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">Demand outruns supply</h2>
        <table class="table">
          <thead>
            <tr>
              <th class="col-30" scope="col">Signal</th>
              <th class="col-24" scope="col">Figure</th>
              <th scope="col">Source</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="table__lead" data-label="Signal">Lithium demand by 2040</td>
              <td class="table__data" data-label="Figure">3&times;</td>
              <td data-label="Source">IEA projection</td>
            </tr>
            <tr>
              <td class="table__lead" data-label="Signal">Copper deficit, 2026</td>
              <td class="table__data" data-label="Figure">150&ndash;330 kt</td>
              <td data-label="Source">Structural shortfall forecast</td>
            </tr>
            <tr>
              <td class="table__lead" data-label="Signal">Federal stockpile buying</td>
              <td class="table__data" data-label="Figure">$12B</td>
              <td data-label="Source">Project Vault</td>
            </tr>
            <tr>
              <td class="table__lead" data-label="Signal">Permanent-magnet market by 2030</td>
              <td class="table__data" data-label="Figure">$30B</td>
              <td data-label="Source">MarketsandMarkets (~$22B in 2025, 6.4% CAGR)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 05 business model -->
    <section class="section-indexed">
      <div class="section-indexed__rail">05</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">Business model &mdash; explore, prove, partner, deliver</h2>
        <div class="steps">
          <div class="steps__item">
            <span class="steps__n">01</span>
            <div>
              <div class="steps__title">Explore</div>
              <p class="steps__text pending">[pending: one sentence &mdash; deck slide 11]</p>
            </div>
          </div>
          <div class="steps__item">
            <span class="steps__n">02</span>
            <div>
              <div class="steps__title">Prove</div>
              <p class="steps__text pending">[pending: one sentence &mdash; deck slide 11]</p>
            </div>
          </div>
          <div class="steps__item">
            <span class="steps__n">03</span>
            <div>
              <div class="steps__title">Partner</div>
              <p class="steps__text pending">[pending: one sentence &mdash; deck slide 11]</p>
            </div>
          </div>
          <div class="steps__item">
            <span class="steps__n">04</span>
            <div>
              <div class="steps__title">Deliver</div>
              <p class="steps__text pending">[pending: one sentence &mdash; deck slide 11]</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 06 federal funding channels -->
    <section class="section-indexed">
      <div class="section-indexed__rail">06</div>
      <div class="section-indexed__body">
        <div class="grid-2-wide">
          <h2>Federal funding channels</h2>
          <div class="stack-24">
            <p class="lead">Six channels pursued in parallel: State Department APS programs (the lead vehicle), DFC development finance, EXIM supply-chain facilities, USTDA feasibility grants, DoD industrial-base programs, and the 54-nation FORGE platform. Precedent transactions show juniors on allied ground getting funded.</p>
            <span class="note">No application-status detail is published on this site.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 07 faq -->
    <section class="section-indexed">
      <div class="section-indexed__rail">07</div>
      <div class="section-indexed__body">
        <h2 class="mb-32">Frequently asked questions</h2>
        <div class="faq">
          <details class="faq__item" name="faq" open>
            <summary class="faq__summary">
              <span class="faq__index">Q1</span>
              <span class="faq__question">What are critical minerals?</span>
              <span class="faq__toggle" aria-hidden="true"></span>
            </summary>
            <div class="faq__answer"><p>Minerals designated essential to economic and national security &mdash; including rare earths, battery metals like lithium and cobalt, and technology metals like gallium &mdash; where supply is concentrated or at risk.</p></div>
          </details>

          <details class="faq__item" name="faq">
            <summary class="faq__summary">
              <span class="faq__index">Q2</span>
              <span class="faq__question">Why does Chinese export control matter?</span>
              <span class="faq__toggle" aria-hidden="true"></span>
            </summary>
            <div class="faq__answer"><p>With ~90% of rare-earth refining and 98% of refined gallium and germanium, export licences effectively decide which countries can build magnets, semiconductors and defence systems.</p></div>
          </details>

          <details class="faq__item" name="faq">
            <summary class="faq__summary">
              <span class="faq__index">Q3</span>
              <span class="faq__question">What is Project Vault?</span>
              <span class="faq__toggle" aria-hidden="true"></span>
            </summary>
            <div class="faq__answer"><p>A $12B U.S. national critical-minerals stockpile that creates a standing federal buyer for strategic supply.</p></div>
          </details>

          <details class="faq__item" name="faq">
            <summary class="faq__summary">
              <span class="faq__index">Q4</span>
              <span class="faq__question">How does U.S. Strategic Resources access federal funding?</span>
              <span class="faq__toggle" aria-hidden="true"></span>
            </summary>
            <div class="faq__answer"><p>Through six parallel channels open to companies proving supply on allied ground &mdash; from State Department programs to DFC equity and USTDA technical grants.</p></div>
          </details>
        </div>
      </div>
    </section>

    <!-- closing CTA -->
    <section class="cta-band">
      <h2 class="h2--statement measure-24">Export licences now decide who builds.</h2>
      <div class="btn-row">
        <a class="btn btn--primary" href="cestos-project.html">The asset &rarr;</a>
        <a class="btn btn--ghost" href="contact.html">Request the investor presentation &rarr;</a>
      </div>
    </section>'''

page(
    file='critical-minerals.html', slug='critical-minerals',
    title='Critical Minerals Supply Gap &amp; U.S. Federal Funding',
    description='China refines ~90% of rare earths. Washington has deployed $30B+ to change that. How U.S. Strategic Resources is positioned for the federal funding window.',
    crumb='Critical Minerals &amp; Strategy', nav='critical-minerals.html',
    schemas=[CM_FAQ_SCHEMA], body=critical_minerals_body)


# ============================================================ NEWS

NEWS_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "News & announcements",
  "url": "{{SITE_URL}}/news",
  "isPartOf": { "@id": "{{SITE_URL}}/#organization" }
}
</script>'''

news_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Newsroom</p>
          <h1>News &amp; announcements</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Published</dt><dd class="facts__value">1 announcement</dd></div>
          <div class="facts__row"><dt class="facts__term">Categories</dt><dd class="facts__value">Company &middot; Exploration &middot; Media</dd></div>
          <div class="facts__row"><dt class="facts__term">Media enquiries</dt><dd class="facts__value pending">[pending]</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 announcements -->
    <!-- Post template notes for the WordPress build:
         · post URLs are /news/{slug} — no dates or numbers in slugs. Each post
           is its own indexable page (NewsArticle schema, share links, in-body
           link back to /cestos-project). Never a modal or an accordion.
         · the category tabs below become links to /news/category/{slug}.
           They are inactive in the static build because no category archive
           exists as a flat file.
         · paginated archives (/news/page/2 and beyond) must be noindex. -->
    <section class="section-indexed">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <nav class="tabs" aria-label="Filter announcements by category">
          <a class="tabs__tab tabs__tab--current" href="news.html" aria-current="page">All</a>
          <span class="tabs__tab" aria-disabled="true">Company</span>
          <span class="tabs__tab" aria-disabled="true">Exploration</span>
          <span class="tabs__tab" aria-disabled="true">Media</span>
          <span class="tabs__count">1 of 1</span>
        </nav>

        <div class="post-list">
          <article class="post">
            <div class="post__meta">
              <span class="post__category">Company</span>
              <span class="post__date pending">[pending: month / year]</span>
              <span class="post__source">Source: U.S. Strategic Resources</span>
            </div>
            <div>
              <h2 class="post__title"><a href="news/company-formation-announcement.html">Company formation announcement</a></h2>
              <p class="post__excerpt">U.S. Strategic Resources formed to prove critical mineral supply on secured ground in Liberia.</p>
            </div>
          </article>
        </div>

        <nav class="pagination" aria-label="Pagination">
          <span class="pagination__step" aria-disabled="true">&larr; Previous</span>
          <span class="pagination__page pagination__page--current" aria-current="page">1</span>
          <span class="pagination__step" aria-disabled="true">Next &rarr;</span>
        </nav>

        <div class="grid-2 block-ruled mt-56">
          <div class="stack-16">
            <h2>Subscribe</h2>
            <p class="body body--small">Announcements will be published here. Subscribe for updates.</p>
          </div>
          <form class="subscribe" action="{{FORM_ENDPOINT}}" method="post">
            <label class="visually-hidden" for="subscribe-email">Email address</label>
            <input class="field__input" id="subscribe-email" name="email" type="email" placeholder="email address" required>
            <button class="btn btn--primary" type="submit">Subscribe</button>
          </form>
        </div>
      </div>
    </section>

    <!-- closing CTA -->
    <section class="cta-band">
      <h2 class="h2--statement measure-24">Speak with the team</h2>
      <div class="btn-row">
        <a class="btn btn--primary" href="contact.html">Request the investor presentation &rarr;</a>
        <a class="btn btn--ghost" href="cestos-project.html">The asset &rarr;</a>
      </div>
    </section>'''

page(
    file='news.html', slug='news',
    title='News &amp; Announcements | U.S. Strategic Resources',
    description='Company announcements, exploration updates and media coverage from U.S. Strategic Resources.',
    crumb='News', nav='news.html',
    schemas=[NEWS_SCHEMA], body=news_body)


# ============================================================ CONTACT

CONTACT_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Contact U.S. Strategic Resources",
  "url": "{{SITE_URL}}/contact",
  "isPartOf": { "@id": "{{SITE_URL}}/#organization" }
}
</script>'''

contact_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Contact</p>
          <h1>Speak with the team</h1>
          <p class="subline">Investor enquiries, partnership discussions and media requests.</p>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Operations</dt><dd class="facts__value">Monrovia, Liberia</dd></div>
          <div class="facts__row"><dt class="facts__term">Headquarters</dt><dd class="facts__value pending">[pending]</dd></div>
          <div class="facts__row"><dt class="facts__term">Email</dt><dd class="facts__value pending">[pending]</dd></div>
          <div class="facts__row"><dt class="facts__term">Phone</dt><dd class="facts__value pending">[pending]</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 enquiry form -->
    <section class="section-indexed">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <h2>Send an enquiry</h2>
            <p class="body">Tell us which kind of enquiry this is and the team will route it. Investor materials are shared on request.</p>
          </div>
          <!-- Wire `action` to the Formspree / Netlify Forms endpoint before
               launch: {{FORM_ENDPOINT}} is a placeholder token, not a URL. -->
          <form class="form" action="{{FORM_ENDPOINT}}" method="post">
            <div class="form__row">
              <div class="field">
                <label class="field__label" for="name">Name</label>
                <input class="field__input" id="name" name="name" type="text" autocomplete="name" required>
              </div>
              <div class="field">
                <label class="field__label" for="organization">Organization</label>
                <input class="field__input" id="organization" name="organization" type="text" autocomplete="organization">
              </div>
            </div>
            <div class="form__row">
              <div class="field">
                <label class="field__label" for="email">Email</label>
                <input class="field__input" id="email" name="email" type="email" autocomplete="email" required>
              </div>
              <div class="field">
                <label class="field__label" for="enquiry-type">Enquiry type</label>
                <select class="field__select" id="enquiry-type" name="enquiry_type" required>
                  <option value="investor">Investor</option>
                  <option value="partner">Partner</option>
                  <option value="media">Media</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label class="field__label" for="message">Message</label>
              <textarea class="field__textarea" id="message" name="message" required></textarea>
            </div>
            <button class="btn btn--primary form__submit" type="submit">Send enquiry &rarr;</button>
          </form>
        </div>
      </div>
    </section>

    <!-- 02 details -->
    <section class="section-indexed section-indexed--last">
      <div class="section-indexed__rail">02</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <h2>Where we are</h2>
            <dl class="list">
              <div class="list__item">
                <dt class="list__term">Operations</dt>
                <dd>Monrovia, Liberia</dd>
              </div>
              <div class="list__item">
                <dt class="list__term">Headquarters</dt>
                <dd class="pending">[pending: HQ address]</dd>
              </div>
              <div class="list__item">
                <dt class="list__term">Email</dt>
                <dd class="pending">[pending]</dd>
              </div>
              <div class="list__item">
                <dt class="list__term">Phone</dt>
                <dd class="pending">[pending]</dd>
              </div>
            </dl>
          </div>
          <div class="stack-24">
            <h2>Newsletter</h2>
            <p class="body">Announcements and exploration updates, sent as they are published.</p>
            <form class="subscribe" action="{{FORM_ENDPOINT}}" method="post">
              <label class="visually-hidden" for="subscribe-email">Email address</label>
              <input class="field__input" id="subscribe-email" name="email" type="email" placeholder="email address" required>
              <button class="btn btn--primary" type="submit">Subscribe</button>
            </form>
          </div>
        </div>
      </div>
    </section>'''

page(
    file='contact.html', slug='contact',
    title='Contact U.S. Strategic Resources',
    description='Reach the U.S. Strategic Resources team — investor enquiries, partnership discussions and media requests.',
    crumb='Contact', nav='contact.html',
    schemas=[CONTACT_SCHEMA], body=contact_body)


# ============================================================ LEGAL

legal_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Legal</p>
          <h1>Legal notice &amp; forward-looking statements</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Last reviewed</dt><dd class="facts__value pending">[pending]</dd></div>
          <div class="facts__row"><dt class="facts__term">Counsel review</dt><dd class="facts__value pending">[pending]</dd></div>
        </dl>
      </div>
    </section>

    <!-- 01 notices -->
    <section class="section-indexed section-indexed--last">
      <div class="section-indexed__rail">01</div>
      <div class="section-indexed__body">
        <div class="grid-2">
          <div class="stack-24">
            <h2>Notices</h2>
            <p class="body body--measure"><span class="pending">[pending: legal review by USR counsel &mdash; the text on this page is the deck disclaimer expanded and must be approved before launch.]</span></p>
          </div>
          <div class="stack-32">
            <div class="stack-12">
              <h3>No offer of securities</h3>
              <p class="body body--measure">Nothing on this website constitutes an offer to sell or a solicitation of an offer to buy any securities.</p>
            </div>
            <div class="stack-12">
              <h3>Forward-looking statements</h3>
              <p class="body body--measure">This website contains forward-looking statements. Forward-looking statements involve risks and uncertainties, and actual results may differ materially from those expressed or implied.</p>
            </div>
            <div class="stack-12">
              <h3>Exploration results</h3>
              <p class="body body--measure">Exploration results are preliminary and subject to verification. Information on this website is subject to verification and may be updated without notice.</p>
            </div>
            <div class="stack-12">
              <h3>Website terms of use</h3>
              <p class="body body--measure"><span class="pending">[pending: terms of use &mdash; drafted by USR counsel]</span></p>
            </div>
            <div class="stack-12">
              <h3>Privacy &amp; analytics</h3>
              <p class="body body--measure"><span class="pending">[pending: privacy note and cookie/analytics disclosure &mdash; required once GA4 is live]</span></p>
            </div>
          </div>
        </div>
      </div>
    </section>'''

page(
    file='legal.html', slug='legal',
    title='Legal Notice &amp; Disclaimer | U.S. Strategic Resources',
    description='Legal notice, forward-looking statements and disclaimer for the U.S. Strategic Resources website.',
    crumb='Legal &amp; Disclaimer', nav='legal.html',
    schemas=[], body=legal_body)


# ============================================================ NEWS POST (example)
# One real post page so the design system can be checked at article level, not
# just in the listing. URL target is /news/company-formation-announcement.

POST_URL = '{{SITE_URL}}/news/company-formation-announcement'
POST_TITLE = 'Company formation announcement'
POST_EXCERPT = ('U.S. Strategic Resources formed to prove critical mineral supply '
                'on secured ground in Liberia.')

post_crumbs = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "{{SITE_URL}}/" },
    { "@type": "ListItem", "position": 2, "name": "News", "item": "{{SITE_URL}}/news" },
    { "@type": "ListItem", "position": 3, "name": "%s" }
  ]
}
</script>''' % POST_TITLE

# datePublished / dateModified are deliberately absent: the date is still
# [pending] and a fabricated one would be published as machine-readable fact.
# Add both properties at the same time as the on-page date.
POST_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "%s",
  "description": "%s",
  "articleSection": "Company",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "%s" },
  "url": "%s",
  "author": { "@id": "{{SITE_URL}}/#organization" },
  "publisher": { "@id": "{{SITE_URL}}/#organization" }
}
</script>''' % (POST_TITLE, POST_EXCERPT, POST_URL, POST_URL)

post_body = '''    <!-- hero -->
    <section class="hero hero--inner">
      <div class="grid-hero">
        <div class="stack-28">
          <p class="label">Company</p>
          <h1 class="h1--article">Company formation announcement</h1>
        </div>
        <dl class="facts">
          <div class="facts__row"><dt class="facts__term">Category</dt><dd class="facts__value">Company</dd></div>
          <div class="facts__row"><dt class="facts__term">Date</dt><dd class="facts__value pending">[pending: month / year]</dd></div>
          <div class="facts__row"><dt class="facts__term">Source</dt><dd class="facts__value">U.S. Strategic Resources</dd></div>
        </dl>
      </div>
    </section>

    <!-- announcement body — rail kept empty: it holds the 120px alignment,
         but a section number would imply further sections below -->
    <section class="section-indexed section-indexed--last">
      <div class="section-indexed__rail"></div>
      <div class="section-indexed__body">
        <div class="grid-2 grid-2--media">
          <div class="stack-32">
            <article class="article">
              <p class="lead">U.S. Strategic Resources formed to prove critical mineral supply on secured ground in Liberia.</p>
              <p><span class="pending">[pending: full announcement text &mdash; incorporation details, licence references and quotes must match the approved release]</span></p>
              <p>The company holds two contiguous licence areas on the Cestos shear zone in Nimba County, Liberia. <a href="../cestos-project.html">Read about the Cestos Project &rarr;</a></p>
            </article>

            <div class="share">
              <span class="share__label">Share</span>
              <a class="share__link" href="https://www.linkedin.com/sharing/share-offsite/?url={{SITE_URL}}/news/company-formation-announcement" target="_blank" rel="noopener">LinkedIn</a>
              <a class="share__link" href="mailto:?subject=Company%20formation%20announcement&amp;body={{SITE_URL}}/news/company-formation-announcement">Email</a>
            </div>

            <a class="link" href="../news.html">&larr; All announcements</a>
          </div>

          <div class="stack-16">
            <p class="label">The asset</p>
            <figure class="figure">
              <input class="lightbox__state visually-hidden" id="lb-post-fig1" type="checkbox">
              <label class="zoomable" for="lb-post-fig1"><img src="../assets/maps/06-nimba-79-adj-licence-map-regional-geology.webp" alt="Nimba 79 Resources and ADJ Exploration licences over regional geology, Nimba County, Liberia" width="1200" height="800"></label>
              <div class="lightbox">
                <label class="lightbox__backdrop" for="lb-post-fig1" aria-label="Close enlarged figure"></label>
                <div class="lightbox__stage">
                  <img src="../assets/maps/06-nimba-79-adj-licence-map-regional-geology.webp" alt="" width="1200" height="800">
                  <p class="lightbox__caption">Fig. 1 &mdash; Nimba 79 Resources and ADJ Exploration licences over regional geology, Nimba County, Liberia</p>
                </div>
                <label class="lightbox__close" for="lb-post-fig1" aria-label="Close enlarged figure"></label>
              </div>
              <figcaption>Fig. 1 &mdash; Nimba 79 Resources and ADJ Exploration licences over regional geology, Nimba County, Liberia</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>

    <!-- closing CTA -->
    <section class="cta-band">
      <h2 class="h2--statement measure-24">Speak with the team</h2>
      <div class="btn-row">
        <a class="btn btn--primary" href="../contact.html">Request the investor presentation &rarr;</a>
        <a class="btn btn--ghost" href="../cestos-project.html">The asset &rarr;</a>
      </div>
    </section>'''

page(
    file='news/company-formation-announcement.html',
    slug='news/company-formation-announcement',
    title='Company Formation Announcement | U.S. Strategic Resources',
    description=POST_EXCERPT,
    crumb=POST_TITLE, nav='news.html',
    schemas=[POST_SCHEMA], body=post_body,
    crumbs=post_crumbs, prefix='../',
    crumb_trail='''  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="index.html">Home</a> /</li>
      <li><a href="news.html">News</a> /</li>
      <li><span aria-current="page">Company formation announcement</span></li>
    </ol>
  </nav>''')


# Regenerating a page wipes the element links that element-symbols.py writes
# into it, so always re-run that pass here — never rely on running it by hand.
import subprocess
subprocess.run([sys.executable if (sys := __import__('sys')) else 'python3',
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'element-symbols.py')],
               cwd=os.path.join(ROOT, '..'), check=True)
