# Design Checkup — dataengineergaurav.github.io

- **Mode:** `/design checkup` (vital-sign triage)
- **Date:** 2026-10-09
- **Surface:** homepage (`index.html`, `layout: none`) + secondary pages (`_layouts/default.html` via `assets/css/style.css`)
- **Register:** Brand (portfolio / lead-generation)

## Score

**35 / 60**

## Verdict

**Block** — one `HIGH` stands: text in the pinned Work section renders below 4.5:1 against its
ground, and the primary navigation disappears on phones. Both are escalation triggers, so
Accessibility scores `Critical` on sight and is not averaged down.

## TL;DR

The identity is deliberate and the composition fits the job: this is a **Decide** surface that
leads with proof and one dominant action, and the paper/ink/amber ledger reads as chosen rather
than assembled. What it fails is the floor, not the taste. The dark Work chapter has several
labels below readable contrast, the header drops every nav link except the CTA below 640px, the
focus ring is amber-on-paper (1.65:1), the homepage has no skip link, and every reveal/cue/pinned
act starts at `opacity: 0` and depends on the runtime to become visible.

Primary recommendation: fix contrast and the mobile nav, add the no-JS floor and the skip link,
then lift the focus ring and the smallest mono labels.

## Heuristic scores

| # | Vital sign | Score | Key finding |
|---|---|---|---|
| 1 | Intentionality | 10 / 10 | Ledger/folio identity is content-shaped, not a template reflex |
| 2 | Readability | 5 / 10 | Work-chapter labels below 4.5:1; smallest mono labels 0.52–0.62rem |
| 3 | Usability | 5 / 10 | Mobile reaches only the CTA; no skip link on the homepage |
| 4 | Responsiveness | 5 / 10 | Nav links removed ≤640px; nav tap targets 32px |
| 5 | Speed | 10 / 10 | No homepage images, one script, one stylesheet, preconnected fonts |
| 6 | Accessibility | 0 / 10 | Contrast trigger + hidden controls + weak focus ring → Critical |

## Findings

Ordered by severity, then reach and leverage.

| # | Severity | Discipline | Location | Before | After | Why |
|---|---|---|---|---|---|---|
| 1 | HIGH | Accessibility | `index.html:235` | `@media (max-width:640px){ .site-bar__nav a:not(.is-cta){display:none} }` | Add a `<details>` disclosure (or equivalent) that exposes Services/Work/Insights/About below 640px | On phones the only reachable control is the Calendly CTA; Work, Insights and About are unreachable — controls hidden |
| 2 | HIGH | Color | `index.html:133,149,151` | `.work-rail-label__count` `rgba(245,240,229,0.35)`; `.work-aside__label` `…,0.4`; `.work-ledger-mini__row` `opacity:0.32` | Raise the alphas to ≈0.62 on the dark stage (`#0f1f18`) | Text on a background it lacks contrast against: 2.9:1, 3.4:1 and ≈2.4:1 respectively, all under 4.5:1 |
| 3 | MEDIUM | Accessibility | `scrollcraft.css:267,286–290` + `index.html` consumers | `[data-sc-cue]{opacity:0}`, `[data-sc-in]{opacity:0}`; reveals only via `.sc-in` / `.sc-ready` added by JS | Gate the hidden base state behind `html:not(.sc-ready)`, and flow the pinned/pan acts when the runtime is absent | Without the runtime (disabled, blocked, or failed) the lede, CTAs, proof, capabilities, voices, insights and all four Work cases render invisible; the pinned cases also stack absolutely |
| 4 | MEDIUM | Accessibility | `index.html:239–273` | No skip link; the nav sits before `<main id="top">` (compare `_layouts/default.html:17`) | Add `<a class="skip-link" href="#top">Skip to content</a>` as the first body element | Keyboard users tab the full nav on every visit; the other layouts already ship this |
| 5 | MEDIUM | Interaction | `index.html:232` | `.site-bar__nav a{min-height:32px}` | Raise to `min-height:44px` | Tap targets below 44×44px mis-tap on touch |
| 6 | MEDIUM | Accessibility | `scrollcraft.css:123–127` (accent overridden at `index.html:24`) | `:focus-visible{outline:2px solid var(--sc-accent)}` = `#efb34e` on `#f5f0e5` | Use a two-tone ring: a light ring with a dark halo (or ink ring on light, light ring on the dark stage) | Focus indicator contrast is 1.65:1 against paper, under the 3:1 non-text minimum |
| 7 | MEDIUM | Accessibility | `index.html:50` | `.folio a{opacity:0.35}` → ≈2.0:1, and the links stay in the tab order at full page height | Raise the resting opacity to ≈0.72, or take inactive chapters out of the tab order | Interactive nav text below 4.5:1 while still focusable |
| 8 | LOW | Type | `index.html:56–57,123,135,149,219` | Mono labels at `0.52–0.62rem` (8.3–9.9px) | Lift the smallest labels to ≈0.72–0.75rem | Eyebrow labels are below comfortable reading size at arm's length |

