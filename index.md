---
layout: default
---

<section class="hero-ledger">
  <div class="hero">
    <p class="eyebrow">Senior data engineer &amp; AI data platform architect · Dubai</p>
    <h1>Reliable data and governed AI systems—from architecture through production.</h1>
    <p class="hero-copy">I help teams modernize data platforms, automate high-value workflows, and build policy-aware AI systems that remain reliable in production.</p>
    <a class="button button-primary" href="https://calendly.com/gauravgurjar/15min">Discuss your data challenge</a>
  </div>
  <div class="proof-ledger" aria-label="Selected experience">
    <p><strong>300+</strong><span>production pipelines built and operated</span></p>
    <p><strong>2M+</strong><span>people reached by a public-health application</span></p>
    <p><strong>7+ years</strong><span>across data engineering and AI</span></p>
  </div>
</section>

<section id="services" class="section">
  <p class="eyebrow">Capabilities</p>
  <h2>Make complex systems dependable.</h2>
  <div class="capability-index">
    <article class="capability-row">
      <h3>Data platforms</h3>
      <p>Cloud ingestion, dimensional modeling, quality, incremental processing, and production operations.</p>
    </article>
    <article class="capability-row">
      <h3>Governed AI systems</h3>
      <p>Knowledge ingestion, policy processing, grounding, routing, provenance, PII controls, and runtime telemetry.</p>
    </article>
    <article class="capability-row">
      <h3>Delivery leadership</h3>
      <p>Architecture through implementation, stakeholder communication, testing, release discipline, and team guidance.</p>
    </article>
  </div>
</section>

<section id="work" class="section">
  <p class="eyebrow">Selected work</p>
  <h2>Systems built for repeatable decisions.</h2>
  <div class="work-ledger">
{% assign featured_projects = site.projects | where: "featured", true | sort: "order" %}
{% for project in featured_projects limit: 3 %}
    <article class="work-row">
      <p class="eyebrow">{{ project.sector }} · {{ project.scale }}</p>
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
  <div class="rec testimonial-feature">
    <blockquote>
      <p>"I have worked with Gaurav for close to a year and he is a very well rounded, skilled, and innovative data scientist. He has helped me in the development of statistical methods, backend server infrastructure, and data science tasks. Gaurav is not only a great developer but also a great communicator. He has always been very prompt, responsive, and completes tasks on time. He goes above and beyond to ensure that the customer requirements and needs are met. I recommend him to anyone seeking expert level data science services."</p>
    </blockquote>
    <cite><strong><a href="https://www.linkedin.com/in/benjaminsharvey/">Benjamin Harvey, Ph.D.</a></strong> · Founder of AI Squared</cite>
  </div>
  <div class="endorsement-grid">
    <div class="rec">
      <blockquote>
        <p>"Gaurav is a thoughtful person with a very creative mind. He is intellectually curious and looks for efficient solutions to any problems. I enjoyed my time working with him and appreciate the collegial relationship we developed. I have great faith that he will achieve success in any career path he pursues."</p>
      </blockquote>
      <cite><strong><a href="https://www.linkedin.com/in/ivette-basterrechea-a17ab23/">Ivette Basterrechea</a></strong> · Department of Justice</cite>
    </div>
    <div class="rec">
      <blockquote>
        <p>"I worked with Gaurav on several projects, he has strong technical skills and is also a good team player. He was able to deliver high-quality work and found solutions to difficult problems."</p>
      </blockquote>
      <cite><strong><a href="https://www.linkedin.com/in/lzhang149/">Le Zhang</a></strong> · Google</cite>
    </div>
  </div>
</section>

<section id="about" class="section authority-about">
  <p class="eyebrow">About</p>
  <h2>Technical depth, delivery focus.</h2>
  <p>Dubai-based senior data engineer and AI data platform architect with 7+ years across governed AI, insurance, public health, regulated analytics, veterinary healthcare, capital markets, and government research.</p>
  <p>UAE Golden Visa holder, available for remote global consulting engagements.</p>
  <p class="technology-line"><strong>Core technology:</strong> Python · SQL · AWS · Redshift · dbt · PySpark · Kafka · FastAPI · Dagster</p>
  <p><a class="secondary-link" href="https://www.linkedin.com/in/ggurjarsocl/">Open to select strategic leadership roles</a></p>
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
