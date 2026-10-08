---
name: github-project-context
description: "Provide persistent knowledge about the owner's GitHub repositories so a change is understood against its project's purpose, audience, stack and themes. Use whenever analyzing or writing about repository activity, and to maintain the project catalog."
---

# GitHub Project Context

A single change ("added a DuckDB query layer") only means something relative to the project it
belongs to. This skill supplies that context from `projects.yaml` and tells you how to maintain it.

## Catalog

The catalog is **`projects.yaml`** in this skill directory:

```yaml
<slug>:
  repo: owner/name            # GitHub full_name, if published
  purpose: What this project is for
  audience: Who it serves
  stack: [Python, DuckDB, Parquet, AWS]
  themes: [regulatory data, AI, data engineering]
  links: {site: "", docs: ""}
```

`github-progress-collector` merges `projects.yaml` into each activity pack as `projects_context`.
`technical-blog-writer` uses it so prose frames work as progress on a known project.

## How to use it

- When writing about a repo, look up its slug. If found, frame the change in terms of `purpose`
  and `themes`; if not found, describe it factually without inventing a mission.
- `themes` map to the blog's editorial topics — use them to keep tone and framing consistent with
  the rest of the site.
- Never expose private-repo details in public prose. `private: true` entries are for framing only;
  do not quote their contents, URLs, or identifiers in a published post.

## Maintenance mode

When the collector reports `new_projects` (a repo with first activity in the window) or a repo
appears in `projects_context` as unknown:

1. Add a starter entry with `purpose`, `audience`, `stack`, `themes` inferred from the repo's
   README and this week's diffs.
2. Mark anything uncertain with a `# TODO: confirm` comment rather than guessing.
3. Keep entries short. The catalog is a framing aid, not documentation.

## Guardrails

- This file is data, not a place for prose. Keep it valid YAML.
- Do not add secrets, client names, or private identifiers.
