---
layout: default
title: Selected Work
description: Selected data engineering and AI consulting case studies covering platform modernization, automation, and reliable delivery.
permalink: /work/
---

<article class="work-index">
  <header class="work-intro">
    <p class="eyebrow">Case studies</p>
    <h1>{{ page.title }}</h1>
    <p class="lede">A selection of data systems built for repeatable, reliable analysis.</p>
  </header>
  <div class="project-grid">
  {% assign projects = site.projects | sort: "order" %}
  {% for project in projects %}
    <article class="project-feature">
      <p class="eyebrow">{{ project.sector }}</p>
      <h2><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h2>
      <p>{{ project.summary }}</p>
      <p class="project-outcome">{{ project.outcome }}</p>
    </article>
  {% endfor %}
  </div>
</article>
