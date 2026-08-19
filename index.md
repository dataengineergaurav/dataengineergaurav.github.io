---
layout: default
title: Gaurav Gurjar — Data Engineer
---

<div class="hero">
  <span class="eyebrow">Data Engineer · Dubai, UAE</span>
  <h1>Gaurav Gurjar</h1>
  <p class="lead">Socio-technical data engineer delivering autonomous value through robust analytics, reliable data infrastructure, and strong governance. I design scalable pipelines, lead AI agent systems, and turn complex data into actionable insights.</p>
  <div class="cta">
    <a class="btn btn-primary" href="#experience">View experience</a>
    <a class="btn btn-outline" href="#contact">Get in touch</a>
  </div>
</div>

<section id="about">
## About

I focus on delivering autonomous value through robust analytics, reliable data infrastructure, and strong governance. By fostering a small, high-leverage team, I prioritize quality, documentation, and long-term client relationships over quick fixes. I actively contribute to high-stakes projects involving AI agents, data pipelines, and BI models, while promoting data quality, observability, and governance from the outset. My work emphasizes transforming complex data into actionable insights through scalable pipelines, reusable components, and cutting-edge frameworks — building sustainable, reliable systems that enable confident, data-driven decisions.

## Services

- IT Consulting, Data Reporting, Business Analytics
- SaaS Development, Database Development, Custom Software Development
</section>

<section id="experience">
## Experience

<div class="experience">

<div class="job">
  <h3 class="role">Senior Data Engineer</h3>
  <span class="org">ISHIR</span>
  <div class="meta">April 2024 – January 2026 · Dubai, UAE</div>
  <ul>
    <li>Owned the Redshift-based analytics platform for a large US Property & Casualty insurer: scalable ELT pipelines with dbt, S3, Lambda, and AWS Glue for high-volume policy and claims data</li>
    <li>Led delivery of autonomous AI agent systems and governed AWS Bedrock-based data pipelines for Policy and Claims datasets, with measurable efficiency gains and compliance-ready architecture</li>
    <li>Implemented automated data validation and contract testing, significantly reducing data quality incidents and downstream rework</li>
    <li>Designed reusable agent templates, data quality frameworks, and governance patterns for production AI deployments</li>
    <li>Recognized with the Rising Star Award (Jun 2024) and Team Excellence Award (Sep 2024)</li>
  </ul>
</div>

<div class="job">
  <h3 class="role">Senior Business Intelligence Developer</h3>
  <span class="org">SageSure</span>
  <div class="meta">April 2024 – January 2026</div>
  <ul>
    <li>Owned the Redshift analytics platform for a US Property & Casualty insurer: ELT pipelines in dbt, S3, Lambda, and AWS Glue for policy and claims data; Python (PySpark) and SQL in Glue jobs</li>
  </ul>
</div>

<div class="job">
  <h3 class="role">Data Engineer</h3>
  <span class="org">CannaSpyglass</span>
  <div class="meta">April 2021 – March 2024</div>
  <ul>
    <li>Built data pipelines across cannabis wholesalers, transporters, growers, and dispensaries; parsed PDFs and scraped spreadsheets and e-commerce sites (Scrapy, Requests, Selenium) on AWS EC2, Glue, S3, Athena, RDS, and Lambda</li>
    <li>Generated scalable data pipelines and API integrations to support data volume; collaborated with the analytics team to enhance BI tools</li>
  </ul>
</div>

<div class="job">
  <h3 class="role">Data Scientist</h3>
  <span class="org">AISquared</span>
  <div class="meta">May 2020 – March 2021</div>
  <ul>
    <li>Developed backend APIs and statistical models for a COVID-19 risk assessment platform used by over 2 million people</li>
    <li>Designed AWS data architecture (Glue, Step Functions, S3, Athena) and scalable ELT pipelines for high-volume medical datasets</li>
  </ul>
</div>

<div class="job">
  <h3 class="role">Assistant Project Manager</h3>
  <span class="org">Casepoint LLC</span>
  <div class="meta">August 2018 – April 2020 · Surat</div>
  <ul>
    <li>Delivered high-value data projects exceeding $1M in revenue; designed data strategies, warehousing solutions (SQL/NoSQL), and storage management plans</li>
    <li>Automated data-driven reports and analysis tasks with Excel macros; streamlined workflows with Agile/Scrum sprints</li>
  </ul>
</div>

</div>
</section>

<section id="projects">
## Projects

{% assign visible = site.projects | where: "draft", false | sort: "order" %}
{% if visible.size > 0 %}
<div class="project-grid">
{% for project in visible %}
<div class="project">
  <h3>{{ project.title }}</h3>
  {% if project.tools %}<span class="tools">{{ project.tools }}</span>{% endif %}
  {{ project.content }}
</div>
{% endfor %}
</div>
{% else %}
*Case studies coming soon.*
{% endif %}

## Skills

