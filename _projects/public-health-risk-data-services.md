---
title: Public-health risk data services
summary: Statistical components, data pipelines, and serverless backend services behind a public COVID-19 mortality-risk application used by 2M+ people.
sector: Public health
scale: 2M+ people reached
role: Data science and backend data delivery
tools: R, Python, AWS Lambda, RDS
client_work: true
featured: true
order: 2
outcome: Backs a public risk application serving 2M+ people, with serverless services that hold up under real public-load spikes.
---

## Context

An enterprise-AI company whose products embed machine learning inside existing business applications. One of those products was a COVID-19 mortality-risk tool — a public web application where anyone could enter their inputs and see an individual risk estimate.

The substance behind it was an academic mortality model, published as an R package called iCARE. Solid peer-reviewed statistics, delivered as a library that expects a statistician with a local R installation.

## Challenge

Turning a research package into a public service meant building three things that did not exist: the data pipelines that fed it, a statistical component that could run inside a web request, and a backend that would survive traffic from the general public rather than from a handful of researchers.

The core difficulty was that the model was not the product. The product was a number a stranger would act on, and every layer between the R package and that number had to hold up under conditions the research code was never built for.

## Approach

The iCARE R functions were wrapped in Python so the statistical component could be called from a web service instead of an interactive session. Data pipelines were built to feed the model its inputs and keep them current.

The API itself ran serverless on AWS Lambda against an RDS-backed store, so it scaled to demand without standing up capacity for a worst case that would mostly never arrive.

## Result

A public application serving 2M+ people in the United States, backed by serverless data services that held up under real public-load spikes — during a period when demand for the information was both enormous and unpredictable.
