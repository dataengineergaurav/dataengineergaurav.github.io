# Weekly CV Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `CV-Development` the single source of truth for the CV and derive the public CV from it weekly, reusing the existing `automation/weekly-progress/` pipeline, without ever leaking a client name.

**Architecture:** The portfolio repo's Monday run gains a CV stage that reuses the deterministic GitHub activity collector and analyzer, then two new skills propose `highlights`-only bullet edits. Deterministic scripts enforce the guard rails (`cv_guard.py`), scan rendered PDFs (`cv_policy.py`), render and copy the one-pager into the site (`cv_sync.py`), and open a PR against `CV-Development` (`cv_publish.py`). Each stage produces its work before any publisher runs, so the site PR carries both the post and the refreshed PDF.

**Tech Stack:** Python 3 (stdlib `unittest`), PyYAML, Jinja2 + weasyprint, pypdf, `uv` (CV-Development), Bash, systemd.

**Spec:** `docs/superpowers/specs/2026-10-09-cv-weekly-refresh-design.md`

## Global Constraints

- **Edit boundary:** the agent may change only `highlights` lists in `data/experience.yaml`. Dates, roles, `organization_id`, `client_id`, `summary`, `technologies` and `meta` are immutable to automation.
- **Highlight cap:** `MAX_HIGHLIGHTS_PER_ENGAGEMENT = 5` (in `cv_guard.py`, importable by tests and the writer prompt).
- **Denylists (verbatim):** `FORBIDDEN_NAMES = ("sagesure", "ishir", "cannaspyglass", "petfolk", "tradetips", "casepoint", "nhs", "archetypal ai", "6overn.ai")`; `RETIRED_CLAIMS = ("$3b+",)`; `CV_ALLOWED_NAMES = ("ishir", "cannaspyglass", "casepoint", "ai squared")`.
- **No em-dashes** may appear in any rendered CV output.
- **Publishers never target the base branch.** Site base is `master`, CV base is `main`. PRs are the only approval path.
- **The agent never runs git.** Only deterministic scripts run `git add/commit/push` or the GitHub API.
- **Two-repo paths:** portfolio `/root/dataengineergaurav.github.io`, CV `/root/CV-Development`.
- Every commit ends with the trailer `Co-authored-by: CommandCodeBot <noreply@commandcode.ai>`.
- `python3 -m unittest` and `uv run pytest` must pass before any PR step.

## Review Focus

Failure modes the spec implies but that no single task's happy-path test exercises. Each is pinned by a test in the owning task.

1. A PDF whose text extraction returns empty (image-only or extraction failure) must **fail closed**, not silently pass the policy gate. (Task 3)
2. `experience.yaml` edited so a highlight moves between entries, or a highlight entry is added or removed, is highlights-only by construction and must be allowed without the guard crashing or misreading a reorder as a change. (Task 4)
3. `cv_sync` failing after the PDF is copied but before `version.json` is written must not leave a half-updated site worktree. (Task 7)
4. Two runs on the same day must be idempotent for both PRs, and a re-run after a guard failure must not leave a stray branch. (Tasks 6, 9)
5. A writer output with `replaces` out of range, or a bullet that duplicates an existing one, must be rejected rather than rendered. (Task 8)

---

### Task 1: Public-name projection in CV-Development

**Files:**
- Modify: `/root/CV-Development/render.py:108-118` (`render_html`)
- Modify: `/root/CV-Development/data/experience.yaml` (organizations `sagesure`, `petfolk`, `covid_public`)
- Test: `/root/CV-Development/tests/test_render.py`

**Interfaces:**
- Produces: `render_html` builds `orgs` as `{slug: {**org, "name": public_name or org["name"], "about": public_about or org.get("about", "")}}`. Templates are unchanged; `public_name` / `public_about` are optional keys on any `organizations[*]` entry.

- [ ] **Step 1: Write the failing tests**

