---
title: "Second Brain Wiki"
layout: "wiki"
tags: ["automation", "cron", "hermes", "knowledge-management", "meta", "second-brain", "wiki"]
visibility: "public"
created: "2026-10-06"
updated: "2026-10-08"
summary: "Personal knowledge wiki ('second brain') topped up daily from agent sessions and notes via wiki_ingest.py."
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

## 2026-10-08 — update

Personal knowledge wiki ('second brain') built by ingesting agent sessions and personal notes.

- Repo: `/root/dataengineergaurav.github.io`.
- `scripts/wiki_ingest.py` with two subcommands: `ingest` (extract durable knowledge into evergreen subject pages + dated daily logs) and `publish --push` (commit/push the generated wiki).
- Daily cron runs both in sequence: `python3 scripts/wiki_ingest.py ingest && python3 scripts/wiki_ingest.py publish --push`, then reports the new subject/daily counts.
- Failure handling: report the last 20 lines of `/root/second-brain/.wiki/ingest.log`.

See blog-automation.
