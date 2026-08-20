# Pages

## Insights dependency tree

`insights.md`
→ `_layouts/default.html`
→ `_includes/head-custom.html`
→ `assets/css/style.scss`
→ `_sass/jekyll-theme-minimal.scss`

Article links resolve to `_posts/*.md`, rendered through `_layouts/post.html`.

Current Insights structure: editorial intro followed by a two-column `.insights-list`; every post is rendered as a large `.insight-card` containing date, linked title, summary, and “Read article” action. It collapses to one column below 48rem.
