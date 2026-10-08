---
name: progress-analyzer
description: "Convert normalized GitHub activity into meaningful, named progress: classify each change and answer what changed, why it mattered, what problem it solved, what is now possible, and what remains unfinished. Use after github-progress-collector and before technical-blog-writer."
---

# Progress Analyzer

This is the stage that stops the blog from becoming *"this week I made 17 commits."* It turns
activity into named developments with meaning.

Input: the normalized activity model from `github-progress-collector`.
Output: a structured analysis JSON that is the **only** material `technical-blog-writer` may draw from.

## Classify every meaningful change

Assign one primary class (and optional secondary) from:

| Class | Meaning |
|---|---|
| `NEW_CAPABILITY` | Something that did not exist before and is now possible |
| `IMPROVEMENT` | Made an existing thing better (speed, clarity, robustness) |
| `BUG_FIX` | Corrected incorrect behavior |
| `RESEARCH` | Investigation, spike, evaluation, benchmarking |
| `ARCHITECTURE` | Restructuring of boundaries, data flow, or interfaces |
| `DATA` | Datasets, schemas, ingestion, quality, modeling |
| `AI` | Models, prompts, retrieval, evaluation of AI systems |
| `DOCUMENTATION` | README/docs/specs that carry real knowledge |
| `MAINTENANCE` | Dependencies, chores, refactors with no user-visible change |
| `EXPERIMENT` | Throwaway exploration, negative results |

## Answer the five questions for each item

For every candidate, write:

1. **What changed?** — concrete, specific (name the module, dataset, endpoint, pipeline stage).
2. **Why did it matter?** — the consequence, not the activity.
3. **What problem was being solved?** — the tension or failure that prompted the work.
4. **What is now possible that wasn't before?** — the new capability/state.
5. **What remains unfinished?** — follow-ups, known gaps, blocked items.

If you cannot answer (2) and (4) from evidence, the item is **maintenance**, not progress — demote it.

## Collapse into 2–5 developments

Raw activity maps to a small number of coherent developments. Example:

> Input: 12 commits, 3 refactors, 1 bug fix, 1 new dataset, 1 architecture change
> Analysis:
> - **Added regulatory document ingestion** — `DATA` + `NEW_CAPABILITY`
> - **Introduced normalized document metadata** — `ARCHITECTURE`
> - **Improved dataset validation** — `IMPROVEMENT`
> - **Fixed duplicate-document handling** — `BUG_FIX`

Rank developments by significance: `NEW_CAPABILITY` / `ARCHITECTURE` / `DATA` / `AI` > `IMPROVEMENT` /
`BUG_FIX` / `RESEARCH` > `DOCUMENTATION` > `MAINTENANCE` / `EXPERIMENT`. Keep the top 2–5; the rest
goes into "what's next" or is dropped.

## Output schema

```json
{
  "period": {"since": "YYYY-MM-DD", "until": "YYYY-MM-DD"},
  "headline": "One sentence: the week's most important outcome.",
  "developments": [
    {
      "name": "Added regulatory document ingestion",
      "classes": ["NEW_CAPABILITY", "DATA"],
      "what_changed": "...",
      "why_it_mattered": "...",
      "problem_solved": "...",
      "now_possible": "...",
      "unfinished": "...",
      "evidence": ["https://github.com/<owner>/<repo>/commit/<sha>", "..."]
    }
  ],
  "maintenance": ["dependency bumps and formatting — not counted as progress"],
  "discarded_as_churn": 9,
  "open_threads": ["..."]
}
```

## Rules

- Every development must cite at least one GitHub artifact in `evidence` (commit/PR/release URL).
- Never invent a development that has no supporting activity.
- "What is now possible" must be a capability claim you can defend from the diff, not aspiration.
- Prefer numbers that exist in the data (files, endpoints, datasets, tests). Never fabricate numbers.
- Redact secrets; do not expose private-repo details in the analysis.
