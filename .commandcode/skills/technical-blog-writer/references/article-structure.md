# Build Log — structure and phrasing guide

## Worked example

Given this analyzer output:

```json
{
  "headline": "The regulatory corpus became a queryable, validated dataset.",
  "developments": [
    {"name": "Added regulatory document ingestion", "classes": ["NEW_CAPABILITY", "DATA"]},
    {"name": "Introduced normalized document metadata", "classes": ["ARCHITECTURE"]},
    {"name": "Improved dataset validation", "classes": ["IMPROVEMENT"]},
    {"name": "Fixed duplicate-document handling", "classes": ["BUG_FIX"]}
  ]
}
```

Write:

```markdown
## The problem

The regulatory corpus was a pile of documents: you could search filenames, but you could not ask
questions of it. Duplicates and inconsistent metadata meant two engineers could get two answers.

## What changed

- Added regulatory document ingestion as a first-class pipeline stage.
- Introduced normalized document metadata, so every document has one shape.
- Improved dataset validation, catching malformed records at ingest instead of at query time.
- Fixed duplicate-document handling so re-ingesting a file is a no-op.

## What I built

...

## GitHub projects

- `owner/regulatory-corpus` — ingestion + validation (commits a1b2c3d, e4f5g6h)
```

## Phrasing rules

- Prefer the outcome over the activity: "so re-ingesting a file is a no-op" beats "refactored dedupe logic".
- One idea per sentence. No marketing adjectives ("seamless", "powerful", "cutting-edge").
- Name real things: files, stages, tables, endpoints, test suites.
- Numbers only when they come from the data; never estimate to sound impressive.
- "What didn't work" is mandatory honesty — a dead end that saved a week is a real contribution.

## Front matter limits

- `title` <= 200 chars, specific.
- `summary` / `description` <= 300 chars each.
- `topic` is always `Build Log`.

## Word budget

350–900 words. Aim for ~600. If the development list is thin, keep it short rather than padding —
a quiet week produces a short, honest post.
