---
title: "Second Brain Wiki"
layout: "wiki"
tags: ["meta", "wiki", "hermes"]
visibility: "public"
created: "2026-10-06"
updated: "2026-10-06"
summary: "How this wiki works: a private, LLM-maintained knowledge base synthesized from Hermes sessions and notes, with a curated public subset."
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
