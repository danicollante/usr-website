# USR — Breakpoint notes

Companion to `USR System — Filing.dc.html` and `USR System — Handoff Notes.md`.
Validated on Home and Cestos Project; apply the same logic to the remaining six pages.

All responsive work is additive and lives in **§11 of `css/style.css`**. §01–§10 are the
desktop design and were not modified, apart from two lines: the file header note, and
`.nav-mobile` added to the `@media print` hide list.

## The three states

| | Width | What it is |
|---|---|---|
| Desktop | ≥ 1440px | The designed page. Fixed `--page-width: 1440px`. Unchanged. |
| Fluid | ≤ 1439px | Same layout, `.page` goes 100%, inset 72 → 48px, H1 88 → 72px. |
| Tablet | ≤ 1023px | Nav collapses; index rail collapses; media pairs stack, text pairs hold. |
| Mobile | ≤ 767px | Everything single-column; tables become stacked cards. |

Reflow is driven first by re-declaring the §01 tokens inside each breakpoint, so any new
component that uses `--page-inset`, `--section-pad`, `--gap-2up` or `--gap-3up` inherits
the behaviour without new rules.

```
                 desktop   fluid   tablet   mobile
--page-inset      72        48      40       20
--section-pad     88        76      64       48
--rail           120        96      —        —
--gap-2up         64        48      40       32
--gap-3up         48        40      32       28
--label-size      13        13      13       12
--header-h        —         —       85       77
```

## Structural changes

**Header — 6 links + CTA → menu, at ≤1023px.** The desktop bar needs ~1030px, so it
collapses at tablet, not only at mobile. `.nav` and `.site-header__cta` are hidden and
`<details class="nav-mobile">` appears: hamburger → wordmark "Menu", opening a full-height
panel of serif links with the primary CTA pinned at its base. No JavaScript — `<details>`
carries the state, the same pattern already used by the FAQ. The panel is fixed from
`--header-h` down, not from 0, so the logo and the close control stay visible. Body scroll
behind the panel is not locked; that would need JS and the panel is opaque and full-height.
**`--header-h` is hardcoded per breakpoint — if header padding or logo height changes,
update it.**

**Index rail (Cestos 01–07) — collapses into the section head at ≤1023px.**
`.section-indexed` switches from `grid` to `block`, so `.section-indexed__rail` falls
above `.section-indexed__body` and reads as a gold mono eyebrow over each H2 — the same
size and letterspacing as `.label`. No markup change; the rail div stays where it is.
Dropped at tablet as well as mobile because a 768px page minus insets minus a 120px rail
leaves the body too narrow to hold the two-column pairs tablet keeps.

**Hero fact-table — stacks below the H1 at ≤1023px.** `.grid-hero` goes single-column with
`align-items: start`. The `.facts` rows keep their desktop form: term left, value right,
hairline between, 2px forest rule on top. Nothing about the component changes.

**Tables — tabular at tablet, stacked cards at mobile.** At ≤1023px cell padding drops to
16px and body cells to 15px; three and four columns still fit at 768. At ≤767px the table
switches to `display: block`, `<thead>` is visually hidden, and every `<tr>` becomes a
card: forest rule top and bottom of the run, hairlines between, cells stacked 14px apart.
Column headers come back **per cell** from `data-label`, set as a 10px mono uppercase
label above the value.

- Requires `data-label="…"` on every `<td>`/`<th>` that becomes a card row. This is the
  one markup change the tables need. `.table__lead` is the card head and gets a label too.
- Per-cell rather than per-column, because the licence comparison labels its two data
  columns "Nimba 79 Resources" / "ADJ Exploration" — the label is the licence, not a
  generic column name.
- **Sequence tables** (roadmap): add `.table--sequence` to the `<table>` and number the
  lead cell's label — `data-label="Phase 01"`, `"Phase 02"`, `"Phase 03"`. The label sets
  gold instead of muted, so once the columns are gone the order still reads down the page
  and the phase numerals are not carrying it alone.

