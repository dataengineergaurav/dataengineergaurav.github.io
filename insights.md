---
layout: default
title: Insights
description: Practical guidance for leaders modernizing data platforms, governing AI systems, and improving analytics delivery.
permalink: /insights/
---

<header class="insights-intro">
  <p class="eyebrow">Insights</p>
  <h1>Clearer decisions for data and AI platforms.</h1>
  <p class="lede">Practical notes on building reliable, governable systems that remain understandable as they grow.</p>
</header>

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
  <div class="topic-filters" role="group" aria-label="Filter insights by topic">
    <button type="button" data-topic-filter="all" aria-pressed="true">All</button>
    {% for topic in topics %}
      <button type="button" data-topic-filter="{{ topic | slugify }}" aria-pressed="false">{{ topic }}</button>
    {% endfor %}
  </div>
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
