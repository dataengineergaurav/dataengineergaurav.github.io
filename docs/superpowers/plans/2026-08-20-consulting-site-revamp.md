# Consulting Site Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing résumé-style Jekyll site into an editorial consulting site that explains the fractional data engineering offer, proves credibility, and converts prospective clients to a Calendly call.

**Architecture:** Keep GitHub Pages and Jekyll. Use Liquid layouts, the existing `projects` collection, ordinary Markdown posts, and one Sass entry point; add only the Work and Insights routes and the layouts they require. Keep interactions CSS-native and render all essential content without JavaScript.

**Tech Stack:** Jekyll/GitHub Pages, Liquid, Markdown/Kramdown, SCSS, semantic HTML, `html-proofer`

**Spec:** `docs/superpowers/specs/2026-08-20-consulting-site-revamp-design.md`

## Global Constraints

- Primary audience: consulting clients.
- Primary offer: fractional data engineering leadership.
- Keep Jekyll and GitHub Pages; add no frontend framework, CMS, or JavaScript dependency.
- Use the Editorial Authority direction: cream canvas, forest-green text, amber accent, editorial serif headings, sans-serif body copy.
- Use Insights in navigation/index naming and Field Notes as the homepage section heading.
- Keep one conversion path: `https://calendly.com/gauravgurjar/15min`.
- Do not invent metrics, outcomes, client names, or confidential details.
- Keep the site usable without JavaScript and honor `prefers-reduced-motion`.
- Preserve semantic landmarks, skip link, visible focus, heading order, and readable contrast.
- Defer search, tags, newsletter, theme switcher, carousel, 3D, WebGL, and scroll-jacking.

---

## File Map

- `_layouts/default.html`: global document shell, navigation, and footer.
- `_layouts/post.html`: narrow article shell and consulting CTA.
- `_layouts/project.html`: case-study page structure.
- `_sass/jekyll-theme-minimal.scss`: the complete visual system and responsive behavior.
- `assets/css/style.scss`: unchanged Sass entry point importing the theme.
- `index.md`: consulting-led homepage sections and collection loops.
- `work.md`: Work index route.
- `insights.md`: Insights index route.
- `_projects/dubai-real-estate-data-pipeline.md`: first publishable case study and structured metadata.
- `_posts/2026-03-21-never-mix-thinking-with-execution.md`: client-focused article metadata and copy.
- `_config.yml`: collection output/permalink defaults and refined SEO description.
- `README.md`: accurate authoring instructions for case studies and insights.
- `script/cibuild`: unchanged source of truth for build and generated-link verification.

### Task 1: Establish The Editorial Site Shell

**Files:**
- Modify: `_layouts/default.html`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: `site.title`, `page.title`, `site.time`, and existing social URLs.
- Produces: shared `.container`, `.section`, `.eyebrow`, `.button`, `.button-primary`, `.site-header`, `.site-footer`, `.prose`, and `.cta-panel` classes used by every later task.

- [ ] **Step 1: Record the current generated shell and prove the new landmarks are absent**

Run:

```bash
bundle exec jekyll build
! rg -q 'class="nav-cta"' _site/index.html
! rg -q -- '--color-ink: #18372a' _site/assets/css/style.css
```

Expected: the build passes and both negated searches pass because the new shell and token are not implemented.

- [ ] **Step 2: Replace the global navigation and footer markup**

Keep the existing `<head>`, SEO tag, cache-busted stylesheet, skip link, and `{{ content }}`. Replace the header/footer bodies with this semantic structure:

```html
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="{{ '/' | relative_url }}">Gaurav Gurjar</a>
    <nav class="nav-links" aria-label="Primary">
      <a href="{{ '/' | relative_url }}#services">Services</a>
      <a href="{{ '/work/' | relative_url }}">Work</a>
      <a href="{{ '/insights/' | relative_url }}">Insights</a>
      <a href="{{ '/' | relative_url }}#about">About</a>
      <a class="nav-cta" href="https://calendly.com/gauravgurjar/15min">Book a call</a>
    </nav>
  </div>
</header>
```

Use a compact footer with one positioning sentence, GitHub/LinkedIn/Medium/X links, and the existing copyright. Do not add a menu script.

- [ ] **Step 3: Replace the GitHub-like theme with the approved token system**

Retain the Rouge import and reset useful defaults. Define these root values and build all later styles from them:

