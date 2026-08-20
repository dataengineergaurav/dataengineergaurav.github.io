# Gaurav Gurjar — Fractional Data Engineering Lead

A Jekyll consulting site for fractional data engineering leadership, reliable platforms, governed AI, and analytics.

## Project Structure

```
.
├── _config.yml              # Site configuration (SEO, social, plugins)
├── _layouts/                # Jekyll page templates
├── _includes/               # Reusable HTML fragments
├── _projects/               # Project case studies (YAML-front-matter files)
├── _posts/                  # Blog posts (YYYY-MM-DD-title.md)
├── _sass/                   # Stylesheet components
├── assets/                  # CSS, fonts, images
├── index.md                 # Homepage
├── Gemfile                  # Ruby dependencies (github-pages)
└── script/cibuild           # Build + link-check script
```

## Quick Start

```bash
# Install dependencies
bundle install

# Build and serve locally
bundle exec jekyll serve

# Site will be at http://localhost:4000
```

## Adding A Case Study

Create a file in `_projects/`. Case studies appear under `/work/`; exactly three `featured: true` engagements appear on the homepage in ascending `order`.

Never include a client or employer name in a case-study filename, front matter, body, URL, image name, or alternative text. Describe the engagement through industry, scale, role, architecture, and outcome. Named testimonial attributions are the only exception.

```markdown
---
title: "Case Study Title"
summary: "One-sentence overview of the work."
sector: Industry or practice area
role: Your delivery role
tools: Python, Airflow, AWS
outcome: "Specific result or operational improvement."
client_work: true
scale: A defensible scale statement
featured: false
order: 4
---

## Problem

Describe the client or operational challenge.
```

## Adding An Article

Create a file in `_posts/` with the naming convention `YYYY-MM-DD-title.md`. Articles are listed under `/insights/`; the homepage features at most two recent articles.

```markdown
---
layout: post
title: "Your Post Title"
date: 2026-08-19
topic: Leadership
summary: "A concise, card-ready summary."
description: "A search and social description for the article."
---

Your content here...
```

Choose one topic from `Data Platforms`, `AI Governance`, `Analytics Delivery`, or `Leadership`.

## CI

Every push runs `script/cibuild` in GitHub Actions: Jekyll build + html-proofer
link/image/script checks.

## Contact

- GitHub: [dataengineergaurav](https://github.com/dataengineergaurav)
- X: [@dubaidataguy](https://x.com/dubaidataguy)
- LinkedIn: [ggurjarsocl](https://www.linkedin.com/in/ggurjarsocl/)