```python
def test_public_name_replaces_client_name_in_both_renders():
    data = load_data()
    data["organizations"]["sagesure"]["public_name"] = "US residential property insurer"
    html = render_html(data, "resume.html")
    assert "SageSure" not in html
    assert "US residential property insurer" in html

def test_employer_without_public_name_keeps_its_name():
    data = load_data()
    assert "ISHIR" in render_html(data, "resume.html")

def test_public_name_defaults_to_name_and_about_to_none():
    data = load_data()
    org = {**data["organizations"]["sagesure"]}
    org.pop("public_name", None)
    data["organizations"]["sagesure"] = org
    assert "SageSure" in render_html(data, "resume.html")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /root/CV-Development && uv run pytest tests/test_render.py -k public_name -v`
Expected: FAIL (`'SageSure' not in html` fails; projection absent).

- [ ] **Step 3: Implement the projection in `render_html`**

Replace the `orgs` comprehension so each entry is projected. One line on approach: build the projected dict before `env.globals["orgs"] = orgs`, so the `concurrent` name lookup also uses public names.

- [ ] **Step 4: Reconcile the data**

Add `public_name` (and `public_about` where the current `about` leaks identifiers like `$3.2B premium`) to the client organizations `sagesure` and `petfolk`. Leave `covid_public` as-is unless its `about` names a restricted term. Delete nothing yet; `6overn.ai` is absent from this file.

- [ ] **Step 5: Run the full CV suite**

Run: `cd /root/CV-Development && uv run pytest -q`
Expected: PASS (including the existing no-em-dash and claim-relocation tests).

- [ ] **Step 6: Commit**

```bash
cd /root/CV-Development && git add render.py data/experience.yaml tests/test_render.py
git commit -F - <<'EOF'
feat: project public names into CV renders

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 2: Close the CI PDF hole (ship this phase on its own)

**Files:**
- Create: `/root/dataengineergaurav.github.io/scripts/public_policy.py`
- Modify: `/root/dataengineergaurav.github.io/scripts/test_public_content.py:11-14,64-83`
- Modify: `/root/dataengineergaurav.github.io/.github/workflows/ci.yaml`
- Modify: `/root/dataengineergaurav.github.io/Gaurav_Gurjar_CV_AI-Data-Engineer.pdf` (regenerated)
- Test: `/root/dataengineergaurav.github.io/scripts/test_public_content.py` (`PublicContentTests`)

**Interfaces:**
- Produces: `scripts/public_policy.py` exports `FORBIDDEN_NAMES`, `RETIRED_CLAIMS`, `TESTIMONIAL_NAMES`, `CV_ALLOWED_NAMES`, and `cv_forbidden_names() -> tuple[str, ...]` (= `FORBIDDEN_NAMES` minus `CV_ALLOWED_NAMES`). Later tasks import this module; it is stdlib-only.
- Produces: `test_public_content.text_reader(path: Path) -> str` returns PDF text for `.pdf` (via `pypdf`) and file text otherwise.

- [ ] **Step 1: Write the failing tests**

Add to `PublicContentTests`:

```python
def test_pdf_files_are_scanned_with_the_client_scoped_list(self):
    with TemporaryDirectory() as t:
        root = Path(t); (root / "index.md").write_text("home", encoding="utf-8")
        (root / "cv.pdf").write_bytes(b"")
        findings = find_forbidden_names(root, text_reader=lambda p: "SageSure and ISHIR")
        self.assertEqual(findings, [f"{root / 'cv.pdf'}: sagesure"])

def test_empty_pdf_extraction_fails_closed(self):
    with TemporaryDirectory() as t:
        root = Path(t); (root / "index.md").write_text("home", encoding="utf-8")
        (root / "cv.pdf").write_bytes(b"")
        findings = find_forbidden_names(root, text_reader=lambda p: "")
        self.assertEqual(findings, [f"{root / 'cv.pdf'}: unreadable pdf"])
