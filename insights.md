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

<div class="insights-list">
{% assign posts = site.posts | sort: "date" | reverse %}
{% for post in posts %}
  <article class="insight-card">
    <p class="eyebrow">{{ post.date | date: "%-d %B %Y" }}</p>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.summary }}</p>
    <a class="button" href="{{ post.url | relative_url }}">Read article</a>
  </article>
{% endfor %}
</div>
