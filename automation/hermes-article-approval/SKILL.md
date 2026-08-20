---
name: personal-article-approval
description: Documents the deterministic Hermes gateway plugin for personal-site article approvals.
---

# Personal-site Article Approval Plugin

This directory is installed as the opt-in Hermes plugin
`personal_article_approval`, not as an agent skill. Its supported
`pre_gateway_dispatch` hook handles an approval before any language model runs.

The hook accepts only an authorized Telegram text update whose normalized and raw
text are identical and whose complete text matches one of:

- `APPROVE <draft-id>`
- `REJECT <draft-id>`

It passes lowercase UTF-8 hex to the canonical `decision-hex` coordinator with
`asyncio.create_subprocess_exec`. Raw message text is never shell input or a process
argument. The existing Hermes gateway delivers the result and the original event is
skipped, so there is no second Telegram listener or agent fallback on this path.