```scss
:root {
  --color-paper: #f5f0e5;
  --color-paper-deep: #ebe3d3;
  --color-ink: #18372a;
  --color-ink-muted: #51665b;
  --color-accent: #efb34e;
  --color-rule: rgba(24, 55, 42, 0.24);
  --font-display: Georgia, "Times New Roman", serif;
  --font-body: "Avenir Next", Avenir, "Segoe UI", sans-serif;
  --content-width: 74rem;
  --reading-width: 44rem;
}
```

Use a subtle CSS radial-gradient texture on `body`, fluid display sizes with `clamp()`, a 44px minimum height for actionable nav links/buttons, clear `:focus-visible`, and the existing reduced-motion rule. Remove the dark color-scheme block and theme-switching assumptions.

- [ ] **Step 4: Build and inspect the shared shell**

Run:

```bash
bundle exec jekyll build
rg -n 'nav-cta|Services|/work/|/insights/' _site/index.html
rg -n -- '--color-ink: #18372a|prefers-reduced-motion|min-height: 44px' _site/assets/css/style.css
```

Expected: all searches return matches and Jekyll reports a successful build.

- [ ] **Step 5: Commit the shell**

```bash
git add _layouts/default.html _sass/jekyll-theme-minimal.scss
git commit -m "Revamp the global editorial site shell"
```

### Task 2: Rebuild The Homepage Around The Consulting Offer

**Files:**
- Modify: `index.md`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: shared classes from Task 1, `site.projects`, `site.posts`, and the Calendly URL.
- Produces: homepage anchors `#services`, `#work`, `#about`, and reusable visual patterns for `.proof-grid`, `.service-grid`, `.project-feature`, `.testimonial-grid`, and `.post-grid`.

- [ ] **Step 1: Prove the approved homepage message and section order are absent**

Run:

```bash
bundle exec jekyll build
! rg -q 'Turn complex data into systems your business can trust' _site/index.html
! rg -q 'id="services"' _site/index.html
```

Expected: both checks pass because the old résumé homepage is still rendered.

- [ ] **Step 2: Replace the hero and proof strip**

Use this exact first-screen structure, leaving metrics marked as qualified statements rather than creating unsupported numbers:

```html
<section class="hero">
  <p class="eyebrow">Fractional data engineering lead · Dubai</p>
  <h1>Turn complex data into systems your business can trust.</h1>
  <p class="hero-copy">I help teams modernize data platforms, automate high-value workflows, and ship governed AI systems—from architecture through production.</p>
  <a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a>
</section>

<section class="proof-grid" aria-label="Selected experience">
  <p><strong>$1M+</strong><span>in data projects delivered</span></p>
  <p><strong>2M+</strong><span>users supported by shipped systems</span></p>
  <p><strong>8 years</strong><span>across data, analytics, and AI</span></p>
</section>
```

Before merging, verify `$1M+`, `2M+`, and `8 years` against the owner's source material. If any cannot be substantiated, replace that item with a non-numeric fact already supported by `index.md`; do not approximate.

- [ ] **Step 3: Add services and selected-work sections**

Create three service cards titled “Modernize the platform,” “Automate with AI,” and “Lead delivery.” Add a selected-work loop limited to projects where `featured: true`, sorted by `order`, and link each card to `project.url`:

```liquid
{% assign featured_projects = site.projects | where: "featured", true | sort: "order" %}
{% for project in featured_projects limit: 2 %}
  <article class="project-feature">
    <p class="eyebrow">{{ project.sector }}</p>
    <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
    <p>{{ project.summary }}</p>
    <p class="project-outcome">{{ project.outcome }}</p>
  </article>
{% endfor %}
```

- [ ] **Step 4: Curate authority, About, Field Notes, and the final CTA**

Render one complete recommendation from Benjamin Harvey and two shorter supporting recommendations from Raja Ram S and Le Zhang. Replace the five-job résumé stack with a compact About narrative plus a short “Selected experience” list that clearly describes ISHIR/SageSure as one overlapping client engagement. Render the newest two posts under `## Field Notes`:

```liquid
{% for post in site.posts limit: 2 %}
  <article class="post-card">
    <p class="eyebrow">{{ post.date | date: "%b %Y" }}</p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p>{{ post.summary | default: post.excerpt | strip_html | truncate: 150 }}</p>
  </article>
{% endfor %}
```