```

- [ ] **Step 2: Run to verify failure**

Run: `cd /root/dataengineergaurav.github.io && python3 -m unittest scripts.test_public_content -v`
Expected: FAIL (`find_forbidden_names` takes no `text_reader`; `.pdf` not discovered).

- [ ] **Step 3: Create `scripts/public_policy.py`**

Move `FORBIDDEN_NAMES`, `RETIRED_CLAIMS`, `TESTIMONIAL_NAMES` verbatim from `test_public_content.py`, add `CV_ALLOWED_NAMES` and `cv_forbidden_names()`, and import them back into `test_public_content.py`.

- [ ] **Step 4: Add PDF discovery and scanning**

In `public_text_files`, include `".pdf"` in `suffixes` for both source and generated modes. In `find_forbidden_names`, accept `text_reader=text_reader`, read via it, and when a `.pdf` yields empty text return `f"{path}: unreadable pdf"`. For `.pdf` paths use `cv_forbidden_names()`; otherwise the full list. Implement `text_reader` with `pypdf.PdfReader(...).pages` and join `page.extract_text()`.

- [ ] **Step 5: Install `pypdf` in CI**

Add a step before `script/cibuild` in `.github/workflows/ci.yaml`: `run: pip install pypdf`. Confirm `script/cibuild`'s `python3 scripts/test_public_content.py --root _site` still runs after it.

- [ ] **Step 6: Regenerate the leaked site PDF from the reconciled source**

Run, in the portfolio repo:
`cp /root/CV-Development/Gaurav_Gurjar_CV.pdf Gaurav_Gurjar_CV_AI-Data-Engineer.pdf` after `cd /root/CV-Development && uv run python render.py`.
Then run `python3 scripts/test_public_content.py --root .` and confirm zero findings (Task 1 removed the client names).

- [ ] **Step 7: Run the suite and commit**

Run: `python3 -m unittest scripts.test_public_content -q` then `python3 scripts/test_public_content.py --root _site`
Expected: PASS / no findings.

```bash
git add scripts/public_policy.py scripts/test_public_content.py .github/workflows/ci.yaml Gaurav_Gurjar_CV_AI-Data-Engineer.pdf
git commit -F - <<'EOF'
fix: scan PDFs in the public content policy and publish the anonymized CV

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

> Phase 1 ends here. Tasks 1-2 alone remove the live client-name leak. Tasks 3-9 build the automation.

---

### Task 3: `cv_policy.py` PDF policy gate

**Files:**
- Create: `/root/dataengineergaurav.github.io/automation/weekly-progress/cv_policy.py`
- Test: `/root/dataengineergaurav.github.io/scripts/test_cv_refresh.py` (new file, `CvPolicyTests`)

**Interfaces:**
- Consumes: `public_policy.cv_forbidden_names()`, `public_policy.RETIRED_CLAIMS`.
- Produces: `text_violations(text: str) -> list[str]`; `pdf_text_violations(text: str) -> list[str]` (adds `"unreadable pdf"` when `text` is empty); `pdf_violations(path: Path) -> list[str]` (extracts then delegates); `main()` CLI `cv_policy.py --pdf PATH [--pdf PATH ...]` exit 1 on any violation.

- [ ] **Step 1: Write the failing tests**

```python
class CvPolicyTests(unittest.TestCase):
    def test_flags_a_client_name(self):
        self.assertEqual(cv_policy.text_violations("Work at SageSure"), ["sagesure"])

    def test_allows_an_employer_name(self):
        self.assertEqual(cv_policy.text_violations("Senior Data Engineer, ISHIR"), [])

    def test_empty_extraction_fails_closed(self):
        self.assertEqual(cv_policy.pdf_text_violations(""), ["unreadable pdf"])

    def test_flags_a_retired_claim(self):
        self.assertEqual(cv_policy.text_violations("$3B+ delivered"), ["$3b+"])
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_cv_refresh.CvPolicyTests -v`
Expected: FAIL (module missing).

- [ ] **Step 3: Implement `cv_policy.py`**

