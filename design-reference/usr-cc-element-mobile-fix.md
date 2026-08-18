## Mobile behavior for `.element-symbol` — resolving the open note in Breakpoint Notes

Current state: on touch, tooltip is suppressed (`@media (hover: none)`) and tap goes straight to the PubChem link — symbols read as bare "Au", "Co", "Nd" with no way to see the full name first.

**Requested fix:** same checkbox-hack pattern already used for the FAQ, mobile menu, and lightbox — no JavaScript, no double-tap.

**Behavior:**
1. Tap on a symbol opens a small inline tooltip/popover showing the full name (e.g. "Promethium") — does **not** navigate yet.
2. Inside that popover, an explicit link ("View on PubChem →") is the only thing that navigates.
3. Tapping outside (backdrop, same as the lightbox pattern) closes the popover without navigating.

**Why not double-tap:** there's no native way to distinguish "first tap" from "second tap" on the same element without JavaScript, and it breaks for keyboard/screen-reader users who don't have a tap gesture at all. The checkbox-hack (visually-hidden checkbox + labels) already solves this exact problem elsewhere in the system — reuse it here instead of inventing new interaction logic.

Apply via the same `.element-symbol` component and `data-element` attribute already in place — this is a state/markup addition, not a new component. Keep desktop hover behavior unchanged; this only affects the `@media (hover: none)` branch.
