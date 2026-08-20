# Personal Authority Article Pipeline Design

## Goal

Move automated research-led article publishing from Metteyya Analytics to
`dataengineergaurav.github.io` so each approved article builds Gaurav Gurjar's
personal authority. The personal site becomes the sole publishing destination.

## Scope

The personal-site repository will own the article generator, runtime state,
tests, Telegram approval integration, systemd units, and published Markdown.
The existing Metteyya content remains unchanged, but its article-generator
timer and approval integration will be disabled after the replacement is
verified.

This migration will not create a reusable multi-site framework or publish the
same article to both sites. Metteyya may link to selected personal articles in
the future, but automatic cross-posting is outside this work.

## Content Strategy

The pipeline will continue using recent primary research, including arXiv, as
evidence rather than treating every new paper as an article topic. Candidate
selection will prioritize practical relevance to Gaurav's authority themes:

- reliable data platforms and pipelines;
- analytics and business intelligence;
- governed AI systems;
- data engineering leadership and delivery.

The selector may decline to draft when no candidate is strong enough. Articles
must explain practical implications, limitations, and decisions for technical
or business leaders. They must not invent clients, results, quotations, or
firsthand experience. Primary sources must be attributed and linked.

## Scheduling

A system-level systemd timer will trigger the generator once per week. The
pipeline will retain its own last-draft state so restarts and manual runs do not
create duplicate drafts. Only one timer will be enabled: the personal-site
timer replaces `metteyya-article-generator.timer` after verification.

## Generation and Approval Flow

1. The timer starts the generator in the personal-site repository.
2. The generator acquires its lock and checks that no draft is pending.
3. It verifies that the Git worktree is clean and synchronized with its
   upstream branch.
4. It retrieves recent primary-research candidates and excludes papers already
   used or previously found unreadable.
5. It scores candidates against the personal authority themes and stops cleanly
   if none meets the publication threshold.
6. It retrieves the selected source, generates a Markdown article, and validates
   its structure, length, citations, and safe Markdown rules.
7. It renders a Jekyll post draft and sends the draft plus its decision ID to
   Telegram.
8. Approval materializes the post under `_posts/YYYY-MM-DD-slug.md`, builds the
   Jekyll site, commits the post, and pushes the synchronized branch. Rejection
   records the decision without modifying published content.
9. Retry state preserves an incomplete approval, publication, or notification
   step without creating a second article.

## Jekyll Output

Generated files will follow the site's existing post convention:

```yaml
---
layout: post
title: "Article title"
date: YYYY-MM-DD
summary: "Concise card-ready summary."
description: "Search and social description."
---
```

The body will be Markdown and will end with a references section containing the
primary source. The existing post layout supplies the consulting call to action,
so generated articles will not embed a second CTA or Metteyya-specific fields.

## Repository Changes

The migration will add the minimum proven pieces to this repository:

- the generator and its focused standard-library test suite;
- a setup script for checking, installing, and removing the integration;
- personal-site systemd service and timer units;
- the Hermes approval integration required for Telegram decisions;
- runtime-state exclusions in `.gitignore` if they are not already present.

The current Metteyya implementation will be adapted rather than generalized.
Metteyya-specific paths, branding, Astro front matter, service IDs, content
calendar reads, npm builds, and article destinations will be replaced with the
personal site's Jekyll equivalents.

## Failure Handling

- A dirty, detached, unsynchronized, or upstream-less repository blocks the run
  before a draft is created.
- Network, Codex, Telegram, validation, Jekyll build, Git, or push failures are
  logged and return a failing service status.
- Pending state records the exact draft and publication phase so a later run can
  resume safely.
- Generated Markdown is treated as untrusted input and validated before it can
  enter the repository.
- The old Metteyya timer is disabled only after the personal timer and approval
  flow pass their checks.

## Verification

The existing pipeline tests will be adapted to cover weekly due-state logic,
personal-theme selection context, Jekyll rendering, approval, rejection,
idempotent setup, retry behavior, and guarded Git publication. Verification will
also include shell syntax checks, the Python test suite, a Jekyll production
build through `script/cibuild`, and confirmation that exactly one article timer
is enabled.

No live article will be published during implementation verification. A real
publication remains subject to Telegram approval.