`text_violations` casefolds and returns the matched terms from `cv_forbidden_names() + RETIRED_CLAIMS`. `pdf_violations(path)` uses `pypdf` and delegates to `text_violations`, returning `["unreadable pdf"]` when extraction is empty. CLI prints findings and exits 1 when non-empty. Load `public_policy` via `sys.path` insertion of the portfolio root (this script runs from `automation/weekly-progress/`).

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m unittest scripts.test_cv_refresh.CvPolicyTests -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/weekly-progress/cv_policy.py scripts/test_cv_refresh.py
git commit -F - <<'EOF'
feat: add the CV pdf policy gate

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 4: `cv_guard.py` highlights-only guard

**Files:**
- Create: `/root/dataengineergaurav.github.io/automation/weekly-progress/cv_guard.py`
- Test: `/root/dataengineergaurav.github.io/scripts/test_cv_refresh.py` (`CvGuardTests`)

**Interfaces:**
- Produces: `MAX_HIGHLIGHTS_PER_ENGAGEMENT = 5`; `structural_violations(old: dict, new: dict) -> list[str]`; `cap_violations(new: dict, cap: int = MAX_HIGHLIGHTS_PER_ENGAGEMENT) -> list[str]`; `violations(old: dict, new: dict) -> list[str]`.
- CLI: `cv_guard.py --data PATH [--base-ref HEAD]` compares `git show <base-ref>:PATH` with the working tree; exit 1 on violations.

- [ ] **Step 1: Write the failing tests**

```python
class CvGuardTests(unittest.TestCase):
    def test_highlights_change_is_allowed(self):
        old = {"engagements": [{"id": "e1", "highlights": ["a"]}]}
        new = {"engagements": [{"id": "e1", "highlights": ["a", "b"]}]}
        self.assertEqual(cv_guard.violations(old, new), [])

    def test_date_change_is_rejected(self):
        old = {"engagements": [{"id": "e1", "start": "2024-04", "highlights": []}]}
        new = {"engagements": [{"id": "e1", "start": "2023-01", "highlights": []}]}
        self.assertEqual(cv_guard.violations(old, new), ["engagements[e1].start changed"])

    def test_cap_rejects_sixth_highlight(self):
        new = {"engagements": [{"id": "e1", "highlights": ["a", "b", "c", "d", "e", "f"]}]}
        self.assertEqual(cv_guard.cap_violations(new), ["engagements[e1]: 6 highlights (cap 5)"])

    def test_moving_a_highlight_between_engagements_is_allowed(self):
        old = {"engagements": [{"id": "a", "highlights": ["x"]}, {"id": "b", "highlights": []}]}
        new = {"engagements": [{"id": "a", "highlights": []}, {"id": "b", "highlights": ["x"]}]}
        self.assertEqual(cv_guard.violations(old, new), [])
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_cv_refresh.CvGuardTests -v`
Expected: FAIL (module missing).

- [ ] **Step 3: Implement `cv_guard.py`**

Walk both trees recursively; at any key named `highlights`, compare as lists and allow differences, including a changed element count. Any other differing leaf yields `"<path> changed"`. Key by list-item `id` where present so reordering does not read as a change. `cap_violations` reports any `highlights` list longer than `cap` for both `engagements` and `projects`.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m unittest scripts.test_cv_refresh.CvGuardTests -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/weekly-progress/cv_guard.py scripts/test_cv_refresh.py
git commit -F - <<'EOF'
feat: add the highlights-only CV data guard

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 5: Widen the publisher guard to a path set

**Files:**
- Modify: `/root/dataengineergaurav.github.io/automation/weekly-progress/publish.py:76-84,110-125`
- Test: `/root/dataengineergaurav.github.io/scripts/test_weekly_progress.py` (`PublishGuardTests`)

**Interfaces:**
- Produces: `only_change_guard(relatives: list[str], repo_root=REPO_ROOT)` compares the **set** of changed paths from `git status --porcelain` to the expected set. `publish()` computes `expected = [post] + ([CV_PDF, CV_VERSION] if version.json exists in the worktree)`, where the constants are `Gaurav_Gurjar_CV_AI-Data-Engineer.pdf` and `Gaurav_Gurjar_CV_AI-Data-Engineer.version.json`.

- [ ] **Step 1: Update the failing tests**

