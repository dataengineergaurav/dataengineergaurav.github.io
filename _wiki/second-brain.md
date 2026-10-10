---
title: "Second Brain Wiki"
layout: "wiki"
tags: ["automation", "cron", "hermes", "ingest", "knowledge-management", "meta", "publishing", "second-brain", "wiki"]
visibility: "public"
created: "2026-10-06"
updated: "2026-10-10"
summary: "The personal second-brain wiki and the script/cron pipeline that ingests sessions and publishes new subject and daily pages."
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

## 2026-10-09 — update

Personal 'second brain' wiki served from the `dataengineergaurav.github.io` GitHub Pages repo.

### Ingest + publish
- Command: `cd /root/dataengineergaurav.github.io && python3 scripts/wiki_ingest.py ingest && python3 scripts/wiki_ingest.py publish --push`
- `publish --push` publishes the generated pages and pushes them.
- Log file: `/root/second-brain/.wiki/ingest.log`; on failure, inspect the last 20 lines.

### Scheduling
Run daily by an "LLM wiki daily ingest" cron job (job id prefix `cron_da4cb247aa1e`, ~03:30). The job reports new subject/daily counts on success and is silent when there is nothing new.

Related: hermes-runtime.

## 2026-10-10 — update

### Repository
- Wiki repo: `/root/dataengineergaurav.github.io`

### Ingest/publish script
- `scripts/wiki_ingest.py` with two subcommands:
  - `ingest` — extract durable knowledge (subjects + daily logs) from sessions/notes.
  - `publish --push` — publish the generated pages and push.
- Typical full run: `cd /root/dataengineergaurav.github.io && python3 scripts/wiki_ingest.py ingest && python3 scripts/wiki_ingest.py publish --push`.

### Logging
- Ingest log: `/root/second-brain/.wiki/ingest.log` (last 20 lines are the expected failure report).

### Scheduling
- Cron job `cron_da4cb247aa1e` (seen 2026-10-10) runs the ingest-then-publish command and reports the **new subject and daily counts**; on failure it reports the last 20 lines of `ingest.log`.

Related: hermes-runtime
