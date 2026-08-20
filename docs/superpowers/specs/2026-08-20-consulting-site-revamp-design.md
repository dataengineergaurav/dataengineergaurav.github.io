# Consulting Site Revamp — Design

Date: 2026-08-20  
Status: Approved in conversation  
Audience: Consulting clients  
Primary offer: Fractional data engineering leadership

## Objective

Reposition the site from an online résumé into a consulting website that helps
a prospective client quickly understand Gaurav's offer, see credible evidence,
and book a 15-minute call.

The redesign keeps the existing Jekyll and GitHub Pages stack. It changes the
information hierarchy, content framing, and visual system without adding a
frontend framework, CMS, or unnecessary client-side behavior.

## Positioning

Lead with fractional data engineering leadership: hands-on strategy and
delivery from architecture through production. Present three supporting buying
paths:

1. Modernize data platforms: cloud architecture, pipelines, quality, and
   governance.
2. Automate with AI: production agents and workflow automation with practical
   guardrails.
3. Lead delivery: technical roadmaps, standards, and execution across data and
   analytics teams.

The homepage must describe client outcomes before tools or employment history.
Technology names support credibility inside service and case-study content;
they do not drive the top-level message.

## Design Direction

Use the approved **Editorial Authority** direction: warm, distinctive, and
senior rather than resembling a generic SaaS landing page or terminal-themed
developer portfolio.

### Visual system

- Warm cream page canvas with deep forest-green text and an amber accent.
- Expressive editorial serif for headlines; highly readable sans-serif for
  body copy and navigation.
- Large type, generous whitespace, thin rules, and restrained asymmetric
  composition.
- Subtle paper-like background texture created in CSS; no stock imagery needed
  for the base design.
- Data-flow diagrams and system schematics built with HTML/CSS for case-study
  visuals where real client imagery is unavailable.
- Small CSS-only entrance reveals and purposeful hover states, disabled when
  `prefers-reduced-motion` requests it.
- Light mode is the art direction. Do not add a theme switcher in this phase.

The visual language may borrow the useful parts of current portfolio trends —
editorial typography, modular layouts, tactile warmth, and selective motion —
without adopting decorative bento grids, 3D effects, or kinetic typography
that compete with the consulting message.

## Information Architecture

### Homepage `/`

The homepage follows this sequence:

1. **Proposition** — “Turn complex data into systems your business can trust,”
   a short supporting statement, and one primary CTA to discuss a data
   challenge.
2. **Proof strip** — three defensible metrics such as project value, users
   supported, and years of experience. Every metric must be verified before
   publication.
3. **Services** — the three buying paths above, written as client outcomes.
4. **Selected work** — one featured case study with problem, role, system, and
   outcome; room for a second card when another publishable case study exists.
5. **Authority** — one prominent testimonial plus a compact grid of selected
   supporting recommendations.
6. **Field Notes** — the two newest client-focused articles, each showing title,
   premise, and reading time or date.
7. **Conversion close** — a direct Calendly CTA for problems that have outgrown
   quick fixes.

Employment history, certifications, languages, and the full tool inventory
move into a compact About section lower on the homepage or a dedicated About
page only if the compact version becomes unwieldy. The first implementation
should prefer the compact homepage section.

### Work `/work/`

List publishable consulting case studies. Each card includes the client or
sector context where disclosure permits, the business problem, Gaurav's role,
the outcome, and selected technology.

Individual case studies use this scannable structure:

1. Summary and outcome.
2. Client problem and constraints.
3. Gaurav's role and decisions.
4. Architecture or delivery approach.
5. Results and lessons.
6. Relevant consulting CTA.

The existing Dubai real-estate pipeline becomes the first case study. Its copy
must replace implementation-detail-first language with a client problem and a
measurable or clearly qualified outcome. Do not invent metrics.

### Insights `/insights/`

Rename “Thoughts” to **Field Notes** on the homepage. Use **Insights** as the
navigation label and index-page title for clarity.

The blog remains tightly client-focused. Topics cover data-platform
modernization, governed AI agents, reliable analytics, data quality, and
delivery decisions. Articles should demonstrate judgment a buyer can apply,
not function as personal learning logs.

Each post includes:

- A concrete client problem in the title or introduction.
- A short summary and publication date.
- A readable, narrow article layout.
- A context-relevant consulting CTA at the end.

The homepage shows only two recent posts. The index lists all posts in reverse
chronological order. Search, categories, tags, newsletter signup, and related
post automation are deferred until content volume creates a real need.

## Navigation

Use a small sticky header with:

- Services (homepage anchor)
- Work
- Insights
- About (homepage anchor)
- Book a call

“Book a call” is visually distinct but not oversized. Mobile navigation may
wrap into a compact two-row header or use a native disclosure pattern. Avoid a
JavaScript menu unless CSS and semantic HTML cannot keep it usable.

## Content Changes

- Rewrite the hero around client transformation, not a professional summary.
- Reduce the current About copy to a short positioning narrative.
- Consolidate overlapping ISHIR and SageSure experience so the relationship is
  clear and does not look like duplicate simultaneous employment.
- Replace the long recommendations stack with a curated selection; retain all
  source text in the repository if useful, but do not render all quotes on the
  homepage.
- Move tool lists into supporting contexts and group them by capability.
- Use one consistent CTA phrase throughout the site.
- Preserve LinkedIn, GitHub, Medium, and X links in the footer; Calendly remains
  the primary conversion destination.

## Components

Keep components native to Jekyll and reuse existing collections where they fit:

- Site header and footer in the default layout.
- Hero and proof strip on the homepage.
- Service cards.
- Case-study cards backed by the existing `projects` collection, expanded only
  with fields required by the approved design.
- Testimonial feature and compact recommendation grid.
- Post preview cards from `site.posts`.
- Shared CTA block.
- Dedicated layouts for case studies, the insights index, and posts where the
  current layouts do not cover those needs.

Do not create a generalized design-system component library. Shared Liquid
includes are justified only when the same non-trivial block is rendered in
multiple places.

## Responsive And Accessible Behavior

- Use a mobile-first layout with a readable line length and fluid type via
  `clamp()`.
- Collapse multi-column sections to one column without changing content order.
- Keep touch targets at least 44 CSS pixels where practical.
- Preserve semantic headings, landmarks, skip link, visible keyboard focus,
  descriptive link text, and sufficient color contrast.
- Honor `prefers-reduced-motion` and avoid scroll-jacking.
- Do not hide important proof or calls to action on small screens.
- Maintain acceptable rendering without JavaScript.

## Performance And SEO

- Keep the site static and dependency-light.
- Use local or carefully selected web fonts with limited weights; preload only
  assets proven necessary.
- Prefer CSS graphics and optimized existing image formats.
- Preserve `jekyll-seo-tag`, sitemap generation, canonical metadata, Open Graph
  assets, and Person schema.
- Give Work and Insights index pages unique titles and descriptions.
- Target stable Core Web Vitals; avoid layout shift from fonts and media.

## Verification

- `bundle exec jekyll build` succeeds.
- Existing link and HTML checks succeed through `script/cibuild` where
  available.
- Homepage, Work, Insights, case-study, and post layouts are manually checked
  at narrow mobile, tablet, and desktop widths.
- Keyboard navigation, focus visibility, heading order, contrast, and reduced
  motion are checked manually.
- All proof metrics, testimonials, client claims, and outbound links are
  verified before release.
- The generated site works with JavaScript disabled.

## Delivery Sequence

1. Establish tokens, typography, global layout, header, and footer.
2. Rebuild homepage hierarchy and rewrite the offer-led content.
3. Expand the projects collection and add Work/case-study views.
4. Add the Insights index and update the post layout and CTAs.
5. Perform responsive, accessibility, performance, and content verification.

## Non-Goals

- No migration from Jekyll or GitHub Pages.
- No React, Vue, Tailwind, component framework, CMS, or new JavaScript
  dependency.
- No search, tags, newsletter, theme switcher, testimonial carousel, 3D,
  WebGL, scroll-jacking, or decorative animation system.
- No invented client outcomes or confidential project details.
- No additional case studies until publishable source material exists.

## Success Criteria

A first-time consulting prospect can understand the offer, identify a relevant
service, see credible evidence, and reach the Calendly action in under one
minute. The site feels recognizably authored by a senior independent data
consultant, remains fast on mobile, and makes ongoing publication possible with
ordinary Jekyll Markdown files.
