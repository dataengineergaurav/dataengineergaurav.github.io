# Insights Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scale `/insights/` with six featured articles, topic filtering, and a compact chronological archive without adding pagination prematurely.

**Architecture:** Keep Jekyll as the rendering layer and post front matter as the content source. Liquid generates the featured cards, unique topic controls, and full archive; a tiny progressive-enhancement script filters already-rendered archive rows while CSS extends the existing editorial system.

**Tech Stack:** Jekyll, Liquid, Markdown, SCSS, native browser JavaScript

**Spec:** `docs/superpowers/specs/2026-08-20-insights-archive-design.md`

## Global Constraints

- Keep the current Editorial Authority visual direction and global shell.
- Feature exactly the newest six published posts.
- Render the entire compact archive in the initial HTML.
- Use one normalized `topic` string per post and derive filter choices from content.
- Keep filtering keyboard accessible, expose `aria-pressed`, and preserve visible content without JavaScript.
- Add no dependency, framework, CMS, search, year grouping, or pagination.
- Reconsider year grouping at 30–40 posts and pagination around 100 posts or after measured degradation.

---

## File Map

- `_posts/*.md`: provides the normalized `topic` value used by cards, controls, and archive rows.
- `insights.md`: renders the featured set, derived filters, compact archive, and minimal enhancement script.
- `_sass/jekyll-theme-minimal.scss`: styles the filter controls and compact archive using existing tokens and breakpoint.
- `script/cibuild`: remains the source of truth for the production Jekyll build and HTML validation.

### Task 1: Establish The Topic Contract

**Files:**
- Modify: `_posts/2026-03-21-never-mix-thinking-with-execution.md`

**Interfaces:**
- Consumes: existing Jekyll post front matter.
- Produces: `post.topic`, a display-ready normalized string consumed by `insights.md`.

- [ ] **Step 1: Prove the current post lacks the topic contract**

Run:

```bash
! rg -q '^topic:' _posts/2026-03-21-never-mix-thinking-with-execution.md
```

Expected: exit 0 because no `topic` key exists yet.

- [ ] **Step 2: Add the normalized topic**

Add this key to the post's YAML front matter:

```yaml
topic: Leadership
```

For future posts, choose one concise display value and reuse its exact capitalization; do not add a separate taxonomy file.

- [ ] **Step 3: Verify the front matter is discoverable**

Run:

```bash
rg -n '^topic: Leadership$' _posts/2026-03-21-never-mix-thinking-with-execution.md
```

Expected: one match.

- [ ] **Step 4: Commit the content contract**

```bash
git add _posts/2026-03-21-never-mix-thinking-with-execution.md
git commit -m "Add topic metadata to insights"
```

### Task 2: Build The Scalable Insights Index

**Files:**
- Modify: `insights.md`
- Modify: `_sass/jekyll-theme-minimal.scss`

**Interfaces:**
- Consumes: `site.posts`, `post.title`, `post.date`, `post.summary`, `post.url`, and `post.topic`.
- Produces: `.featured-insights`, `.topic-filters`, `.insights-archive`, filter buttons with `data-topic-filter`, and archive rows with `data-topic`.

- [ ] **Step 1: Record failing generated-page checks**

Run:

```bash
bundle exec jekyll build
! rg -q 'class="topic-filters"' _site/insights/index.html
! rg -q 'class="insights-archive"' _site/insights/index.html
```

Expected: the build passes and both negated searches pass because the scalable index is absent.

- [ ] **Step 2: Render the featured set and derived topic controls**

In `insights.md`, keep the intro and replace the current loop with this Liquid structure:

