---
title: "Dubai Real Estate Data Pipeline"
tools: Python, MongoDB, REST API
order: 1
---

An end-to-end ETL process for Dubai real estate data analysis. Property listings are collected daily from a real estate listing API and dumped to MongoDB with a timestamp. The pipeline uses a data factory abstraction over services like a data crawler, file writer, and MongoDB dumper — built for repeatable daily ingestion.