Rewrite `PublishGuardTests` to pass lists and add one case: `{post, pdf, version.json}` present → accepted; an unexpected fourth path → rejected.

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_weekly_progress.PublishGuardTests -v`
Expected: FAIL (signature still expects a string).

- [ ] **Step 3: Implement the set comparison**

Parse each `git status --porcelain --untracked-files=all` line to its path (strip the 3-character status column), compare `set(paths) == set(relatives)`. Update `publish()` to build `expected` as above and pass the list.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m unittest scripts.test_weekly_progress -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/weekly-progress/publish.py scripts/test_weekly_progress.py
git commit -F - <<'EOF'
refactor: let the publish guard accept the post plus the synced CV

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 6: `cv_publish.py` — open the CV-Development PR

**Files:**
- Create: `/root/dataengineergaurav.github.io/automation/weekly-progress/cv_publish.py`
- Test: `/root/dataengineergaurav.github.io/scripts/test_cv_refresh.py` (`CvPublishTests`)

**Interfaces:**
- Consumes: `publish.git`, `publish.parse_remote`, `publish.existing_pr`, `publish._api`, `publish.sha256_bytes`, `publish._load_env_value`.
- Produces: `publish(date, base="main", remote="origin", repo_root=CV_ROOT, body_file=None, push=True) -> int`; `branch_for(date: str) -> str` returning `f"cv-refresh/{date}"`; `assert_only(expected: list[str], actual: list[str]) -> None` (raises `SystemExit` on any difference); constants `CV_ROOT = Path("/root/CV-Development")` and `CV_FILES = ["data/experience.yaml", "resume.html", "resume_expanded.html", "Gaurav_Gurjar_CV.pdf", "Gaurav_Gurjar_CV_extended.pdf"]`; CLI `cv_publish.py --date YYYY-MM-DD [--body-file P] [--repo-root P] [--no-push|--dry-run]`.

- [ ] **Step 1: Write the failing tests**

```python
class CvPublishTests(unittest.TestCase):
    def test_allow_list_rejects_an_unexpected_path(self):
        with self.assertRaises(SystemExit):
            cv_publish.assert_only(CV_FILES, CV_FILES + ["notes.txt"])

    def test_allow_list_accepts_the_expected_set(self):
        cv_publish.assert_only(CV_FILES, CV_FILES)  # no raise

    def test_branch_name_is_idempotent(self):
        self.assertEqual(cv_publish.branch_for("2026-10-12"), "cv-refresh/2026-10-12")
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_cv_refresh.CvPublishTests -v`
Expected: FAIL (module missing).

- [ ] **Step 3: Implement `cv_publish.py`**

Mirror `publish.py`: fetch base, require clean synchronized `main`, assert the changed-path set equals `CV_FILES`, look up an existing PR on `cv-refresh/<date>` and exit 0 if found, else `git checkout -B`, add exactly `CV_FILES`, verify each staged blob hash against the reviewed bytes, commit `cv: weekly highlights <date>`, push, open `{"title": f"CV highlights — {date}", "head", "base", "body"}`, then return to `main`. Reuse `publish.py`'s helpers by importing it as a module (same directory).

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m unittest scripts.test_cv_refresh.CvPublishTests -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add automation/weekly-progress/cv_publish.py scripts/test_cv_refresh.py
git commit -F - <<'EOF'
feat: open the weekly CV pull request deterministically

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 7: `cv_sync.py` — render and publish the one-pager

**Files:**
- Create: `/root/dataengineergaurav.github.io/automation/weekly-progress/cv_sync.py`
- Create: `/root/dataengineergaurav.github.io/scripts/check_cv_marker.py`
- Modify: `/root/dataengineergaurav.github.io/script/cibuild`
- Test: `/root/dataengineergaurav.github.io/scripts/test_cv_refresh.py` (`CvSyncTests`)

**Interfaces:**
- Produces: `SITE_PDF = "Gaurav_Gurjar_CV_AI-Data-Engineer.pdf"`, `SITE_VERSION = "Gaurav_Gurjar_CV_AI-Data-Engineer.version.json"`; `sha256_file(path: Path) -> str`; `render(cv_root: Path) -> None` (runs `uv run python render.py` and `uv run python render.py --expanded` with `cwd=cv_root`); `sync(cv_root: Path, site_root: Path) -> dict` copies `Gaurav_Gurjar_CV.pdf` to `site_root/SITE_PDF` and writes `SITE_VERSION` = `{"cv_commit", "rendered_at", "sha256"}`; `marker_violations(site_root: Path) -> list[str]`; CLI `cv_sync.py [--cv-root P] [--site-root P] [--dry-run]`.

- [ ] **Step 1: Write the failing tests**

```python
class CvSyncTests(unittest.TestCase):
    def test_writes_version_marker_next_to_the_pdf(self):
        with cv_sync_fixture() as (cv_root, site_root):
            marker = cv_sync.sync(cv_root, site_root)
            written = json.loads((site_root / cv_sync.SITE_VERSION).read_text())
            self.assertEqual(written["sha256"], cv_sync.sha256_file(site_root / cv_sync.SITE_PDF))
            self.assertEqual(marker["cv_commit"], "deadbeef")

    def test_site_worktree_is_not_half_updated_on_failure(self):
        with cv_sync_fixture(render_fails=True) as (cv_root, site_root):
            with self.assertRaises(SystemExit):
                cv_sync.sync(cv_root, site_root)
            self.assertFalse((site_root / cv_sync.SITE_PDF).exists())

    def test_version_marker_hash_check_rejects_a_swapped_pdf(self):
        with cv_sync_fixture() as (cv_root, site_root):
            cv_sync.sync(cv_root, site_root)
            (site_root / cv_sync.SITE_PDF).write_bytes(b"tampered")
            self.assertIn("sha256", cv_sync.marker_violations(site_root))
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_cv_refresh.CvSyncTests -v`
Expected: FAIL (module missing).

- [ ] **Step 3: Implement `cv_sync.py`**

Render into a staging directory first, and only move the PDF and write the marker once both render and copy succeed, so a failure leaves the site worktree untouched. `marker_violations(site_root)` returns a non-empty list when the marker is missing, malformed, or its `sha256` differs from the committed PDF.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m unittest scripts.test_cv_refresh.CvSyncTests -v`
Expected: PASS.