**Figure grids — stack at ≤1023px.** `.figure__pair` (the two-up gold/cobalt maps) goes
single-column with a 16px gap under its one shared caption; the six-up ADJ grid is a single
image and simply scales. Two-column blocks that pair a figure with text carry an explicit
`.grid-2--media` class and stack at tablet, while text-only pairs (`.grid-2-wide`,
`.grid-2--wide-gap`) hold until mobile. The class is explicit rather than `:has(.figure)`
so the rule is greppable and predictable in the build.

**Leadership 3-up — becomes a ruled list at ≤1023px.** `.grid-3` goes single-column and
`.person` turns horizontal: portrait left (120px, 84px at mobile), name/role/bio right.
Avoids the 2 + 1 orphan a two-column tablet grid would produce with three people.

**Other grids at ≤767px.** `.grid-2`, `.grid-2-wide`, `.grid-aside`, `.pairs__row`,
`.form__row`, `.news__item`, `.post`, `.list__item` all go single-column. `.stats` holds
2 × 2 at both breakpoints. `.takeaways__item` keeps its number rail, narrowed 60 → 40px.
`.heading-row` stacks its mono qualifier under the H2. Footer 4-col → 2-col at tablet →
1-col at mobile.

**Actions.** `.btn-row` and `.subscribe` go vertical and full-width at ≤767px; button
padding goes to 15px so every tap target clears 44px.

## Figures — ratio fix and lightbox

**The distortion was a presentational-hint collision, not an `object-fit` problem.**
`<img width="1200" height="800">` maps both attributes to presentational hints.
`.figure img { width: 100% }` overrode the width hint but left the height hint applied, so
every figure resolved to *100% × 800px* and stretched. It was wrong at desktop too — just
less visible, because the desktop column width happened to sit near the true ratio.
The fix is `height: auto` on the image; `object-fit: contain` is set alongside it so no
future rule can crop these frames. **Maps are never cropped** — legend, coordinate frame and
licence boundary all carry information.

**Lightbox — one pattern, every figure.** Tap or click any map to open it over the page at
full viewport size. Dense figures (the prospectivity surfaces, the six-panel ADJ grid) are
unreadable at 375px otherwise. JS-free, same family as the FAQ and the mobile menu: a
visually-hidden checkbox holds the open state, and both the backdrop and the X are
`<label for>` pointing back at it. Pinch-zoom over the open overlay works natively.

```html
<input class="lightbox__state visually-hidden" id="lb-fig1" type="checkbox">
<label class="zoomable" for="lb-fig1"><img src="…" alt="…" width="1200" height="800"></label>
<div class="lightbox">
  <label class="lightbox__backdrop" for="lb-fig1" aria-label="Close enlarged figure"></label>
  <div class="lightbox__stage">
    <img src="…" alt="" width="1200" height="800">
    <p class="lightbox__caption">Fig. 1 — …</p>
  </div>
  <label class="lightbox__close" for="lb-fig1" aria-label="Close enlarged figure"></label>
</div>
```

- Order matters: the CSS selector is `.lightbox__state:checked ~ .lightbox`.
- The input and the lightbox are both out of flow (absolute / fixed), so the unit drops
  into a flex `.figure` **or** a two-column `.figure__pair` without adding a track or a gap.
  Applied per *image*, not per figure — Fig. 2's two maps get one lightbox each under a
  single shared figcaption.
- The overlay copy uses `alt=""`; the visible figure image keeps the real alt text, so the
  duplicate is not announced twice.
- `.zoomable::after` is an "Enlarge" chip on hover; under `@media (hover: none)` it is
  permanent, since touch has no hover to reveal it.
- Ids in use: `lb-home-fig1` (Home), `lb-fig1` / `lb-fig2a` / `lb-fig2b` / `lb-fig3`
  (Cestos). Ids must be unique per page.
