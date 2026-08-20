---
layout: default
title: Gaurav Gurjar — Fractional Data Engineering Lead
---

<section class="hero">
  <p class="eyebrow">Fractional data engineering lead · Dubai</p>
  <h1>Turn complex data into systems your business can trust.</h1>
  <p class="hero-copy">I help teams modernize data platforms, automate high-value workflows, and ship governed AI systems—from architecture through production.</p>
  <a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a>
</section>

<section class="proof-grid" aria-label="Selected experience">
  <p><strong>$3B+</strong><span>worth of data projects delivered</span></p>
  <p><strong>2M+</strong><span>users supported by shipped systems</span></p>
  <p><strong>7+ years</strong><span>across data, analytics, and AI</span></p>
</section>

<section id="services" class="section">
  <p class="eyebrow">Services</p>
  <h2>Make the data work move with confidence.</h2>
  <div class="service-grid">
    <article class="service-card">
      <h3>Modernize the platform</h3>
      <p>Build reliable ELT pipelines, warehouse foundations, and data-quality practices that keep analysis dependable as volume grows.</p>
    </article>
    <article class="service-card">
      <h3>Automate with AI</h3>
      <p>Design governed AI workflows with clear policy boundaries, reusable delivery patterns, and production-ready data foundations.</p>
    </article>
    <article class="service-card">
      <h3>Lead delivery</h3>
      <p>Bring architecture, implementation, and stakeholder communication together so important data work reaches production.</p>
    </article>
  </div>
</section>

<section id="work" class="section">
  <p class="eyebrow">Selected work</p>
  <h2>Systems built for repeatable decisions.</h2>
  <div class="project-grid">
{% assign featured_projects = site.projects | where: "featured", true | sort: "order" %}
{% for project in featured_projects limit: 2 %}
    <article class="project-feature">
      <p class="eyebrow">{{ project.sector }}</p>
      <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
      <p>{{ project.summary }}</p>
      <p class="project-outcome">{{ project.outcome }}</p>
    </article>
{% endfor %}
  </div>
</section>

<section class="section">
  <p class="eyebrow">Authority</p>
  <h2>Trusted in the work.</h2>
  <div class="testimonial-grid">
    <div class="rec">
      <blockquote>
        <p>"I have worked with Gaurav for close to a year and he is a very well rounded, skilled, and innovative data scientist. He has helped me in the development of statistical methods, backend server infrastructure, and data science tasks. Gaurav is not only a great developer but also a great communicator. He has always been very prompt, responsive, and completes tasks on time. He goes above and beyond to ensure that the customer requirements and needs are met. I recommend him to anyone seeking expert level data science services."</p>
      </blockquote>
      <cite><strong>Benjamin Harvey, Ph.D.</strong> · Founder of AI Squared · managed Gaurav directly</cite>
    </div>
    <div class="rec">
      <blockquote>
        <p>"Gaurav is a thoughtful person with a very creative mind. He is intellectually curious and looks for efficient solutions to any problems. I enjoyed my time working with him and appreciate the collegial relationship we developed. I have great faith that he will achieve success in any career path he pursues."</p>
      </blockquote>
      <cite><strong>Ivette Basterrechea</strong> · Department of Justice</cite>
    </div>
    <div class="rec">
      <blockquote>
        <p>"I worked with Gaurav on several projects, he has strong technical skills and is also a good team player. He was able to deliver high-quality work and found solutions to difficult problems."</p>
      </blockquote>
      <cite><strong>Le Zhang</strong> · Google</cite>
    </div>
  </div>
</section>

<section id="about" class="section prose">
  <p class="eyebrow">About</p>
  <h2>Technical depth, delivery focus.</h2>
  <p>I work across data engineering, analytics, and governed AI systems, with a focus on the practical foundations that make systems reliable: clear architecture, quality checks, and delivery discipline.</p>
  <h3>Selected experience</h3>
  <ul>
    <li><strong>ISHIR / SageSure</strong> — Senior Data Engineer and Senior Business Intelligence Developer, April 2024–January 2026; overlapping roles for the same client engagement.</li>
    <li><strong>CannaSpyglass</strong> — Data Engineer, April 2021–March 2024.</li>
    <li><strong>AI Squared</strong> — Data Scientist, May 2020–March 2021.</li>
    <li><strong>Casepoint</strong> — Assistant Project Manager, August 2018–April 2020.</li>
  </ul>
</section>

<section class="section">
  <p class="eyebrow">Insights</p>
  <h2>Field Notes</h2>
  <div class="post-grid">
{% for post in site.posts limit: 2 %}
    <article class="post-card">
      <p class="eyebrow">{{ post.date | date: "%b %Y" }}</p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.summary | default: post.excerpt | strip_html | truncate: 150 }}</p>
    </article>
{% endfor %}
  </div>
</section>

<section class="cta-panel">
  <p class="eyebrow">Start a conversation</p>
  <h2>Have a data challenge that has outgrown quick fixes?</h2>
  <a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a>
</section>
