---
title: Insurance analytics data platform
summary: Tested warehouse models, compliance datasets, and analytical marts on a fixed daily and monthly cadence, replacing manual extracts behind regulatory filings.
sector: Insurance
scale: Daily and monthly incremental snapshots
role: Senior data engineering
tools: Redshift, dbt, SQL, AWS, pytest
client_work: true
featured: true
order: 3
outcome: Gives compliance and actuarial teams reconciled, trusted marts on a fixed daily and monthly cadence instead of manual extracts.
---

## Context

A residential-property managing general underwriter. Insurance underwriting means premium, exposure, and loss data assembled to regulatory standards, and the numbers land in state filings and internal reporting that both need to survive scrutiny.

The insurance data function had grown one extract at a time. Someone needed the loss triangle, someone else needed the exposure rollup, and each request was assembled by hand from whatever was current that morning. Two analysts asking the same question on the same day could get two answers.

## Challenge

There was no shared model layer underneath those extracts. Compliance datasets were rebuilt per request. Full reloads were the only option, because nothing tracked what had already landed — so the data could not keep up with a daily reporting rhythm, let alone a monthly one.

The requirement was a tested warehouse layer, owned end to end, that produced the same numbers for everyone and could point to how any figure was derived.

## Approach

Amazon Redshift with dbt carried the modeling. Fact and dimension models were built first, then the compliance datasets and analytical marts that reporting actually consumed. dbt data-quality tests enforced correctness at the model boundary, with pytest covering the logic underneath.

Incremental snapshots ran on a daily and monthly cadence with scheduled Redshift automation, so a run processed only what had changed instead of rebuilding the warehouse. Reusable ETL packages and database modules were built beneath the models so the next dataset joined the platform without new bespoke plumbing.

<div class="architecture-flow">
  <span>Source<br>systems</span>
  <span>dbt models<br>&amp; tests</span>
  <span>Incremental<br>snapshots</span>
  <span>Compliance<br>&amp; marts</span>
</div>

## Result

Fact and dimension models, compliance datasets, and analytical marts on a fixed daily and monthly cadence, delivered end to end. Compliance and actuarial teams read from reconciled marts instead of assembling manual extracts, and any figure can be traced to the model and test that produced it.
