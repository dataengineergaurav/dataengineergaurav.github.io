# CV-Led Personal Authority Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revamp the Jekyll site into a consulting-first personal authority site using defensible CV evidence, anonymized case studies, and the selected Editorial Experience Ledger design.

**Architecture:** Keep the existing Jekyll layouts, `projects` collection, Liquid rendering, and single Sass theme. Store each anonymized engagement as ordinary project front matter and Markdown, render the same collection into homepage highlights and the Work index, and enforce the privacy rule with one standard-library Python regression test plus a generated-site check in CI.

**Tech Stack:** Jekyll, Liquid, Markdown/Kramdown, SCSS, Python standard library, pytest, HTML-Proofer

**Spec:** `docs/superpowers/specs/2026-08-20-cv-led-authority-revamp-design.md`

## Global Constraints

- Use the selected Editorial Experience Ledger design.
- Keep consulting as the dominant conversion path and strategic-role availability as subdued text.
- Never publicly name clients, employers, or project organizations in project or employment narratives, metadata, URLs, or alternative text.
- Named testimonial authors and their current public organizations are the only organization-name exception.
- Replace `$3B+` with `300+ production pipelines`, `2M+ people reached`, and `7+ years`.
- Preserve the cream, forest, amber, Georgia, and Avenir/system design tokens; add no webfont.
- Add no frontend framework, component library, CMS, analytics dependency, or JavaScript behavior.
- Preserve semantic landmarks, visible focus, 44px targets, reduced motion, and no-JavaScript content.
- Do not invent metrics, outcomes, causal claims, or confidential operational details.

---

## File Map

- `scripts/test_public_content.py`: privacy and approved-proof regression checks over public source or generated HTML.
- `script/cibuild`: builds, validates HTML, then runs the public-content regression check against `_site`.
- `_projects/*.md`: one anonymized engagement per file; front matter is the shared content interface.
- `_projects/dubai-real-estate-data-pipeline.md`: retained as independent work and removed from homepage features.
- `work.md`: separates anonymized client engagements from independent work.
- `index.md`: selected split-hero, proof ledger, capabilities, work ledger, testimonials, About, Field Notes, and CTA.
- `_layouts/default.html`: shared positioning copy and navigation labels only.
- `_sass/jekyll-theme-minimal.scss`: Editorial Experience Ledger layout and responsive behavior.
- `_config.yml`: consulting-first title and description without organization names.
- `README.md`: documents anonymization and the project front-matter contract.

### Task 1: Enforce The Public-Content Boundary

**Files:**
- Create: `scripts/test_public_content.py`
- Modify: `script/cibuild`

**Interfaces:**
- Consumes: a repository/public-site root supplied as `--root PATH`.
- Produces: exit 0 when forbidden organization names are absent and approved homepage proof is present; non-zero with exact offending file paths otherwise.

- [ ] **Step 1: Write the failing privacy test**

Create `scripts/test_public_content.py` with standard-library `argparse`, `pathlib`, and `unittest`. Its public API is:

```python
FORBIDDEN_NAMES = (
    "sagesure", "ishir", "cannasp yglass".replace(" ", ""), "petfolk",
    "tradetips", "casepoint", "nhs", "archetypal ai", "6overn.ai",
)

SOURCE_PATHS = (
    Path("index.md"), Path("work.md"), Path("_config.yml"),
    Path("_layouts"), Path("_projects"),
)

def public_text_files(root: Path) -> list[Path]:
    if (root / "index.md").exists():
        paths = SOURCE_PATHS
        suffixes = {".md", ".html", ".yml", ".yaml"}
    else:
        paths = (Path("."),)
        suffixes = {".html", ".xml", ".txt"}
    files = []
    for relative in paths:
        candidate = root / relative
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*") if path.suffix in suffixes)
    return sorted(files)

def find_forbidden_names(root: Path) -> list[str]:
    findings = []
    for path in public_text_files(root):
        text = path.read_text(encoding="utf-8").casefold()
        for name in FORBIDDEN_NAMES:
            if name in text:
                findings.append(f"{path}: {name}")
    return findings
```