```liquid
{% assign posts = site.posts | sort: "date" | reverse %}
{% assign topics = posts | map: "topic" | compact | uniq | sort %}

<section aria-labelledby="featured-insights-heading">
  <h2 id="featured-insights-heading">Featured insights</h2>
  <div class="featured-insights">
  {% for post in posts limit: 6 %}
    <article class="insight-card">
      <p class="eyebrow">{{ post.topic }} · {{ post.date | date: "%-d %B %Y" }}</p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.summary }}</p>
      <a class="button" href="{{ post.url | relative_url }}">Read article</a>
    </article>
  {% endfor %}
  </div>
</section>

<section aria-labelledby="all-insights-heading">
  <h2 id="all-insights-heading">All insights</h2>
  <div class="topic-filters" aria-label="Filter insights by topic">
    <button type="button" data-topic-filter="all" aria-pressed="true">All</button>
    {% for topic in topics %}
      <button type="button" data-topic-filter="{{ topic | slugify }}" aria-pressed="false">{{ topic }}</button>
    {% endfor %}
  </div>
```

- [ ] **Step 3: Render every post in the compact archive**

Continue the same section with:

```liquid
  <div class="insights-archive">
  {% for post in posts %}
    <article class="archive-entry" data-topic="{{ post.topic | slugify }}">
      <p class="archive-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ post.topic }}</p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.summary }}</p>
    </article>
  {% endfor %}
  </div>
</section>
```

This intentionally repeats featured posts in “All insights”: the archive remains complete, and filtering always operates on the full library.

- [ ] **Step 4: Add progressive topic filtering**

Append one inline script to `insights.md`:

```html
<script>
  document.querySelectorAll('[data-topic-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      const topic = button.dataset.topicFilter;
      document.querySelectorAll('[data-topic-filter]').forEach((item) =>
        item.setAttribute('aria-pressed', String(item === button)));
      document.querySelectorAll('.archive-entry').forEach((entry) =>
        entry.hidden = topic !== 'all' && entry.dataset.topic !== topic);
    });
  });
</script>
```

With JavaScript disabled, the buttons do nothing and the full server-rendered archive remains visible.

- [ ] **Step 5: Extend the existing responsive styles**

In `_sass/jekyll-theme-minimal.scss`, reuse existing tokens and card rules. Rename the existing `.insights-list` grid selector to `.featured-insights`, include `.insight-card h3` in the existing card-heading rule, then add:

```scss
.topic-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.topic-filters button {
  min-height: 44px;
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--color-rule);
  background: transparent;
  color: var(--color-ink);
  font: inherit;
  cursor: pointer;
}

.topic-filters button[aria-pressed="true"] {
  background: var(--color-accent);
  border-color: var(--color-accent);
}

.archive-entry {
  display: grid;
  grid-template-columns: 10rem minmax(0, 1fr) minmax(14rem, 2fr);
  gap: 1rem;
  padding: 1.25rem 0;
  border-top: 1px solid var(--color-rule);
}

.archive-entry > * { margin: 0; }
.archive-entry h3 { font-size: 1.25rem; }
.archive-meta { color: var(--color-ink-muted); font-size: 0.85rem; }
.archive-entry[hidden] { display: none; }
```

At the existing `max-width: 48rem` breakpoint, add `.featured-insights` to the one-column grid list and collapse archive rows:

```scss
.archive-entry { grid-template-columns: 1fr; gap: 0.35rem; }
```

- [ ] **Step 6: Build and verify structure, metadata, and accessibility hooks**

Run:

```bash
bundle exec jekyll build
rg -n 'Featured insights|class="topic-filters"|aria-pressed="true"|class="insights-archive"|data-topic="leadership"' _site/insights/index.html
rg -n 'min-height: 44px|archive-entry\[hidden\]|grid-template-columns: 10rem' _site/assets/css/style.css
```

Expected: Jekyll succeeds and every expression has at least one match.

- [ ] **Step 7: Run the repository production check**

Run:

```bash
bash script/cibuild
git diff --check
```

Expected: both commands exit 0.

- [ ] **Step 8: Commit the Insights index**

```bash
git add insights.md _sass/jekyll-theme-minimal.scss
git commit -m "Scale the Insights archive"
```

## Deferred Upgrade Checks

- At 30 published posts, review scanning with real content; add year headings only if the list is hard to navigate.
- At 100 published posts, measure generated HTML size and browser rendering; add Jekyll pagination only if the measurement or user behavior warrants it.
- Add search only if topic filtering no longer supports common discovery paths.