## Considered but rejected

| Location | Candidate | Rejected because |
|---|---|---|
| `index.html:333` | Drop the pinned Work act entirely | The pin is the page's signature and the engine already degrades it under reduced motion; the defect is its colour and its no-JS floor, not the device |
| `index.html:19–34` | Retune the paper/green/amber palette | The palette is a reason-tied brand decision, not a category reflex; it does not read as generic AI output |
| `index.html:311–330`, `413–428` | Flatten the capability and voice grids to lists | The content is genuinely card-shaped — discrete, self-contained, scannable as a unit |
| `scrollcraft.css:380–384` | Remove the grain/dot atmosphere | `pointer-events:none`, low opacity, and it is the difference between "a dark page" and "a lit room" |
| `_sass/jekyll-theme-minimal.scss` | Merge its tokens with the scrollcraft tokens | The two systems agree on paper/ink/accent; consolidating them is a refactor with no user-visible effect |

## Verification

Checks that passed:

- **Source inspection** — read `index.html` (all 525 lines), `assets/scrollcraft/scrollcraft.css`,
  `assets/scrollcraft/scrollcraft.js`, `assets/css/style.scss`, `_sass/jekyll-theme-minimal.scss`,
  `_sass/_wiki.scss`, `_layouts/default.html`, `_layouts/post.html`, `_layouts/project.html`,
  `_config.yml`, `script/cibuild`.
- **Contrast computation** — WCAG 2.1 relative-luminance ratios for each reported pair over its
  actual ground (`#f5f0e5`, `#0f1f18`): `.work-rail-label__count` 2.90:1, `.work-aside__label`
  3.40:1, `.work-ledger-mini__row` (0.32) ≈2.4:1, focus ring (amber on paper) 1.65:1, inactive
  folio 1.98:1.
- **Runtime contract** — confirmed `document.documentElement.classList.add('sc-ready')` is the
  last statement of `mount()` (`scrollcraft.js:1157`), which makes `html:not(.sc-ready)` a sound
  no-JS hook, and confirmed the hidden base states at `scrollcraft.css:267,286–290`.
- **Reduced motion** — `scrollcraft.css:386–414` and `_sass/jekyll-theme-minimal.scss` both honour
  `prefers-reduced-motion`; the pan rail is handed back as a scroll region. Passing.
- **Asset inventory (Speed)** — homepage loads one stylesheet, one script, no images, and
  preconnects to Google Fonts.

Checks marked **Not verified**:

- **Rendered focus order and ring visibility in a live browser** — inferred from source only.
- **320px reflow and 200% zoom** — not exercised in a real viewport.
- **`script/cibuild` output** — not run at report time.
- **iOS input auto-zoom** — no `input`, `select` or `textarea` on the homepage; not applicable
  there, and not audited on the wiki pages.
- **Field load timings** — asset inventory only; no measured metrics.

## Next modes

`/design a11y` (findings 3–7), `/design recolor` (findings 2, 6), `/design responsive` (findings
1, 5), `/design typeset` (finding 8). The fixes for findings 1–7 were applied in the same pass;
see the working answer.
