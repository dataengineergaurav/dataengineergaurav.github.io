# Personal Site Cleanup & Growth — Design

Date: 2026-08-19
Status: Approved
Approach: B — Convert the forked jekyll-theme-minimal repo into a clean GitHub Pages user site.

## Context

The repo is currently the *theme gem source* itself: it ships a gemspec,
a publish-gem workflow (can push to RubyGems), theme docs, and template
branding ("Theme by orderedlist", "View the Project on GitHub"). The
site should be a personal portfolio + blog, not a publishable theme.

Recent commits show deliberate pruning of the homepage (email, location,
socials removed, featured projects cut). The README still claims a
"Featured projects" portfolio section that no longer exists.

## Goals

Phased: (1) solid foundation now, (2) blog layer with 3–5 planned posts,
(3) SEO + distribution layered on top.

## Phase 1 — Foundation

### 1a. Repo cleanup
- Delete gem-publishing layer: `jekyll-theme-minimal.gemspec`,
  `.github/workflows/publish-gem.yml`, `.travis.yml`, `script/`, theme
  `docs/` (theme docs), `another-page.md`.
- Rewrite `Gemfile` to depend on the `github-pages` gem; drop `gemspec`.
- Keep vendored `_layouts/`, `_includes/`, `_sass/`, `assets/` — already
  local, no theme gem needed at runtime.
- Localize `_layouts/default.html`: remove "Theme by orderedlist" footer,
  `is_project_page`/`is_user_page` header links, `show_downloads` block.
  Keep `scale.fix.js` (responsive layout).
- `_config.yml`: set `url`, `title`, `description`, `author`, `social`,
  `google_analytics`, `plugins: [jekyll-seo-tag, jekyll-sitemap]`.
- Update `README.md` to the cleaned structure.

### 1b. Homepage polish
- Tighten the About block in `index.md` (2–3 lines + skills).
- Add a `_projects/` collection; each project is a YAML-front-matter file
  (title, context, role, tools, outcome). Source material is off-GitHub
  case studies written by the owner.
- Render project cards on the homepage; clean up the contact block.

### 1c. SEO + sharing
- `{% seo %}` already present in the template; configure via `_config.yml`
  (title template, canonical, Person JSON-LD, social links, OG image).
- Add `sitemap.xml` (jekyll-sitemap plugin) and `robots.txt`.
- OG/favicon assets built from existing `thumbnail.png`.

### 1d. Build & QA
- Add `html-proofer` to the Gemfile; `script/cibuild` builds + link-checks.
- Keep `ci.yaml` building on push/PR.
- Verify the live Pages URL after deploy.

## Phase 2 — Content
- 3–5 planned posts, written in the owner's voice.
- Add a `categories`/`tags` taxonomy for the post list.

## Phase 3 — Distribution
- Content strategy: cross-post excerpts to X/LinkedIn; homepage CTAs.

## Verification
- `bundle exec jekyll build` passes locally.
- `htmlproofer` reports zero broken links.
- Deployed site smoke-tested after each release.

## Non-goals
- No full redesign or stack swap (contradicts "minimal, no bloat").
- No new analytics beyond the existing `google_analytics` field.