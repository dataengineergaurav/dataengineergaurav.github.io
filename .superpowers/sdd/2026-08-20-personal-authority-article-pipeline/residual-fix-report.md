# Residual HTML detector fix

## Changed code

- `scripts/article_pipeline.py`: made `RAW_HTML_RE` reject any apparent raw
  HTML tag opener (`<`, optional whitespace/slash, ASCII letter), before
  attributes are parsed.
- `scripts/test_article_pipeline.py`: added both slash-separated front-matter
  cases (`<svg/onload=alert(1)>`, `<img/src=x onerror=alert(1)>`) and a body
  safe-Markdown regression (`<svg/onload=alert(1)>`).

## TDD evidence

- RED: `python3 -m unittest scripts.test_article_pipeline.PipelineCoreTests.test_article_validation_rejects_active_frontmatter_content scripts.test_article_pipeline.PipelineCoreTests.test_article_validation_rejects_active_html_and_unsafe_urls -v` failed with 7 expected failures: both slash-separated front-matter payloads for title, summary, and description, plus the body payload.
- GREEN: the same focused command passed: 2 tests, `OK`.

## Verification

- `python3 -m unittest scripts.test_article_pipeline -v`: 88 tests passed, `OK`.
- `git diff --check`: passed.

## Self-review

Both field validators consume the same regex, so the one-line detector change
covers front matter and Markdown without a duplicate validation path. Code
fences remain excluded by `_markdown_prose`; normal raw tag openers, including
incomplete ones, fail closed as required.

## Concerns

None. The intentionally fail-closed detector can reject prose that begins
with a less-than sign followed by an ASCII word; that is the authorized
contract for generated content.