End with `.cta-panel`, the heading “Have a data challenge that has outgrown quick fixes?”, and “Book a 15-minute call.” Keep social links in the footer, not the homepage body.

- [ ] **Step 5: Add responsive homepage styles**

Use CSS Grid for proof, services, project, testimonial, and post cards. Collapse each grid to one column at `48rem`; preserve DOM order; limit prose to `--reading-width`; use no animation beyond a short opacity/translate reveal guarded by `prefers-reduced-motion`.

- [ ] **Step 6: Build and verify hierarchy and content limits**

Run:

```bash
bundle exec jekyll build
rg -n 'Turn complex data|id="services"|Selected work|Field Notes|outgrown quick fixes' _site/index.html
test "$(rg -c 'class="rec' _site/index.html)" -le 3
```

Expected: all named sections exist and no more than three recommendation blocks render.

- [ ] **Step 7: Commit the homepage**

```bash
git add index.md _sass/jekyll-theme-minimal.scss
git commit -m "Reframe homepage for consulting clients"
```

### Task 3: Publish Work And Case-Study Pages

**Files:**
- Modify: `_config.yml`
- Create: `_layouts/project.html`
- Create: `work.md`
- Modify: `_projects/dubai-real-estate-data-pipeline.md`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: shared shell from Task 1 and project-card fields used by Task 2.
- Produces: project documents with `layout`, `title`, `summary`, `sector`, `role`, `tools`, `outcome`, `featured`, and `order`; public URLs under `/work/:name/`.

- [ ] **Step 1: Prove project output is currently disabled**

Run:

```bash
bundle exec jekyll build
test ! -e _site/work/index.html
test ! -e _site/work/dubai-real-estate-data-pipeline/index.html
```

Expected: both paths are absent.

- [ ] **Step 2: Enable the collection with stable URLs**

Replace `projects: output: false` in `_config.yml` with:

```yaml
collections:
  projects:
    output: true
    permalink: /work/:name/
defaults:
  - scope:
      path: ""
      type: projects
    values:
      layout: project
      image: /assets/img/og.png
  - scope:
      path: ""
    values:
      image: /assets/img/og.png
```

Preserve the existing default image behavior and update the site description to lead with fractional data engineering consulting.

- [ ] **Step 3: Structure the Dubai case study without invented outcomes**

Use this front matter:

```yaml
---
title: "Dubai Real Estate Data Pipeline"
summary: "A repeatable ingestion pipeline for collecting and analyzing daily Dubai property listings."
sector: Real estate data
role: Data architecture and pipeline delivery
tools: Python, MongoDB, REST API
outcome: "Turned changing listing data into a timestamped dataset ready for repeatable analysis."
featured: true
order: 1
---
```

Rewrite the body under `## Problem`, `## Approach`, `## Architecture`, and `## Outcome`. Reuse only facts already present in the source: daily API collection, timestamps, MongoDB, and the crawler/file-writer/dumper services. State “repeatable analysis” rather than claiming unverified revenue, latency, or volume gains.

- [ ] **Step 4: Add the case-study layout and Work index**

`_layouts/project.html` must render metadata, content, and CTA:

```html
---
layout: default
---
<article class="case-study">
  <header class="case-study-header">
    <p class="eyebrow">{{ page.sector }}</p>
    <h1>{{ page.title }}</h1>
    <p class="lede">{{ page.summary }}</p>
    <dl class="case-study-meta">
      <div><dt>Role</dt><dd>{{ page.role }}</dd></div>
      <div><dt>Tools</dt><dd>{{ page.tools }}</dd></div>
      <div><dt>Outcome</dt><dd>{{ page.outcome }}</dd></div>
    </dl>
  </header>
  <div class="prose">{{ content }}</div>
  <aside class="cta-panel"><h2>Planning a data platform that needs to last?</h2><a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a></aside>
</article>
```

Create `work.md` with `layout: default`, `title: Selected Work`, `permalink: /work/`, an introductory paragraph, and a loop over `site.projects | sort: "order"` using the same metadata and links as the homepage.

- [ ] **Step 5: Style project index and article anatomy**

Add narrow prose, responsive `<dl>` rows, a CSS-only pipeline schematic style for `.architecture-flow`, and cards matching the approved editorial direction. Do not add diagrams as images or JavaScript.