Add tests for source discovery, case-insensitive detection, and a clean temporary directory. Add a CLI `main()` that accepts `--root`, prints each finding, and returns 1 when findings exist. When scanning generated `_site`, additionally require the homepage HTML to contain `300+`, `2M+`, `7+ years`, and `Open to select strategic leadership roles`.

- [ ] **Step 2: Run the test and prove the current site violates the rule**

Run:

```bash
pytest -q scripts/test_public_content.py
python scripts/test_public_content.py --root .
```

Expected: unit tests pass; the CLI exits 1 and reports current named employment/client references in `index.md`.

- [ ] **Step 3: Add the generated-site privacy check to CI**

Append this exact command after HTML-Proofer in `script/cibuild`:

```sh
python scripts/test_public_content.py --root _site
```

- [ ] **Step 4: Verify the CI hook is present**

Run:

```bash
rg -n 'test_public_content.py --root _site' script/cibuild
git diff --check
```

Expected: one hook match and no whitespace errors.

- [ ] **Step 5: Commit the privacy guard**

```bash
git add scripts/test_public_content.py script/cibuild
git commit -m "Guard public content anonymity"
```

### Task 2: Build The Anonymized Work Portfolio

**Files:**
- Create: `_projects/regulated-industry-analytics-platform.md`
- Create: `_projects/insurance-data-platform.md`
- Create: `_projects/public-health-risk-data-services.md`
- Create: `_projects/veterinary-inventory-etl.md`
- Create: `_projects/capital-markets-signals-platform.md`
- Create: `_projects/genetics-data-infrastructure.md`
- Modify: `_projects/dubai-real-estate-data-pipeline.md`
- Modify: `work.md`
- Modify: `_layouts/project.html`

**Interfaces:**
- Consumes: Jekyll `site.projects` and the existing `project` layout.
- Produces: `client_work` boolean, `featured` boolean, `order` integer, and display-ready `sector`, `scale`, `role`, `tools`, `summary`, and `outcome` strings for homepage and Work loops.

- [ ] **Step 1: Record failing collection checks**

Run:

```bash
test "$(rg -l '^client_work: true$' _projects/*.md | wc -l)" -eq 6
```

Expected: failure because the six anonymized engagements do not exist.

- [ ] **Step 2: Create the six engagement files**

Use these exact front-matter values:

| Filename | title | summary | sector | scale | role | tools | featured | order | outcome |
|---|---|---|---|---|---|---|---:|---:|---|
| `regulated-industry-analytics-platform.md` | Regulated-industry analytics platform | Cloud ingestion and transformation across regulated-business, geospatial, API, and PDF sources. | Regulated analytics | 300+ production pipelines | Data engineering and platform delivery | Python, SQL, AWS Glue, PySpark, GCP | true | 1 | Built and operated analytics-ready ingestion across APIs, geospatial sources, regulated-business data, and PDFs. |
| `public-health-risk-data-services.md` | Public-health risk data services | Statistical components, pipelines, and backend data services for a public risk application. | Public health | 2M+ people reached | Data science and backend data delivery | R, Python, AWS Lambda, RDS | true | 2 | Supported a public risk application with statistical components, pipelines, and serverless data services. |
| `insurance-data-platform.md` | Insurance analytics data platform | Tested warehouse models, compliance datasets, analytical marts, and scheduled snapshots. | Insurance | Daily and monthly incremental snapshots | Senior data engineering | Redshift, dbt, SQL | true | 3 | Delivered tested fact and dimension models, compliance datasets, analytical marts, and scheduled snapshots. |
| `veterinary-inventory-etl.md` | Multi-location veterinary inventory ETL | A modular package for validated inventory adjustments and weekly releases. | Veterinary healthcare | 46 clinic locations | ETL package delivery | Python, Dagster, AWS, Pydantic | false | 4 | Automated validated inventory adjustments and reproducible weekly releases across all covered locations. |
| `capital-markets-signals-platform.md` | Capital-markets signals platform | Batch and streaming data services for market signals and investment analytics. | Capital markets | Batch and streaming ingestion | Data engineering and team guidance | AWS Glue, Kafka, FastAPI, Aurora, PySpark | false | 5 | Delivered storage, warehouse, ingestion, and signal-processing services while guiding three junior engineers. |
| `genetics-data-infrastructure.md` | Genetics-data infrastructure blueprint | Architecture and access tooling for large-scale precision-medicine research data. | Government research | Designed for 2–20 PB | Data architecture and ingestion delivery | Python, Kafka, NoSQL | false | 6 | Contributed architecture and access tooling for large-scale precision-medicine research data. |

