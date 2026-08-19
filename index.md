---
layout: default
title: Gaurav Gurjar — Data Engineer
---

## About

I'm Gaurav — a socio-technical data engineer in Dubai focused on delivering autonomous value through robust analytics and reliable data. I design ETL/ELT pipelines, automate data workflows, write clean Python and SQL, and turn raw data into usable insights — as an engineer, a team lead, and a freelancer serving clients across industries.

## Services

- IT Consulting, Data Reporting, Business Analytics
- SaaS Development, Database Development, Custom Software Development

## Skills

- **Languages & Tools**: Python, SQL, R, Excel, Streamlit
- **Data Engineering**: ETL/ELT pipelines, data automation, orchestration, real-time data, data lakes & warehousing
- **Data Quality**: Validation, cleaning, and transformation at scale
- **Cloud & Big Data**: AWS (Glue, S3, RDS, Aurora, Redshift), GCP, PySpark, Airflow, Dagster, dbt

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

## Recommendations

> "Gaurav Gurjar is a fantastic Cross-Cloud Data Engineer and an even better teammate. I had the opportunity to work with Gaurav on building scalable data pipelines using AWS Glue and Redshift. He brings deep expertise in data engineering, a strong understanding of cloud technologies, and excellent problem-solving skills. As my Team Lead, Gaurav has been a great mentor and leader."
>
> — Raja Ram S, AWS Glue & Redshift pipelines

> "I worked with Gaurav on several projects, he has strong technical skills and is also a good team player. He was able to deliver high-quality work and found solutions to difficult problems. Being collaborative, communicative, and always willing to jump in and help."
>
> — Le Z., project collaboration

## Thoughts (posts)

{% for post in site.posts %}
- <a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %Y" }}
{% endfor %}

## Contact

- **GitHub**: [dataengineergaurav](https://github.com/dataengineergaurav)
- **X**: [@dubaidataguy](https://x.com/dubaidataguy)
- **LinkedIn**: [ggurjarsocl](https://www.linkedin.com/in/ggurjarsocl/)
- **Medium**: [gauravgurjar.medium.com](https://gauravgurjar.medium.com/)
- **Calendly**: [Book a 15-min call](https://calendly.com/gauravgurjar/15min)