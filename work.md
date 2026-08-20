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
  {% assign client_projects = site.projects | where: "client_work", true | sort: "order" %}
  <section aria-labelledby="client-engagements-heading">
    <h2 id="client-engagements-heading">Selected engagements</h2>
    <div class="work-ledger">
    {% for project in client_projects %}
      <article class="work-row">
        <p class="eyebrow">{{ project.sector }} · {{ project.scale }}</p>
        <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
        <p>{{ project.summary }}</p>
        <p class="project-outcome">{{ project.outcome }}</p>
      </article>
    {% endfor %}
    </div>
  </section>

  {% assign independent_projects = site.projects | where: "client_work", false | sort: "order" %}
  <section class="independent-work" aria-labelledby="independent-work-heading">
    <p class="eyebrow">Independent work</p>
    <h2 id="independent-work-heading">Public projects</h2>
    {% for project in independent_projects %}
      <article class="work-row work-row-compact">
        <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
        <p>{{ project.summary }}</p>
      </article>
    {% endfor %}
  </section>
</article>