<ul class="skill-list">
  <li><strong>Languages &amp; Tools</strong> — Python, SQL, R, Excel, Streamlit</li>
  <li><strong>Data Engineering</strong> — ETL/ELT pipelines, data automation, orchestration, real-time data, data lakes &amp; warehousing</li>
  <li><strong>Data Quality</strong> — Validation, contract testing, cleaning, and transformation at scale</li>
  <li><strong>Cloud &amp; Big Data</strong> — AWS (Glue, S3, RDS, Aurora, Redshift, Lambda, Athena, Bedrock), GCP, PySpark, Airflow, Dagster, dbt, MongoDB</li>
  <li><strong>AI &amp; Agents</strong> — Autonomous AI agent systems, AWS Bedrock pipelines, agent templates, governance patterns</li>
  <li><strong>Languages</strong> — Gujarati (native), English (native/bilingual), Hindi (full professional), Arabic (elementary)</li>
</ul>

## Certifications & Education

- **Data Engineering Professional Certificate (V2)** — IBM
- **Data Warehouse Engineer** — IBM
- **Data Engineer** — IBM
- **Dagster & dbt**
- **UAE AI Camp Certificate 2024**
- **Bachelor of Computer Applications** — Dr. Babasaheb Ambedkar Open University (2013–2017)
</section>

<section id="recommendations">
## Recommendations

<div class="rec">
  <blockquote>
    <p>"Gaurav Gurjar is a fantastic Cross-Cloud Data Engineer and an even better teammate. I had the opportunity to work with Gaurav on building scalable data pipelines using AWS Glue and Redshift. He brings deep expertise in data engineering, a strong understanding of cloud technologies, and excellent problem-solving skills. As my Team Lead, Gaurav has been a great mentor and leader."</p>
  </blockquote>
  <cite><strong>Raja Ram S</strong> — AWS Data Engineer · worked with Gaurav on the same team</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"I worked with Gaurav on several projects, he has strong technical skills and is also a good team player. He was able to deliver high-quality work and found solutions to difficult problems. Being collaborative, communicative, and always willing to jump in and help."</p>
  </blockquote>
  <cite><strong>Le Zhang</strong> — Data Engineering · worked with Gaurav on the same team</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"Knowing Gaurav for years, I've seen firsthand how exceptional he's in data science and business. He has a rare talent for turning complex data into actionable insights that drive real results. On top of that, his communication skills are outstanding — he makes sure everyone's on the same page, from analysts to executives. What sets him apart is his proactive nature; he's always ahead, spotting opportunities and solving problems before they even arise. Gaurav is a true asset to any team."</p>
  </blockquote>
  <cite><strong>Krunal Parikh</strong> — TeamGrid AI · studied together</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"I had a pleasure of working and collaborating with Gaurav on a cross functional data engineering project. His expertise and excellent project management skills were top notch. As a team member he always brought a positive energy and a can-do attitude. He was very quick to lend a helping hand to support anyone when needed."</p>
  </blockquote>
  <cite><strong>John Bassey</strong> — Data and Software Professional · worked with Gaurav on the same team</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"Gaurav is a very diligent, hardworking and proactive person. He is a very reliable technical guy with expertise in data sciences area. Keen learner and comes up with good ideas."</p>
  </blockquote>
  <cite><strong>Stanly Thomas</strong> — Co-Founder &amp; Managing Director, Stanra Tech Solutions</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"I have worked with Gaurav for close to a year and he is a very well rounded, skilled, and innovative data scientist. He has helped me in the development of statistical methods, backend server infrastructure, and data science tasks. Gaurav is not only a great developer but also a great communicator. He has always been very prompt, responsive, and completes tasks on time. He goes above and beyond to ensure that the customer requirements and needs are met. I recommend him to anyone seeking expert level data science services."</p>
  </blockquote>
  <cite><strong>Benjamin Harvey, Ph.D.</strong> — Founder of AI Squared · managed Gaurav directly</cite>
</div>

<div class="rec">
  <blockquote>
    <p>"Gaurav is a thoughtful person with a very creative mind. He is intellectually curious and looks for efficient solutions to any problems. I enjoyed my time working with him and appreciate the collegial relationship we developed. I have great faith that he will achieve success in any career path he pursues."</p>
  </blockquote>
  <cite><strong>Ivette Basterrechea</strong> — Senior Litigation Support Specialist · senior to Gaurav</cite>
</div>
</section>

<section id="contact">
## Contact

<div class="contact-grid">
  <div class="contact-card">
    <a href="https://github.com/dataengineergaurav">GitHub</a>
    <span>@dataengineergaurav</span>
  </div>
  <div class="contact-card">
    <a href="https://www.linkedin.com/in/ggurjarsocl/">LinkedIn</a>
    <span>ggurjarsocl</span>
  </div>
  <div class="contact-card">
    <a href="https://x.com/dubaidataguy">X</a>
    <span>@dubaidataguy</span>
  </div>
  <div class="contact-card">
    <a href="https://gauravgurjar.medium.com/">Medium</a>
    <span>gauravgurjar.medium.com</span>
  </div>
  <div class="contact-card">
    <a href="https://calendly.com/gauravgurjar/15min">Calendly</a>
    <span>Book a 15-min call</span>
  </div>
</div>

## Thoughts (posts)

{% for post in site.posts %}
- <a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%b %Y" }}
{% endfor %}
</section>