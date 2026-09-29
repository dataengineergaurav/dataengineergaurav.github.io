---
title: Multi-location veterinary inventory ETL
summary: A modular ETL package that validates inventory adjustments and mappings across 46 clinic locations, on reproducible weekly releases.
sector: Veterinary healthcare
scale: 46 clinic locations
role: ETL package delivery
tools: Python, Airflow, FastAPI, Pydantic, boto3
client_work: true
featured: false
order: 4
outcome: Automated validated inventory adjustments and reproducible weekly releases across all covered locations.
---

## Context

A membership veterinary-care network running in-person clinics alongside virtual care. Membership is what shapes the data problem: a patient may be seen at one location and treated at another, so stock does not belong to a clinic in the way a shop's inventory does. It belongs to the network, reconciled across all of them.

Forty-six clinic locations were feeding inventory movements into the central record, each through systems that identified locations their own way.

## Challenge

The source systems did not agree on how a location was identified, so adjustments could not be applied to the wrong clinic or, worse, silently dropped. Every exception had to be handled deliberately rather than by a retry that quietly discarded it.

The second problem was proving coverage. A weekly release that processed forty-five of forty-six locations was indistinguishable from a successful run unless something checked it — and clinic-operations decisions run on those numbers, where a missed location becomes a physical stock error.

## Approach

The work was a modular ETL package rather than a single job. Pydantic handled typed validation at the boundary, so malformed API responses failed loudly at the edge instead of propagating into the warehouse. boto3 and the API integrations covered the source pulls.

Airflow orchestrated the whole thing on a weekly schedule, keeping the release reproducible — the same inputs produce the same adjustments, run after run.

Coverage was validated explicitly: location mappings were checked against the full clinic set before anything was published, and data exceptions were handled rather than discarded.

## Result

Automated, validated inventory adjustments and reproducible weekly releases across all covered locations. Coverage is proven at publish time rather than assumed, and a bad source response stops the run instead of quietly removing a clinic from it.