Every file must set `client_work: true` and include these body headings with concise CV-supported prose: `## Context`, `## Challenge`, `## Role`, `## Architecture And Delivery`, `## Validation`, and `## Outcome`. Do not name an organization or add a metric beyond its table row.

- [ ] **Step 3: Classify the existing Dubai project as independent**

Add these values to its front matter:

```yaml
client_work: false
featured: false
order: 20
```

- [ ] **Step 4: Render client engagements and independent work separately**

Replace the project loop in `work.md` with:

```liquid
{% assign client_projects = site.projects | where: "client_work", true | sort: "order" %}
<section aria-labelledby="client-engagements-heading">
  <h2 id="client-engagements-heading">Selected engagements</h2>
  <div class="work-ledger">
  {% for project in client_projects %}
    <article class="work-row">
      <p class="eyebrow">{{ project.sector }} · {{ project.scale }}</p>
      <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
      <p>{{ project.summary }}</p>
      <p class="project-outcome">{{ project.outcome }}</p>
    </article>
  {% endfor %}
  </div>
</section>

{% assign independent_projects = site.projects | where: "client_work", false | sort: "order" %}
<section class="independent-work" aria-labelledby="independent-work-heading">
  <p class="eyebrow">Independent work</p>
  <h2 id="independent-work-heading">Public projects</h2>
  {% for project in independent_projects %}
    <article class="work-row work-row-compact">
      <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
      <p>{{ project.summary }}</p>
    </article>
  {% endfor %}
</section>
```

- [ ] **Step 5: Add scale to the shared case-study metadata**

In `_layouts/project.html`, insert this row after Role:

```liquid
{% if page.scale %}<div><dt>Scale</dt><dd>{{ page.scale }}</dd></div>{% endif %}
```

- [ ] **Step 6: Verify portfolio structure and privacy**

Run:

```bash
test "$(rg -l '^client_work: true$' _projects/*.md | wc -l)" -eq 6
test "$(rg -l '^featured: true$' _projects/*.md | wc -l)" -eq 3
! rg -n -i 'sagesure|ishir|cannasp[y]glass|petfolk|tradetips|casepoint|nhs|archetypal ai|6overn\.ai' _projects work.md _layouts/project.html
git diff --check
```

Expected: six client engagements, three homepage features, no forbidden organization matches in portfolio files, and no whitespace errors.

- [ ] **Step 7: Commit the portfolio**

```bash
git add _projects _layouts/project.html work.md
git commit -m "Build the anonymized work portfolio"
```

### Task 3: Implement The Editorial Experience Ledger Homepage

**Files:**
- Modify: `index.md`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: `site.projects` entries where `featured: true`, `site.posts`, and existing testimonials.
- Produces: `.hero-ledger`, `.proof-ledger`, `.capability-index`, `.work-ledger`, `.work-row`, `.testimonial-feature`, `.endorsement-grid`, `.authority-about`, and `.technology-line` patterns.

- [ ] **Step 1: Prove selected layout and proof are absent**

Run:

