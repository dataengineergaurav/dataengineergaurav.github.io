---
layout: default
title: Proof of Work
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
    <h2 id="client-engagements-heading">Client work</h2>
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
    <h2 id="independent-work-heading">Maintained projects</h2>
    <article class="work-row work-row-compact">
      <h3><a href="https://github.com/dataengineergaurav/setu">Setu</a></h3>
      <p>A Rust data-activation engine that reacts to PostgreSQL change streams and delivers matching events to webhooks, Slack, or Telegram without polling or middleware.</p>
    </article>
    <article class="work-row work-row-compact">
      <h3><a href="https://github.com/dataengineergaurav/rental-market-dynamics-dubai">Rental Market Dynamics — Dubai</a></h3>
      <p>An automated pipeline for extracting Dubai rent-contract data, transforming it to Parquet, and publishing analysis-ready releases and property-usage reports.</p>
    </article>
    <article class="work-row work-row-compact">
      <h3><a href="https://github.com/dataengineergaurav/hermes-gsheets">Hermes Google Sheets</a></h3>
      <p>A maintained Hermes Agent plugin for reading, searching, and updating Google Sheets through focused spreadsheet tools.</p>
    </article>
    {% for project in independent_projects %}
      <article class="work-row work-row-compact">
        <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
        <p>{{ project.summary }}</p>
      </article>
    {% endfor %}
  </section>

  <section class="independent-work" aria-labelledby="open-source-heading">
    <p class="eyebrow">Contributor work</p>
    <h2 id="open-source-heading">Open-source contributions</h2>
    <article class="work-row work-row-compact">
      <h3>PUDL</h3>
      <p>Submitted upstream work to modernize <a href="https://github.com/catalyst-cooperative/pudl/pull/3931">six test modules from unittest patterns to pytest</a>, move FERC pipelines from <a href="https://github.com/catalyst-cooperative/pudl/pull/3983"><code>SourceAsset</code> toward <code>AssetSpec</code></a>, and iterate on nightly-build cache handling in <a href="https://github.com/catalyst-cooperative/pudl/pull/2951">PR #2951</a> and <a href="https://github.com/catalyst-cooperative/pudl/pull/2953">PR #2953</a>.</p>
    </article>
    <article class="work-row work-row-compact">
      <h3>sportsdataverse-py</h3>
      <p>Submitted an <a href="https://github.com/sportsdataverse/sportsdataverse-py/pull/82">NFL play-by-play analysis example</a> covering field goals, kickoffs, and punts.</p>
    </article>
    <p class="fine-print">These submissions were reviewed upstream and closed without merge.</p>
  </section>
</article>