- [ ] **Step 6: Build and verify both public routes**

Run:

```bash
bundle exec jekyll build
test -f _site/work/index.html
test -f _site/work/dubai-real-estate-data-pipeline/index.html
rg -n 'repeatable ingestion|Data architecture and pipeline delivery|Discuss your data challenge' _site/work/dubai-real-estate-data-pipeline/index.html
```

Expected: both files exist and all structured case-study content renders.

- [ ] **Step 7: Commit Work**

```bash
git add _config.yml _layouts/project.html work.md _projects/dubai-real-estate-data-pipeline.md _sass/jekyll-theme-minimal.scss
git commit -m "Add consulting case-study pages"
```

### Task 4: Add The Client-Focused Insights Experience

**Files:**
- Create: `insights.md`
- Modify: `_layouts/post.html`
- Modify: `_posts/2026-03-21-never-mix-thinking-with-execution.md`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: `site.posts`, shared `.prose` and `.cta-panel` classes.
- Produces: `/insights/`, post front matter fields `layout`, `title`, `date`, `summary`, and optional `description`.

- [ ] **Step 1: Prove the Insights route and processed post are absent**

Run:

```bash
bundle exec jekyll build
test ! -e _site/insights/index.html
! rg -q 'Why reliable AI systems separate policy from execution' _site/index.html
```

Expected: the route and revised title are absent. The current post lacks YAML front matter and therefore does not provide dependable page metadata.

- [ ] **Step 2: Convert the existing essay into a client-facing post**

Add this front matter:

```yaml
---
layout: post
title: "Why Reliable AI Systems Separate Policy from Execution"
date: 2026-03-21
summary: "A practical architecture rule for keeping governed AI workflows understandable, testable, and safe to change."
description: "Separate business policy from orchestration to make AI-agent workflows easier to govern and operate."
---
```

Keep the existing refund-policy example, but rewrite the opening around the client risk: policy hidden inside retries, prompts, and orchestration becomes hard to audit. Remove malformed escaped blockquotes, stray `--`, and manual horizontal rules. End the article body with the practical rule, leaving the commercial CTA to the layout.

- [ ] **Step 3: Create the Insights index**

Create `insights.md` with `layout: default`, `title: Insights`, `permalink: /insights/`, a short client-oriented introduction, and a reverse-chronological loop over all posts. Each card renders date, title, and `post.summary` with a descriptive “Read article” link.

- [ ] **Step 4: Simplify and strengthen the post layout**

Replace tag links and duplicate title behavior with:

```html
---
layout: default
---
<article class="article">
  <header class="article-header">
    <p class="eyebrow">Insight · {{ page.date | date: "%-d %B %Y" }}</p>
    <h1>{{ page.title }}</h1>
    {% if page.summary %}<p class="lede">{{ page.summary }}</p>{% endif %}
  </header>
  <div class="prose">{{ content }}</div>
  <aside class="cta-panel"><h2>Need this kind of clarity in your data or AI platform?</h2><a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a></aside>
</article>
```

Do not render tags until a taxonomy is deliberately introduced.

- [ ] **Step 5: Add article and Insights-index styles**

Keep article text at `--reading-width`, provide clear code-block overflow on mobile, preserve Rouge syntax highlighting, and make the index a simple list/grid that collapses to one column at `48rem`.

- [ ] **Step 6: Build and verify article metadata and links**

Run:

```bash
bundle exec jekyll build
test -f _site/insights/index.html
rg -n 'Why Reliable AI Systems|Read article' _site/insights/index.html
rg -n 'Need this kind of clarity|Discuss your data challenge' _site/2026/03/21/never-mix-thinking-with-execution.html
```

Expected: the index, post, and CTA all render at stable generated paths.

- [ ] **Step 7: Commit Insights**

```bash
git add insights.md _layouts/post.html _posts/2026-03-21-never-mix-thinking-with-execution.md _sass/jekyll-theme-minimal.scss
git commit -m "Add client-focused consulting insights"
```

### Task 5: Align Documentation, SEO, And Generated Output

**Files:**
- Modify: `README.md`
- Modify: `_includes/head-custom.html` only if a verified head fix is needed during inspection
- Modify: `assets/img/og.png` only if the existing image does not match the new cream/green/amber identity

**Interfaces:**
- Consumes: final routes and front-matter contracts from Tasks 3 and 4.
- Produces: accurate authoring instructions and share metadata consistent with the deployed site.

