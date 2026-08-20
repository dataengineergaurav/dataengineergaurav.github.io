# CV-Led Personal Authority Revamp Design

## Goal

Reposition Gaurav Gurjar’s personal website as a consulting-first authority site for senior data engineering and governed AI engagements, with a quiet secondary signal that he is open to select strategic leadership roles.

## Selected Design

Use the selected [Editorial Experience Ledger](https://superdesign.dev/teams/6afedad9-c020-4231-bcc2-07c27bb80970/projects/3936e291-d59c-434e-9a1c-ac5594456ddc?node=draft-variant-5c8422e3-0ba6-4df4-be4c-4bf4dcc4b2a3) direction.

Preserve the established Editorial Authority system:

- Warm cream paper canvas with subtle texture.
- Forest-green text, muted green secondary copy, and amber accents.
- Georgia display headings and the existing Avenir/system sans-serif body stack.
- Square editorial surfaces, fine rules, restrained motion, and generous whitespace.
- No new font downloads, gradients, glass effects, portraits, company logos, dashboards, or decorative technology imagery.

## Audience And Conversion

The primary audience is leaders seeking senior consulting help with data platforms, governed AI systems, and delivery. The dominant action remains `Discuss your data challenge`, linking to the existing Calendly URL. Employment positioning appears only as a subdued text link near About: `Open to select strategic leadership roles`.

## Public-Content Rule

Do not publicly name clients, employers, or project organizations anywhere in project or employment narratives. This includes homepage copy, Work pages, metadata, SEO descriptions, URLs, and image alternative text. Describe credibility through industry, scale, architecture, technology, role, and outcome.

Named testimonial authors and their already-public organizations remain visible as explicit endorsements. Do not infer that a testimonial author participated in any anonymized engagement.

## Approved Claims

Use only these leading proof statements:

- `300+` — production pipelines built and operated.
- `2M+` — people reached by a public-health application.
- `7+ years` — across data engineering and AI.
- `46 locations` — covered by a veterinary inventory ETL.
- `2–20 PB` — intended scale of a genetics-data architecture blueprint.
- Guided three junior data engineers.
- UAE Golden Visa holder, Dubai-based, available for remote global consulting engagements.

Remove the current `$3B+ worth of data projects delivered` statement because it is not supported by the supplied CV.

## Homepage Structure

### Global Shell

Retain the sticky header, text brand, navigation, skip link, centered content container, social footer, and primary Calendly CTA. Keep navigation usable at all viewport widths; it may wrap but must not disappear without an accessible replacement.

### Split Hero And Proof Ledger

Use a desktop split: approximately two thirds for the positioning statement and one third for the vertical proof ledger. Collapse to a single column on mobile.

- Eyebrow: `Senior data engineer & AI data platform architect · Dubai`.
- Heading: `Reliable data and governed AI systems—from architecture through production.`
- Supporting copy: explain that Gaurav helps teams modernize data platforms, automate high-value workflows, and build policy-aware AI systems.
- Primary action: `Discuss your data challenge`.
- Proof ledger: the three approved `300+`, `2M+`, and `7+ years` claims.

### Capability Index

Replace equal marketing cards with a slimmer editorial index:

1. `Data platforms` — cloud ingestion, dimensional modeling, quality, incremental processing, and production operations.
2. `Governed AI systems` — knowledge ingestion, policy processing, grounding, routing, provenance, PII controls, and runtime telemetry.
3. `Delivery leadership` — architecture through implementation, stakeholder communication, testing, release discipline, and team guidance.

### Selected Work Ledger

Show three strongest engagements on the homepage as full-width editorial rows with industry, scale, challenge, approach, and outcome. Link each row to an anonymized Work detail page.

1. Regulated analytics: 300+ pipelines across APIs, geospatial sources, regulated-business data, and PDFs using Python, AWS Glue, PySpark, GCP, and SQL.
2. Public health: statistical and backend data services for a risk application used by 2M+ people using R, Python, AWS Lambda, and RDS.
3. Insurance analytics: Redshift fact/dimension models, compliance datasets, dbt tests, integration tests, and incremental snapshots.

### Testimonials

Feature the Benjamin Harvey testimonial as the primary endorsement. Present the Ivette Basterrechea and Le Zhang testimonials as quieter supporting endorsements. Preserve their current approved wording, names, organizations, and LinkedIn links.

### About And Technology

Replace the named chronological employment list with a concise narrative covering seven-plus years across governed AI, insurance, public health, regulated analytics, veterinary healthcare, capital markets, and government research. Mention Dubai, UAE Golden Visa status, and global remote availability.

Use one compact technology line rather than a large skill cloud: Python, SQL, AWS, Redshift, dbt, PySpark, Kafka, FastAPI, and Dagster. Add the subdued strategic-role link here.

### Field Notes And Closing CTA

Retain the latest Insights cards and closing consulting CTA. Keep consulting as the only visually dominant conversion path.

## Work Index And Case Studies

The Work index uses the same editorial-row pattern as the homepage and lists six anonymized engagements:

1. Regulated-industry analytics platform — 300+ production pipelines.
2. Insurance data platform — Redshift/dbt models, compliance data, and snapshots.
3. Public-health risk application — 2M+ people reached.
4. Multi-location veterinary inventory ETL — 46 locations.
5. Capital-markets signals platform — batch and streaming ingestion plus delivery leadership.
6. Genetics-data infrastructure blueprint — designed for 2–20 PB.

Each detail page uses a consistent structure: context, challenge, role, architecture, delivery approach, validation, and outcome. Avoid unsupported causal claims, confidential operational details, invented metrics, or invented results. Existing personal/public projects may remain only if clearly labeled as independent work and visually separated from client engagements.

## Insights

Keep the newly implemented Insights architecture: six newest featured posts, derived topic filters, and a complete compact archive. Update only shared shell or token changes necessary to keep it visually consistent with the selected direction. Do not add pagination, search, or new JavaScript behavior in this revamp.

## Content And SEO

- Refine the site title and description around senior data engineering, governed AI systems, and consulting availability.
- Never include the email address in visible copy unless explicitly requested later; Calendly remains the primary contact path.
- Keep claims specific, defensible, and traceable to the supplied CV.
- Use plain business language before technology lists.
- Do not present the site as a résumé or reproduce the full employment chronology.

## Accessibility And Responsive Requirements

- Preserve semantic landmarks, heading order, skip link, visible keyboard focus, and readable contrast.
- Keep actionable controls at least 44px high.
- Retain all essential content without JavaScript.
- Honor `prefers-reduced-motion`.
- Collapse split and multi-column layouts to one column at the existing 48rem breakpoint.
- Ensure long testimonials, technology lists, and proof labels wrap without horizontal overflow.

## Architecture And Scope

Keep Jekyll, Liquid, Markdown, the existing projects collection, and the existing Sass entry point. Do not add a frontend framework, component library, CMS, analytics dependency, or font package. Reuse the current layouts and theme file unless a small additional Jekyll include materially removes duplication across the new case studies.

## Verification

- Run the article-pipeline Python suite.
- Build with the GitHub Pages dependency set.
- Run HTML-Proofer for links, images, and scripts.
- Assert forbidden organization names are absent from generated public HTML except inside the three approved testimonial attribution blocks.
- Verify the three headline metrics and strategic-role text in generated homepage HTML.
- Check the desktop and mobile page hierarchy against the selected Superdesign draft.
