---
layout: default
title: Gaurav Gurjar — Data Engineer
---

## About

I'm Gaurav — a Data Engineer in Dubai building reliable, scalable data systems. I design ETL/ELT pipelines, automate data workflows, write clean Python and SQL, and turn raw data into usable insights.

## Skills

- **Languages & Tools**: Python, SQL, Streamlit
- **Data Engineering**: ETL/ELT pipelines, data automation, orchestration, AI pipelines
- **Data Quality**: Validation, cleaning, and transformation at scale
- **Cloud & Big Data**: AWS, PySpark, Airflow, Dagster, dbt

## Projects

{% assign visible = site.projects | where: "draft", false | sort: "order" %}
{% if visible.size > 0 %}
{% for project in visible %}
<div class="project">
  <h3>{{ project.title }}</h3>
  {% if project.tools %}<small class="tools">{{ project.tools }}</small>{% endif %}
  {{ project.content }}
</div>
{% endfor %}
{% else %}
*Case studies coming soon.*
{% endif %}

## Thoughts (posts)

{% for post in site.posts %}
- <a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %Y" }}
{% endfor %}

## Contact

- **GitHub**: [dataengineergaurav](https://github.com/dataengineergaurav)
- **X**: [@dubaidataguy](https://x.com/dubaidataguy)
- **LinkedIn**: [ggurjarsocl](https://www.linkedin.com/in/ggurjarsocl/)
- **Calendly**: [Book a 15-min call](https://calendly.com/gauravgurjar/15min)