- [ ] **Step 5: Wire the marker check into CI**

Create `scripts/check_cv_marker.py` (`--root`, default repo root) that inserts `automation/weekly-progress` on `sys.path`, imports `cv_sync`, prints `cv_sync.marker_violations(root)`, and exits 1 when non-empty. Add `python3 scripts/check_cv_marker.py --root .` to `script/cibuild` after the content check.

- [ ] **Step 6: Verify the CI check both ways**

Run: `python3 scripts/check_cv_marker.py --root .` (expect exit 0), then append a byte to the committed PDF and re-run (expect exit 1 naming `sha256`); restore the PDF.

- [ ] **Step 7: Commit**

```bash
git add automation/weekly-progress/cv_sync.py scripts/check_cv_marker.py scripts/test_cv_refresh.py script/cibuild
git commit -F - <<'EOF'
feat: render and sync the public CV, guarded by a version marker

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 8: The writer and editor skills

**Files:**
- Create: `/root/dataengineergaurav.github.io/.commandcode/skills/cv-highlight-writer/SKILL.md`
- Create: `/root/dataengineergaurav.github.io/.commandcode/skills/cv-editor/SKILL.md`
- Test: `/root/dataengineergaurav.github.io/scripts/test_weekly_progress.py` (`SkillContractTests`)

**Interfaces:**
- Produces: `cv-highlight-writer` writes `.progress-generator/<date>/cv-bullets.json` with `{"bullets": [{"engagement_id"|"project_id", "bullet", "replaces"?, "evidence": [url]}]}`. `cv-editor` returns `{"verdict": "approve|revise|block", "violations": [...], "notes": "...", "revised_bullets": [...]}`.

- [ ] **Step 1: Extend the failing skill-contract test**

Add `cv-highlight-writer` and `cv-editor` to the list `SkillContractTests` iterates, asserting `---` frontmatter with matching `name:` and a `description:`.

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest scripts.test_weekly_progress.SkillContractTests -v`
Expected: FAIL (skills missing).

