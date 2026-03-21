# Gaurav Gurjar — Data Engineer Portfolio

A clean, minimalist personal portfolio and blog built with Jekyll and GitHub Pages.

## 🚀 Features

- **Portfolio**: Featured projects showcasing data engineering work
- **Blog**: Post articles about data systems, ETL, data quality, and automation
- **Responsive**: Built on the minimal Jekyll theme for fast loading
- **No bloat**: Streamlined directory with only essential files

## 📁 Project Structure

```
.
├── _config.yml              # Site configuration
├── _layouts/                # Jekyll page templates
├── _includes/               # Reusable HTML fragments
├── _posts/                  # Blog posts (YYYY-MM-DD-title.md)
├── _sass/                   # Stylesheet components
├── assets/                  # CSS, fonts, images
├── index.md                 # Homepage
├── Gemfile                  # Ruby dependencies
└── LICENSE
```

## 🎯 Quick Start

### Local Development

```bash
# Install dependencies
bundle install

# Build and serve locally
bundle exec jekyll serve

# Site will be at http://localhost:4000
```

### Add a Blog Post

Create a new file in `_posts/` with the naming convention `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Post Title"
date: 2026-03-21
categories: [blog, tag-here]
---

Your content here...
```

Posts will automatically appear on the homepage in reverse chronological order.

## 🛠️ Configuration

Edit `_config.yml` to customize:

- `title`: Site title
- `description`: Site tagline
- `github_username`: Link to GitHub profile
- `author`: Author metadata

## 📦 Dependencies

- Jekyll 3.9+
- Ruby 2.6+
- github-pages gem (includes Jekyll + plugins)

See `Gemfile` for all dependencies.

## 📄 License

MIT License — See [LICENSE](LICENSE) file.

## 📧 Contact

**Gaurav Gurjar**
- GitHub: [@dataengineergaurav](https://github.com/dataengineergaurav)
- X: [@dubaidataguy](https://x.com/dubaidataguy)
- LinkedIn: [ggurjarsocl](https://www.linkedin.com/in/ggurjarsocl/)
- Email: ggurjar333@gmail.com