```bash
! rg -q 'class="hero-ledger"' index.md
! rg -q '300+.*production pipelines' index.md
```

Expected: both checks pass because the selected layout is not implemented.

- [ ] **Step 2: Replace the hero and metrics**

Use this structure at the top of `index.md`:

```html
<section class="hero-ledger">
  <div class="hero">
    <p class="eyebrow">Senior data engineer &amp; AI data platform architect · Dubai</p>
    <h1>Reliable data and governed AI systems—from architecture through production.</h1>
    <p class="hero-copy">I help teams modernize data platforms, automate high-value workflows, and build policy-aware AI systems that remain reliable in production.</p>
    <a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a>
  </div>
  <div class="proof-ledger" aria-label="Selected experience">
    <p><strong>300+</strong><span>production pipelines built and operated</span></p>
    <p><strong>2M+</strong><span>people reached by a public-health application</span></p>
    <p><strong>7+ years</strong><span>across data engineering and AI</span></p>
  </div>
</section>
```

- [ ] **Step 3: Replace service cards with the capability index**

Render three `.capability-row` articles titled `Data platforms`, `Governed AI systems`, and `Delivery leadership`, using the exact capability descriptions from the spec. Keep the section id `services` so existing navigation remains valid.

- [ ] **Step 4: Render the three featured engagements as editorial rows**

Use `site.projects | where: "featured", true | sort: "order"`, limit three, and render sector/scale, title link, summary, and outcome inside `.work-ledger > .work-row`.

- [ ] **Step 5: Recompose testimonials without changing approved wording**

Keep all three existing blockquote texts, names, organization labels, and LinkedIn URLs verbatim. Put Benjamin Harvey in `.testimonial-feature`; put Ivette Basterrechea and Le Zhang in `.endorsement-grid`. Do not associate these endorsements with any case study.

- [ ] **Step 6: Replace named employment history with About and technology copy**

Use this approved content:

```html
<section id="about" class="section authority-about">
  <p class="eyebrow">About</p>
  <h2>Technical depth, delivery focus.</h2>
  <p>Dubai-based senior data engineer and AI data platform architect with 7+ years across governed AI, insurance, public health, regulated analytics, veterinary healthcare, capital markets, and government research.</p>
  <p>UAE Golden Visa holder, available for remote global consulting engagements.</p>
  <p class="technology-line"><strong>Core technology:</strong> Python · SQL · AWS · Redshift · dbt · PySpark · Kafka · FastAPI · Dagster</p>
  <p><a class="secondary-link" href="https://www.linkedin.com/in/ggurjarsocl/">Open to select strategic leadership roles</a></p>
</section>
```

Retain Field Notes and the closing Calendly CTA.

- [ ] **Step 7: Implement the selected responsive layout**

In `_sass/jekyll-theme-minimal.scss`, reuse current tokens and add:

```scss
.hero-ledger {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(14rem, 1fr);
  gap: clamp(2rem, 6vw, 5rem);
  padding-bottom: clamp(3rem, 8vw, 6rem);
}

.proof-ledger { border-top: 3px solid var(--color-accent); }
.proof-ledger p,
.capability-row,
.work-row { border-bottom: 1px solid var(--color-rule); padding: 1.25rem 0; }
.proof-ledger strong,
.proof-ledger span { display: block; }
.proof-ledger strong { font-family: var(--font-display); font-size: 2.25rem; line-height: 1; }
.proof-ledger span { color: var(--color-ink-muted); margin-top: 0.4rem; }

.capability-row,
.work-row {
  display: grid;
  grid-template-columns: minmax(10rem, 1fr) minmax(0, 2fr);
  gap: clamp(1rem, 4vw, 3rem);
}

.capability-row > *, .work-row > * { margin-bottom: 0; }
.testimonial-feature { max-width: var(--reading-width); margin-bottom: 1rem; }
.endorsement-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.technology-line { padding-block: 1rem; border-block: 1px solid var(--color-rule); }
.secondary-link { text-decoration: underline; text-decoration-color: var(--color-accent); }
```

