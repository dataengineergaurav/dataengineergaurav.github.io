---
title: "Second Brain Wiki"
layout: "wiki"
tags: ["automation", "cron", "hermes", "meta", "wiki"]
visibility: "public"
created: "2026-10-06"
updated: "2026-10-06"
summary: "Personal 'second brain' wiki whose daily ingest is scheduled and which folds inbox notes into the vault."
---

A living knowledge base that summarizes what I work on, decisions made, and threads left
open — built automatically from agent sessions and personal notes, then curated for the
topics worth publishing.

## How it works

- **Capture** — recent Hermes sessions and notes are summarized incrementally.
- **Synthesize** — an LLM extracts durable, specific knowledge into evergreen pages
  (`subjects/`) and a dated log (`daily/`), merging into existing topics instead of
  duplicating.
- **Curate** — every page is private by default; only pages explicitly marked
  `visibility: public` appear here.
- **Publish** — the public subset is rebuilt into this site daily.

## Why

Most engineering knowledge is lost in chat scrollback. This keeps the useful residue —
architecture choices, trade-offs, and open questions — in one searchable place.

## 2026-10-06 — update

Personal "second brain" wiki.

### Ingest

- Runs daily at **03:30 UTC** via the **Hermes gateway cron job** (decided at launch).
- Personal notes dropped in `inbox/` are folded into the vault on the next ingest.

### Log

- 2026-10-06: seed note "second brain launch" captured.