- [ ] **Step 3: Write `cv-highlight-writer/SKILL.md`**

Frontmatter matching the existing skills. Body: consume `analysis.json` and the current `experience.yaml`; emit `cv-bullets.json`. State the constraints verbatim (highlights only, cap and `replaces` semantics from `MAX_HIGHLIGHTS_PER_ENGAGEMENT = 5`, past tense, no first person, no em-dashes, at most one bullet per engagement per week, no invented metrics, evidence links required). State that STORIFY shapes which development is significant, never the literal bullet text.

- [ ] **Step 4: Write `cv-editor/SKILL.md`**

Frontmatter matching. Body: model on `blog-editor`; reject duplicates of existing role bullets (the CV test's < 50% distinctive-word rule), missing evidence, contradictions with the Build Log, forbidden client names, and `replaces` out of range; return the verdict JSON. State that it never commits.

- [ ] **Step 5: Run to verify pass**

Run: `python3 -m unittest scripts.test_weekly_progress.SkillContractTests -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add .commandcode/skills/cv-highlight-writer .commandcode/skills/cv-editor scripts/test_weekly_progress.py
git commit -F - <<'EOF'
feat: add the CV highlight writer and editor skills

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

### Task 9: Wire the CV stage into the Monday run

**Files:**
- Modify: `/root/dataengineergaurav.github.io/automation/weekly-progress/run.sh`
- Modify: `/root/dataengineergaurav.github.io/README.md` (document the CV stage)
- Test: manual rehearsal (no unit coverage; the rehearsed commands are the verification)

**Interfaces:**
- Consumes: `collect.py`, `cv_guard.py`, `cv_policy.py`, `cv_sync.py`, `cv_publish.py`, `publish.py`, the two new skills, `uv` (via `cv_sync.py`).

- [ ] **Step 1: Move the site publish to the end of `run.sh`**

Relocate the `publish.py` call so it runs after the CV stage, and pass the widened expected set implicitly (Task 5). The blog post must be written before the CV stage; the CV stage reuses `.progress-generator/activity/<date>.json` and only reruns `collect.py` if that file is absent.

- [ ] **Step 2: Add the CV stage**

After the blog post exists, run a second `cmd -p` invoking `cv-highlight-writer` then `cv-editor`, then in order: `cv_guard.py --data /root/CV-Development/data/experience.yaml`; `(cd /root/CV-Development && uv run pytest -q)`; `cv_policy.py` over the rendered PDFs; `cv_sync.py`; `cv_publish.py --date <date> $no_push`. On any non-zero step, skip the CV PR and continue to the site publish with the post alone.

- [ ] **Step 3: Rehearse without pushing**

Run: `automation/weekly-progress/run.sh --no-push`
Expected: post written; CV stage prints its intended branch/PR and the synced PDF path; no branches created; `git -C /root/CV-Development status` clean after the run.

- [ ] **Step 4: Verify idempotency and cleanliness**

Re-run Step 3 and confirm no stray branches (`git -C /root/CV-Development branch --list 'cv-refresh/*'` is empty) and identical output.

- [ ] **Step 5: Document and commit**

Add a "Weekly CV refresh" subsection to `README.md` mirroring the existing pipeline section (entry point, `--no-push`, the two PRs, the guard rails).

```bash
git add automation/weekly-progress/run.sh README.md
git commit -F - <<'EOF'
feat: run the CV highlight stage in the weekly pipeline

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

---

## Execution notes

- Tasks 1-2 are Phase 1 and are independently shippable; they remove the live leak. Decide whether to execute Phase 1 before scheduling the rest.
- Tasks 3-7 are pure-`unittest` and can be built without the agent (the skills are the only LLM surface).
- Task 9 is the only task whose verification is a rehearsal rather than a test; run it with `--no-push` first and inspect `.progress-generator/<date>/`.
