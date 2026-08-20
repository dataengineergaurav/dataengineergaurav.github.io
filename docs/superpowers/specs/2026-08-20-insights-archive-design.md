# Insights Archive Design

## Goal

Let the Insights page grow from a handful of posts to a substantial article library while preserving the site's editorial authority and keeping every article discoverable.

## Approved Experience

- Keep the newest six posts as prominent two-column cards.
- Add a compact chronological archive below the featured cards.
- Add topic filters that operate on the complete compact archive.
- Preserve the current cream, forest, amber, serif-led visual system and responsive site shell.
- Keep all archive content visible when JavaScript is unavailable; filtering is progressive enhancement.
- Use post front matter as the single source of truth for topics.

## Content Contract

Each post continues to require `title`, `date`, and `summary`. Add one normalized `topic` string, using a small editorial vocabulary such as `Data Platforms`, `AI Governance`, `Analytics Delivery`, or `Leadership`. The page derives its filter choices from published posts so the navigation cannot drift from the content.

## Responsive and Accessible Behavior

Featured cards remain two columns on wide screens and one column below the existing 48rem breakpoint. Archive entries use semantic articles and links. Filter buttons expose their pressed state, remain keyboard accessible, meet the existing 44px target size, and do not hide content until the enhancement script runs.

## Growth Thresholds

- Add year grouping when the archive reaches roughly 30–40 posts and chronological scanning becomes difficult.
- Add pagination only around 100 posts, or earlier if measured page weight/rendering shows a real regression.
- Defer search, multi-select filters, URL filter state, a CMS, and a frontend framework until demonstrated demand.

## Design Reference

[Superdesign Insights Archive variation](https://superdesign.dev/teams/6afedad9-c020-4231-bcc2-07c27bb80970/projects/31509a9b-132f-4726-b29c-99f2a105d3f4?node=draft-variant-85d67a49-19db-4cba-9873-a53e107f1965)
