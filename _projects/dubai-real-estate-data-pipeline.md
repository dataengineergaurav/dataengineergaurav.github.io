---
title: "Dubai Real Estate Data Pipeline"
summary: "A repeatable ingestion pipeline for collecting and analyzing daily Dubai property listings."
sector: Real estate data
role: Data architecture and pipeline delivery
tools: Python, MongoDB, REST API
outcome: "Turned changing listing data into a timestamped dataset ready for repeatable analysis."
client_work: false
featured: false
order: 20
---

## Problem

Dubai property listings change daily, making one-off collection unsuitable for ongoing analysis.

## Approach

The pipeline collects listings from a real estate API each day and records a timestamp with every collection. This establishes a repeatable ingestion process rather than a single static export.

## Architecture

<div class="architecture-flow" role="img" aria-label="Real estate listing API flows through crawler, file writer, and MongoDB dumper services">
  <span>Listing API</span>
  <span>Crawler</span>
  <span>File writer</span>
  <span>MongoDB dumper</span>
</div>

The data factory coordinates the crawler, file-writer, and MongoDB dumper services. Collected listing data is stored in MongoDB with its timestamp.

## Outcome

Changing listing data became a timestamped dataset ready for repeatable analysis.