- **Keyboard:** the checkbox is focusable — Space opens, Space closes, and focus stays on
  it. Escape-to-close and focus trapping would both need JavaScript.

## Type scale

```
                desktop  tablet  mobile
h1                 88      56      40
.h1--article       56      40      32
h2                 48      38      30
.h2--statement     56      40      30
h3                 26      24      22
.lead              23      21      19
.subline           26      22      19
.takeaways__text   22      20      18
.stats__figure     52      44      36
.table__lead       22      20      21
```

Body copy stays 17/1.65 throughout. Mono labels stay 10–13px and are not scaled down
further; they are the smallest type in the system already.

## Two things to know

- **Element tooltips under `@media (hover: none)` — RESOLVED.** The hover tooltip is still
  suppressed on touch, but it is now replaced by a tap popover rather than leaving the
  symbols bare. Same checkbox-hack family as the FAQ, the menu and the lightbox: a
  transparent `<label class="element__tap">` sits over each symbol and takes the tap, so the
  first tap opens a small centred card (symbol, full name, and an explicit
  "View on PubChem →" link) instead of navigating; the backdrop is another `<label>` on the
  same checkbox, so tapping outside closes without navigating. Both the overlay and the
  popover are `display: none` on pointer devices, so mouse and keyboard behaviour is
  unchanged — and because the overlay only intercepts *pointer* events, Enter on the focused
  link still navigates directly on any device. Markup is emitted by
  `tools/element-symbols.py`; ids are `es-{page}-{n}` and unique per page.
- **The menu does not lock background scroll.** JS-free constraint. Not visible in use.
- **The lightbox has no Escape key and no focus trap.** Same constraint. Space on the
  focused control closes it, as does the backdrop or the X.

## Applying to the other six pages — DONE

All nine pages now carry the responsive markup; audited at 375px and 768px with zero
horizontal overflow, the menu active and every table cell labelled. Nothing in §11 is
page-specific. The per-page work was markup only:

1. Add the `<details class="nav-mobile">` block to `.site-header`, with `aria-current="page"`
   on the current link, and add `site-header__cta` to the desktop header button.
2. Add `data-label` to every table cell; add `.table--sequence` and numbered phase labels
   to any table whose row order carries meaning.
3. Add `.grid-2--media` to any `.grid-2` that pairs a figure or placeholder with text.
4. Wrap every figure image in the zoomable/lightbox unit above, with page-unique ids.

What that came to in practice:

| Page | nav-mobile | data-label | .grid-2--media | lightbox |
|---|---|---|---|---|
| Company | yes | — | — | — |
| Why Liberia | yes | — | photo pair | — (placeholders) |
| Critical Minerals | yes | 12 cells | — | — |
| News | yes | — | — | — |
| Contact | yes | — | — | — |
| Legal | yes | — | — | — |
| News post | yes | — | text + figure | `lb-post-fig1` |

No sequence table exists outside the Cestos roadmap: Critical Minerals' "Demand outruns
supply" has no meaningful row order, so it takes plain column labels and no
`.table--sequence`. The business-model steps are `.steps`, not a table, and §11 already
covers them.

**Photography placeholders are deliberately not wrapped in a lightbox.** The unit needs an
`<img>` to enlarge, and a hatched "pending from USR" block has nothing to show — the
affordance would be dead. Each placeholder carries an HTML comment saying to add the unit
when the real image lands, with the ids to use. Leadership portraits stay unzoomable.

Components already covered by §11 with no markup change: `.section-indexed`, `.facts`,
`.takeaways`, `.stats`, `.chips`, `.pairs`, `.faq`, `.person`, `.news`, `.post-list`,
`.tabs`, `.pagination`, `.share`, `.list`, `.steps`, `.form`, `.subscribe`, `.cta-band`,
`.site-footer`, `.breadcrumb`, all placeholders.