At the existing 48rem breakpoint, collapse `.hero-ledger`, `.capability-row`, `.work-row`, and `.endorsement-grid` to one column. Keep `.nav-links` visible and wrapping.

- [ ] **Step 8: Verify source structure and privacy**

Run:

```bash
rg -n 'hero-ledger|300\+|2M\+|7\+ years|Open to select strategic leadership roles' index.md
rg -n 'grid-template-columns: minmax\(0, 2fr\)|testimonial-feature|technology-line' _sass/jekyll-theme-minimal.scss
python scripts/test_public_content.py --root .
git diff --check
```

Expected: every selected-design hook matches, privacy exits 0, and diff check passes.

- [ ] **Step 9: Commit the selected homepage**

```bash
git add index.md _sass/jekyll-theme-minimal.scss
git commit -m "Revamp the homepage authority narrative"
```

### Task 4: Align Shared Positioning, Documentation, And Production Verification

**Files:**
- Modify: `_config.yml`
- Modify: `_layouts/default.html`
- Modify: `README.md`

**Interfaces:**
- Consumes: the homepage and portfolio contracts from Tasks 2–3.
- Produces: consulting-first SEO, consistent shared-shell positioning, and documented anonymized authoring rules.

- [ ] **Step 1: Record the stale metadata checks**

Run:

```bash
! rg -q 'Senior data engineering and governed AI consulting' _config.yml
! rg -q 'Never include a client or employer name' README.md
```

Expected: both checks pass because the final positioning is absent.

- [ ] **Step 2: Update site metadata and shared footer positioning**

Use:

```yaml
title: Gaurav Gurjar — Senior Data Engineer & AI Data Platform Architect
description: Senior data engineering and governed AI consulting for reliable cloud platforms, policy-aware AI systems, and production delivery.
```

Change the footer positioning sentence to:

```html
Senior data engineering and governed AI consulting—from architecture through production.
```

Keep the existing navigation, Calendly URL, social links, and document shell.

- [ ] **Step 3: Document the public case-study contract**

Update README’s case-study example to include:

```yaml
client_work: true
scale: A defensible scale statement
featured: false
order: 4
```

Add this rule immediately above the example:

```markdown
Never include a client or employer name in a case-study filename, front matter, body, URL, image name, or alternative text. Describe the engagement through industry, scale, role, architecture, and outcome. Named testimonial attributions are the only exception.
```

State that exactly three `featured: true` engagements appear on the homepage.

- [ ] **Step 4: Run source-level verification**

Run:

```bash
pytest -q
python scripts/test_public_content.py --root .
git diff --check
```

Expected: all Python tests pass, privacy exits 0, and diff check passes.

- [ ] **Step 5: Build and validate the generated site**

Run:

```bash
bash script/cibuild
```

Expected: Jekyll build, HTML-Proofer, and the `_site` public-content check all exit 0.

- [ ] **Step 6: Verify generated homepage and portfolio content**

Run:

```bash
rg -n '300\+|2M\+|7\+ years|Open to select strategic leadership roles' _site/index.html
test "$(find _site/work -mindepth 2 -name index.html | wc -l)" -ge 7
```

Expected: all proof statements are present and Work contains at least six anonymized engagements plus the independent project.

- [ ] **Step 7: Commit shared positioning and documentation**

```bash
git add _config.yml _layouts/default.html README.md
git commit -m "Align the authority site positioning"
```

## Deferred Work

- Do not add a downloadable CV; add it only if consulting prospects request it.
- Do not add more technology badges; the compact line is sufficient until usability evidence says otherwise.
- Do not add more case studies until a new engagement has defensible public facts and passes the anonymization rule.
- Keep the current Insights archive thresholds: year grouping around 30–40 posts and pagination around 100 posts or measured degradation.
