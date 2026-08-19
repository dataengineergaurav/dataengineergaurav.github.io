---
layout: default
title: Gaurav Gurjar — Data Engineer
---

## About

I focus on delivering autonomous value through robust analytics, reliable data infrastructure, and strong governance. By fostering a small, high-leverage team, I prioritize quality, documentation, and long-term client relationships over quick fixes. I actively contribute to high-stakes projects involving AI agents, data pipelines, and BI models, while promoting data quality, observability, and governance from the outset. My work emphasizes transforming complex data into actionable insights through scalable pipelines, reusable components, and cutting-edge frameworks — building sustainable, reliable systems that enable confident, data-driven decisions.

## Services

- IT Consulting, Data Reporting, Business Analytics
- SaaS Development, Database Development, Custom Software Development

## Experience

### Senior Data Engineer — ISHIR
*April 2024 – January 2026 · Dubai, UAE*

- Owned the Redshift-based analytics platform for a large US Property & Casualty insurer: scalable ELT pipelines with dbt, S3, Lambda, and AWS Glue for high-volume policy and claims data
- Led delivery of autonomous AI agent systems and governed AWS Bedrock-based data pipelines for Policy and Claims datasets, with measurable efficiency gains and compliance-ready architecture
- Implemented automated data validation and contract testing, significantly reducing data quality incidents and downstream rework
- Designed reusable agent templates, data quality frameworks, and governance patterns for production AI deployments
- Recognized with the Rising Star Award (Jun 2024) and Team Excellence Award (Sep 2024)

### Senior Business Intelligence Developer — SageSure
*April 2024 – January 2026*

- Owned the Redshift analytics platform for a US Property & Casualty insurer: ELT pipelines in dbt, S3, Lambda, and AWS Glue for policy and claims data; Python (PySpark) and SQL in Glue jobs

### Data Engineer — CannaSpyglass
*April 2021 – March 2024*

- Built data pipelines across cannabis wholesalers, transporters, growers, and dispensaries; parsed PDFs and scraped spreadsheets and e-commerce sites (Scrapy, Requests, Selenium) on AWS EC2, Glue, S3, Athena, RDS, and Lambda
- Generated scalable data pipelines and API integrations to support data volume; collaborated with the analytics team to enhance BI tools

### Data Scientist — AISquared
*May 2020 – March 2021*

- Developed backend APIs and statistical models for a COVID-19 risk assessment platform used by over 2 million people
- Designed AWS data architecture (Glue, Step Functions, S3, Athena) and scalable ELT pipelines for high-volume medical datasets

### Assistant Project Manager — Casepoint LLC
*August 2018 – April 2020 · Surat*

- Delivered high-value data projects exceeding $1M in revenue; designed data strategies, warehousing solutions (SQL/NoSQL), and storage management plans
- Automated data-driven reports and analysis tasks with Excel macros; streamlined workflows with Agile/Scrum sprints

## Skills

- **Languages & Tools**: Python, SQL, R, Excel, Streamlit
- **Data Engineering**: ETL/ELT pipelines, data automation, orchestration, real-time data, data lakes & warehousing
- **Data Quality**: Validation, contract testing, cleaning, and transformation at scale
- **Cloud & Big Data**: AWS (Glue, S3, RDS, Aurora, Redshift, Lambda, Athena, Bedrock), GCP, PySpark, Airflow, Dagster, dbt, MongoDB
- **AI & Agents**: Autonomous AI agent systems, AWS Bedrock pipelines, agent templates, governance patterns
- **Languages**: Gujarati (native), English (native/bilingual), Hindi (full professional), Arabic (elementary)

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

## Certifications & Education

- **Data Engineering Professional Certificate (V2)** — IBM
- **Data Warehouse Engineer** — IBM
- **Data Engineer** — IBM
- **Dagster & dbt**
- **UAE AI Camp Certificate 2024**
- **Bachelor of Computer Applications** — Dr. Babasaheb Ambedkar Open University (2013–2017)

## Recommendations

> "Gaurav Gurjar is a fantastic Cross-Cloud Data Engineer and an even better teammate. I had the opportunity to work with Gaurav on building scalable data pipelines using AWS Glue and Redshift. He brings deep expertise in data engineering, a strong understanding of cloud technologies, and excellent problem-solving skills. As my Team Lead, Gaurav has been a great mentor and leader."
>
> — Raja Ram S, AWS Data Engineer · worked with Gaurav on the same team

> "I worked with Gaurav on several projects, he has strong technical skills and is also a good team player. He was able to deliver high-quality work and found solutions to difficult problems. Being collaborative, communicative, and always willing to jump in and help."
>
> — Le Zhang, Data Engineering · worked with Gaurav on the same team

> "Knowing Gaurav for years, I've seen firsthand how exceptional he's in data science and business. He has a rare talent for turning complex data into actionable insights that drive real results. On top of that, his communication skills are outstanding — he makes sure everyone's on the same page, from analysts to executives. What sets him apart is his proactive nature; he's always ahead, spotting opportunities and solving problems before they even arise. Gaurav is a true asset to any team."
>
> — Krunal Parikh, TeamGrid AI · studied together

> "I had a pleasure of working and collaborating with Gaurav on a cross functional data engineering project. His expertise and excellent project management skills were top notch. As a team member he always brought a positive energy and a can-do attitude. He was very quick to lend a helping hand to support anyone when needed."
>
> — John Bassey, Data and Software Professional · worked with Gaurav on the same team

> "Gaurav is a very diligent, hardworking and proactive person. He is a very reliable technical guy with expertise in data sciences area. Keen learner and comes up with good ideas."
>
> — Stanly Thomas, Co-Founder & Managing Director, Stanra Tech Solutions

> "I have worked with Gaurav for close to a year and he is a very well rounded, skilled, and innovative data scientist. He has helped me in the development of statistical methods, backend server infrastructure, and data science tasks. Gaurav is not only a great developer but also a great communicator. He has always been very prompt, responsive, and completes tasks on time. He goes above and beyond to ensure that the customer requirements and needs are met. I recommend him to anyone seeking expert level data science services."
>
> — Benjamin Harvey, Ph.D., Founder of AI Squared · managed Gaurav directly

> "Gaurav is a thoughtful person with a very creative mind. He is intellectually curious and looks for efficient solutions to any problems. I enjoyed my time working with him and appreciate the collegial relationship we developed. I have great faith that he will achieve success in any career path he pursues."
>
> — Ivette Basterrechea, Senior Litigation Support Specialist · senior to Gaurav

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