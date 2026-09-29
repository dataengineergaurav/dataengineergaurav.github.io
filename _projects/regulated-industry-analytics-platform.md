---
title: Regulated market-data ingestion platform
summary: Cloud ingestion and transformation behind 300+ production pipelines, spanning regulated-business records, geospatial sources, APIs, and PDF documents.
sector: Regulated market data
scale: 300+ production pipelines
role: Data engineering and platform delivery
tools: Python, SQL, AWS Glue, PySpark, GCP, FastAPI
client_work: true
featured: true
order: 1
outcome: Runs as the governed ingestion standard behind 300+ production pipelines — auditable, reproducible, and no longer dependent on one-off scripts.
---

## Context

A B2B market-data and analytics platform founded in 2021, selling regulated-industry intelligence to retailers, multi-state operators, and investors. The product was only as good as the data underneath it, and the data arrived in six incompatible shapes: wholesaler records, transporter records, producer records, retailer records, geospatial data pulled from mapping services, and PDF documents that no API would ever expose.

The state at handover was a sprawl of one-off scripts. Each source had its own job, its own credentials, its own idea of what a record meant, and its own failure mode. Nothing could be re-run safely, and nothing could be audited.

## Challenge

Six source families, hundreds of customers, and no contract between any of them. Source schemas changed without notice. PDF documents arrived with no consistent structure. Geospatial data needed normalizing against location hierarchies that varied by market. And the whole thing had to be *operated*, not just built — a pipeline that failed quietly was worse than no pipeline, because downstream analytics had no way to tell the difference.

The requirement was a single ingestion standard that a new source could join without re-inventing the plumbing.

## Approach

Batch ingestion ran on AWS Glue with PySpark for the heavy reshaping. Python and SQL handled the transformation logic. PDF parsing was handled as a first-class source type rather than a bolt-on. Geospatial normalization and the API surface were served through FastAPI services. GCP ran alongside AWS where the workload fit it better.

Every source was brought into the platform through the same path: land, normalize, validate, publish. Adding a source meant writing a source adapter, not another bespoke script.

<div class="architecture-flow">
  <span>Land<br>raw</span>
  <span>Normalize<br>schemas</span>
  <span>Validate<br>&amp; publish</span>
  <span>Serve<br>analytically</span>
</div>

## Result

The platform consolidated wholesalers, transporters, producers, retailers, geospatial sources, and PDFs into one ingestion standard carrying 300+ production pipelines. The output is analytics-ready data, including essential-services location data across the United States, rather than a folder of extracts that each analyst had to interpret differently.
