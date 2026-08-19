# Gaurav Gurjar — Data Engineer

A clean, minimalist personal portfolio and blog built with Jekyll and GitHub Pages.

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

## Adding a Project

Create a file in `_projects/` with front matter:

```markdown
---
title: "Project Name"
tools: Python, Airflow, AWS
---

Short case study — context, your role, what you built, and the outcome.
```

## Adding a Blog Post

Create a file in `_posts/` with the naming convention `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Post Title"
date: 2026-08-19
categories: [blog, tag-here]
---

Your content here...
```

Posts appear on the homepage in reverse chronological order.

## CI

Every push runs `script/cibuild` in GitHub Actions: Jekyll build + html-proofer
link/image/script checks.

## Contact

- GitHub: [dataengineergaurav](https://github.com/dataengineergaurav)
- X: [@dubaidataguy](https://x.com/dubaidataguy)
- LinkedIn: [ggurjarsocl](https://www.linkedin.com/in/ggurjarsocl/)