# Editorial rules — failure modes and fixes

| Draft claim | Why it fails | Fix |
|---|---|---|
| "Shipped a production-ready ingestion service." | No deploy evidence; "production-ready" is a usage claim. | "Built the ingestion service and covered it with tests." (evidence: PR + tests) |
| "Improved query performance by 40%." | No benchmark in evidence. | "Added a benchmark harness for the query layer." (or cite the measured number if present) |
| "Upgraded several dependencies." | Maintenance, not progress. | Move to "What's next" / maintenance list. |
| "Now handles 2M documents/day." | No throughput measurement. | "Added batching to the ingest path." |
| "Used the internal `acme-corp` dataset." | Client/private name leak. | Describe by industry/schema: "a regulatory document dataset". |
| "Set `API_KEY=sk-...` in config." | Secret exposure. | Remove entirely. |
| "Added **12** new endpoints." | Number not in evidence. | Only if the diff/analysis contains it; otherwise drop the number. |

## Contract checklist (must all pass)

- [ ] `layout: post`
- [ ] `topic: Build Log`
- [ ] `title` specific, <= 200 chars
- [ ] `summary` and `description` present and <= 300 chars
- [ ] body 350–900 words
- [ ] body has no `# ` H1 heading
- [ ] no CTA text (the layout adds one)
- [ ] no raw HTML, no Liquid (`{{`, `{%`)
- [ ] at least one GitHub artifact link
- [ ] every development maps to analyzer evidence

## Tone

Practical, first-person, specific. No hype adjectives. "What didn't work" should be present and
honest. If the week was quiet, the post is short — that is correct, not a failure.
