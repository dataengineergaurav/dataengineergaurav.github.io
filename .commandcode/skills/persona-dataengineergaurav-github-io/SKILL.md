---
name: persona-dataengineergaurav-github-io
description: dataengineergaurav.github.io persona - the domain and technical context for a Jekyll consulting site on data engineering and governed AI. Use whenever working in this repository, changing its content, templates or styles, or answering questions about how the site is built and published.
---

# dataengineergaurav.github.io — Persona

A static Jekyll site that markets senior data engineering and governed-AI consulting. It is a
lead-generation asset: anonymized case studies, capability and services messaging, a blog, an
ingested wiki, and a downloadable CV. It is not an application; almost every change is content,
template, or style.

## Domain knowledge

- **Purpose and outcome:** convert senior data and AI leaders into consulting conversations by
  demonstrating delivery through specific, defensible case studies rather than adjectives.
- **Audience / users:** senior data and AI leaders evaluating consulting engagements. Write for
  a technical decision-maker who is skimming for evidence.
- **Vocabulary:** engagements are described by `sector`, `scale`, `role`, `tools` and `outcome`.
  Articles carry one `topic` from `Data Platforms`, `AI Governance`, `Analytics Delivery`,
  `Leadership`, or `Build Log`. See `README.md` for the canonical authoring guide.
- **Rules and constraints:**
  - **Never name a client or employer** in a filename, front matter, body, URL, image name, or
    alt text. Describe work through industry, scale, role, architecture and outcome. Named
    testimonial attributions are the only exception — and the published CV, which names its
    employers-of-record and its client-work index roster by the owner's decision.
  - CI enforces this: `scripts/test_public_content.py` scans the built site for forbidden
    organization names and retired claims, and requires the homepage proof points to remain.
  - No unsupported production, performance or scale claims. Prefer numbers already present in
    the evidence over new ones.
- **Key artifacts:** `_projects/*.md` case studies (exactly three `featured: true`, homepage
  order by `order`), `_posts/*.md` articles, `work.md` (`/work/`), `insights.md` (`/insights/`),
  `index.html` (homepage), `credentials.md`, and the committed CV PDF.

## Technical knowledge

- **Stack:** Jekyll via the `github-pages` gem, Ruby + Bundler. Python 3 for the content and
  test scripts. Deployed by GitHub Pages from `master`.
- **Environment:** Jekyll runs through `bundle exec`; scripts run through plain `python3`. This
  project has no `uv`, `npm`, or virtualenv of its own.
- **Commands:**
  - install: `bundle install`
  - build and serve locally: `bundle exec jekyll serve` (`http://localhost:4000`)
  - full verification: `script/cibuild` — Jekyll build + `htmlproofer` + the content policy + the CV
    marker check + the pipeline test suites
  - unit tests: `python3 -m unittest scripts.test_public_content scripts.test_weekly_progress scripts.test_cv_refresh scripts.test_article_pipeline scripts.test_wiki_ingest`
- **Architecture:** static Jekyll site. Collections `projects` (`/work/:name/`) and `wiki`
  (`/wiki/:name/`). Templates in `_layouts/`, fragments in `_includes/`, styles in `_sass/` and
  `assets/`. `_site/` is generated build output. Two local pipelines produce content as pull
  requests: `automation/weekly-progress/` (GitHub activity to a Build Log post **and** a weekly CV
  refresh, driven by eight skills in `.commandcode/skills/`) and `scripts/article_pipeline.py`
  (personal articles with a Telegram approval gate).
- **Entry points:** `index.html`, `_config.yml`, `work.md`, `insights.md`, `_layouts/`,
  `_sass/`, and the two pipeline directories.
- **Conventions:**
  - Front matter contracts. A case study needs `title`, `summary`, `sector`, `role`, `tools`,
    `outcome`, `client_work`, `scale`, `featured`, `order`. A post needs `layout`, `title`,
    `date`, `topic`, `summary`, `description`.
  - Choose `topic` from the fixed vocabulary above; `/insights/` derives its filters from the
    published posts, so the vocabulary must not drift.
  - Content changes arrive as a pull request. The pipelines never push to `master`; merging is
    the approval step and triggers the Pages deploy.
  - When adding a file that must not be published, add it to the `exclude` list in
    `_config.yml`.
- **Gotchas:**
  - A root-level `.md` file, or any file under `docs/` outside `docs/superpowers`, is **published**
    unless excluded. `credentials.md`, `index.html` and the CV PDF are intentionally public.
  - `scrollcraft/` is design scratch, excluded from the build — leave it alone.
  - The `wiki/` collection is a copy ingested from the separate `second-brain` project via
    `scripts/wiki_ingest.py`. Edit upstream, not the copy.
  - The committed CV PDF is a **derived artifact** — `automation/weekly-progress/cv_sync.py`
    regenerates it from the `CV-Development` project and writes its `.version.json` marker. Never
    hand-edit either; `scripts/check_cv_marker.py` fails CI when the two disagree.

## Canonical sources

| What | Where |
| --- | --- |
| How to run | `README.md` |
| Authoring guide for case studies and posts | `README.md` (canonical) |
| Site configuration and exclude list | `_config.yml` |
| Content policy and forbidden names | `scripts/test_public_content.py` |
| Verification gate | `script/cibuild` |
| Headless permissions (shell denied) | `.commandcode/settings.json` |
| Published CV + version marker | `Gaurav_Gurjar_CV_AI-Data-Engineer.{pdf,version.json}` |
| Weekly content pipeline | `automation/weekly-progress/` |
| Agent skills | `.commandcode/skills/` |

Read these; do not restate them here.

## Confirm before trusting

- `TODO: confirm` — whether the site should ever link the `wiki/` collection from primary
  navigation; it is currently reachable but not promoted.
- `TODO: confirm` — the intended naming scheme if the CV PDF is ever renamed (the homepage links
  `Gaurav_Gurjar_CV_AI-Data-Engineer.pdf` by exact filename).

## Guardrails

- Never name a client or employer in site prose, case studies, or posts. The one exception is the
  published CV: its extended render names the employers-of-record and the client-work index roster
  by the owner's decision, so do not "fix" those names.
- Never edit `_site/` or `scrollcraft/`.
- Run `script/cibuild` before declaring a content, template, or style change complete.
- Keep the human-facing guide at
  `.commandcode/skills/persona-dataengineergaurav-github-io/README.md`; it lives beside this
  skill rather than under `docs/` so it is not published.