- [ ] **Step 1: Identify stale documentation and metadata**

Run:

```bash
rg -n 'portfolio and blog|categories:|Short case study|Posts appear on the homepage' README.md
bundle exec jekyll build
rg -n '<meta property="og:|canonical|application/ld\+json' _site/index.html
```

Expected: README matches reveal stale authoring guidance; SEO tags remain present.

- [ ] **Step 2: Update README authoring contracts**

Document the exact project front matter from Task 3 and the post front matter from Task 4. State that case studies appear under `/work/`, articles under `/insights/`, and the homepage features at most two of each. Remove category/tag instructions and describe the site as a consulting site rather than a generic portfolio.

- [ ] **Step 3: Inspect social metadata and OG art**

Open `_site/index.html` and verify title, description, canonical URL, Person JSON-LD, and `/assets/img/og.png`. Inspect the image at desktop size. If it already communicates Gaurav's name and consulting positioning legibly, leave it unchanged. If not, replace only `assets/img/og.png` with a 1200×630 image using the approved colors and the text “Gaurav Gurjar · Fractional Data Engineering Lead”; preserve the configured path.

- [ ] **Step 4: Build and verify documentation-facing contracts**

Run:

```bash
bundle exec jekyll build
rg -n '/work/|/insights/|featured: true|summary:' README.md
rg -n 'Fractional data engineering|og:image|canonical' _site/index.html
```

Expected: route and metadata contracts are documented and rendered.

- [ ] **Step 5: Commit documentation and any verified asset change**

```bash
git add README.md _includes/head-custom.html assets/img/og.png
git diff --cached --quiet || git commit -m "Align consulting site metadata and docs"
```

Only stage `_includes/head-custom.html` or `assets/img/og.png` if inspection required a real change.

### Task 6: Perform Responsive, Accessibility, And Release Verification

**Files:**
- Modify: only files with defects discovered by the checks below

**Interfaces:**
- Consumes: the complete generated site.
- Produces: a release-ready static build with working internal routes and no known keyboard, responsive, motion, or generated-link regressions.

- [ ] **Step 1: Run the repository's full build and link checker**

Run:

```bash
chmod +x script/cibuild
script/cibuild
```

Expected: Jekyll and `html-proofer` exit 0 with no broken internal links, images, or scripts.

- [ ] **Step 2: Serve the generated site and inspect core routes**

Run:

```bash
bundle exec jekyll serve
```

Inspect `/`, `/work/`, `/work/dubai-real-estate-data-pipeline/`, `/insights/`, and `/2026/03/21/never-mix-thinking-with-execution.html` at approximately 375px, 768px, and 1440px viewport widths.

Expected: no horizontal page overflow; cards collapse in DOM order; body copy remains readable; CTA and navigation targets remain reachable.

- [ ] **Step 3: Perform keyboard and semantic checks**

On every core route, tab from the browser chrome through the page. Verify the skip link becomes visible, focus never disappears, navigation order follows the visual order, every page has one `<h1>`, headings do not skip levels, and Calendly links have descriptive text.

Run this generated-output sanity check:

```bash
for page in _site/index.html _site/work/index.html _site/work/dubai-real-estate-data-pipeline/index.html _site/insights/index.html _site/2026/03/21/never-mix-thinking-with-execution.html; do test "$(rg -o '<h1[ >]' "$page" | wc -l | tr -d ' ')" = 1 || exit 1; done
```

Expected: exit 0.

- [ ] **Step 4: Check motion, no-JavaScript behavior, and content claims**

Enable reduced motion in browser developer tools and confirm reveal/scroll behavior stops. Disable JavaScript and reload all core routes; all content and navigation must remain usable. Compare the three homepage proof statements, case-study outcome, and rendered testimonials against the source content in the repository; remove or qualify anything not directly supported.

- [ ] **Step 5: Fix only verified defects and rerun the full gate**

Apply the smallest source change for each observed defect, then run:

```bash
script/cibuild
git diff --check
```

Expected: both commands exit 0.

- [ ] **Step 6: Commit release fixes if any**

```bash
git add index.md work.md insights.md _config.yml _layouts _sass _projects _posts README.md assets/img
git diff --cached --quiet || git commit -m "Polish consulting site release"
```

Do not create an empty commit when verification required no changes.
