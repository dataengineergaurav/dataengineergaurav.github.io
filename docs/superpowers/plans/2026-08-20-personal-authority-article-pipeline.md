# Personal Authority Article Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the proven research-led article pipeline to `dataengineergaurav.github.io`, generate approval-gated Jekyll posts weekly, and retire the Metteyya article timer after the replacement is verified.

**Architecture:** Adapt the existing standard-library Metteyya coordinator in place rather than introducing a shared framework. The personal-site repository owns generation state, Jekyll rendering, Telegram approval, guarded Git publication, Hermes routing, and one weekly systemd timer.

**Tech Stack:** Python 3.12 standard library, `unittest`, Jekyll/GitHub Pages, Bash, systemd, Hermes Telegram hooks, Git

**Spec:** `docs/superpowers/specs/2026-08-20-personal-authority-article-pipeline-design.md`

## Global Constraints

- `dataengineergaurav.github.io` is the sole destination; do not cross-post to Metteyya.
- Run once per week and preserve due-state and pending-review idempotency.
- Keep Telegram approval mandatory before commit or push.
- Use recent primary research as evidence, but score topics against reliable data platforms, analytics and BI, governed AI, and engineering leadership.
- Do not invent clients, results, quotations, or firsthand experience.
- Generate Jekyll posts under `_posts/YYYY-MM-DD-slug.md` using the existing post layout.
- Keep the implementation dependency-free beyond tools already installed on the machine.
- Do not publish a live article during implementation verification.
- Disable the Metteyya timer only after the personal pipeline passes its local and operational checks.

---

### Task 1: Port the coordinator and adapt generation for the personal site

**Files:**
- Create: `scripts/article_pipeline.py`
- Create: `scripts/test_article_pipeline.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: the proven coordinator and tests at `/root/blog-metteyyaanalytics/scripts/article_pipeline.py` and `/root/blog-metteyyaanalytics/scripts/test_article_pipeline.py`
- Produces: `is_due(state: dict, now: datetime) -> bool`, `authority_context() -> str`, `render_markdown(article: dict, selection: dict, date: datetime) -> str`, `article_destination(title: str, date: datetime, directory: Path = REPO_ROOT / "_posts") -> Path`, and the existing coordinator CLI

- [ ] **Step 1: Copy the proven coordinator and regression suite into this repository**

Run:

```bash
mkdir -p scripts
cp /root/blog-metteyyaanalytics/scripts/article_pipeline.py scripts/article_pipeline.py
cp /root/blog-metteyyaanalytics/scripts/test_article_pipeline.py scripts/test_article_pipeline.py
```

Expected: both files exist under `scripts/`; no Metteyya source file is modified.

- [ ] **Step 2: Replace the first core tests with personal-site expectations**

In `scripts/test_article_pipeline.py`, keep the imported module and existing safety regressions, then change/add focused cases equivalent to:

```python
def test_due_only_after_one_week_without_pending_draft(self):
    now = datetime(2026, 8, 20, 3, 30, tzinfo=timezone.utc)
    state = pipeline.default_state()
    self.assertTrue(pipeline.is_due(state, now))
    state["last_draft_at"] = (now - timedelta(hours=167)).isoformat()
    self.assertFalse(pipeline.is_due(state, now))
    state["last_draft_at"] = (now - timedelta(hours=168)).isoformat()
    self.assertTrue(pipeline.is_due(state, now))
    state["pending"] = {"id": "draft-1"}
    self.assertFalse(pipeline.is_due(state, now))

def test_authority_context_names_all_personal_themes(self):
    context = pipeline.authority_context()
    for phrase in ("reliable data platforms", "analytics and business intelligence",
                   "governed AI", "data engineering leadership"):
        self.assertIn(phrase, context)
    self.assertNotIn("Metteyya", context)

def test_render_markdown_uses_existing_jekyll_frontmatter(self):
    rendered = pipeline.render_markdown(
        self.valid_article(), self.selection,
        datetime(2026, 8, 20, tzinfo=timezone.utc),
    )
    self.assertTrue(rendered.startswith("---\nlayout: post\n"))
    self.assertIn("date: 2026-08-20\n", rendered)
    self.assertIn('summary: "A practical summary."\n', rendered)
    self.assertNotIn("serviceId:", rendered)
    self.assertNotIn("Metteyya", rendered)

def test_article_destination_uses_dated_jekyll_filename(self):
    with tempfile.TemporaryDirectory() as directory:
        destination = pipeline.article_destination(
            "Useful Research", datetime(2026, 8, 20, tzinfo=timezone.utc),
            Path(directory),
        )
        self.assertEqual(destination.name, "2026-08-20-useful-research.md")
```

Update `valid_article()` so its schema includes `summary`, and remove assertions that require Astro-only `tags`, `author`, `serviceId`, `funnelStage`, `targetKeyword`, or embedded CTA fields.

- [ ] **Step 3: Run the focused tests and confirm they fail for the old behavior**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline.PipelineCoreTests -v
```

Expected: failures mention the 96-hour interval, missing `authority_context`, Astro front matter, or the undated destination.

- [ ] **Step 4: Adapt the minimum coordinator surface**

Make these exact changes in `scripts/article_pipeline.py`:

```python
ARXIV_CATEGORIES = ("cs.LG", "cs.AI", "cs.DB")
AUTHORITY_CONTEXT = """Gaurav Gurjar is a fractional data engineering lead writing for technical and business leaders. Prioritize practical decisions involving reliable data platforms and pipelines, analytics and business intelligence, governed AI systems, and data engineering leadership and delivery. Reject topics that cannot produce specific, evidence-backed guidance."""

def is_due(state, now):
    if state.get("pending"):
        return False
    last = state.get("last_draft_at")
    return not last or now >= datetime.fromisoformat(last) + timedelta(hours=168)

def authority_context():
    return AUTHORITY_CONTEXT
```

Replace `_blog_titles()` with a scan of `REPO_ROOT / "_posts"`. Replace both reads of `src/data/services.ts` and `src/data/content-calendar.ts` with `authority_context()`. Rewrite the selection prompt to score direct fit with the four authority themes rather than a Metteyya service, while retaining the existing minimum total, practical-value, novelty, and evidence thresholds.

Change `ARTICLE_SCHEMA` to require `title`, `summary`, `description`, `body`, `linkedin_post`, and `newsletter_intro`. Keep 1,200–1,800 words, safe-Markdown validation, the selected primary-source URL, and `## References` validation.

Use this rendering and destination contract:

```python
def render_markdown(article, selection, date):
    frontmatter = [
        "---", "layout: post", f"title: {json.dumps(article['title'])}",
        f"date: {date.date().isoformat()}",
        f"summary: {json.dumps(article['summary'])}",
        f"description: {json.dumps(article['description'])}", "---",
    ]
    return "\n".join(frontmatter) + "\n\n" + article["body"].strip() + "\n"

def article_destination(title, date, directory=REPO_ROOT / "_posts"):
    destination = directory / f"{date.date().isoformat()}-{slugify(title)}.md"
    if destination.exists():
        raise FileExistsError(f"destination exists: {destination}")
    return destination
```

Update pending paths, staging paths, and path validation from `src/content/blog` to `_posts`. Change `_build_site()` to execute `[str(REPO_ROOT / "script/cibuild")]`. Use the personal-site URL in distribution messages and derive the default Jekyll URL as `/{year}/{month}/{day}/{slug}.html` from the dated filename.

- [ ] **Step 5: Ignore only runtime state**

Append to `.gitignore`:

```gitignore
.article-generator/
```

- [ ] **Step 6: Run the coordinator suite**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline -v
```

Expected: all coordinator tests pass; skipped canonical-installer tests are acceptable until Task 3 adapts the installer.

- [ ] **Step 7: Commit the personal generation core**

```bash
git add .gitignore scripts/article_pipeline.py scripts/test_article_pipeline.py
git commit -m "feat: adapt article generation for personal site"
```

---

### Task 2: Adapt Telegram approval routing to the personal coordinator

**Files:**
- Create: `automation/hermes-article-approval/__init__.py`
- Create: `automation/hermes-article-approval/plugin.yaml`
- Create: `automation/hermes-article-approval/SKILL.md`
- Modify: `scripts/test_article_pipeline.py`

**Interfaces:**
- Consumes: `scripts/article_pipeline.py decision-hex <lowercase-hex-utf8>`
- Produces: Hermes plugin `personal_article_approval` and `_coordinator_argv(raw_message: str) -> tuple[str, ...]`

- [ ] **Step 1: Copy the deterministic hook and write the path/name regression**

Run:

```bash
mkdir -p automation/hermes-article-approval
cp /root/blog-metteyyaanalytics/automation/hermes-article-approval/__init__.py automation/hermes-article-approval/__init__.py
cp /root/blog-metteyyaanalytics/automation/hermes-article-approval/plugin.yaml automation/hermes-article-approval/plugin.yaml
cp /root/blog-metteyyaanalytics/automation/hermes-article-approval/SKILL.md automation/hermes-article-approval/SKILL.md
```

Add a test that imports the hook by file path and asserts:

```python
self.assertEqual(
    hook._coordinator_argv("APPROVE AbC_123"),
    ("/usr/bin/python3",
     "/root/dataengineergaurav.github.io/scripts/article_pipeline.py",
     "decision-hex", "415050524f5645204162435f313233"),
)
```

- [ ] **Step 2: Run the hook regression and confirm it fails**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline -v
```

Expected: the hook still points to `/root/blog-metteyyaanalytics`.

- [ ] **Step 3: Rebrand only the hook ownership and canonical path**

Keep the exact-command regex, authorized-user check, raw/normalized text equality, hexadecimal message transport, subprocess timeout, and skip behavior unchanged. Set the coordinator path and working directory to:

```python
"/root/dataengineergaurav.github.io/scripts/article_pipeline.py"
cwd="/root/dataengineergaurav.github.io"
```

Set `plugin.yaml` to:

```yaml
name: personal_article_approval
version: 1.0.0
description: Deterministic Telegram approval dispatch for personal-site article drafts
kind: standalone
provides_hooks:
  - pre_gateway_dispatch
```

Update `SKILL.md` and the module docstring to describe the personal-site plugin without changing its protocol.

- [ ] **Step 4: Run the complete test suite**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the personal approval integration**

```bash
git add automation/hermes-article-approval scripts/test_article_pipeline.py
git commit -m "feat: route article approvals to personal site"
```

---

### Task 3: Install one weekly personal-site timer idempotently

**Files:**
- Create: `scripts/setup_article_pipeline.sh`
- Create: `scripts/personal-article-generator.service`
- Create: `scripts/personal-article-generator.timer`
- Modify: `scripts/test_article_pipeline.py`

**Interfaces:**
- Consumes: canonical checkout `/root/dataengineergaurav.github.io`, plugin `personal_article_approval`, coordinator `scripts/article_pipeline.py`
- Produces: `scripts/setup_article_pipeline.sh check|install|remove`, systemd unit `personal-article-generator.service`, and weekly timer `personal-article-generator.timer`

- [ ] **Step 1: Copy the proven installer and units, then change installer test expectations**

Run:

```bash
cp /root/blog-metteyyaanalytics/scripts/setup_article_pipeline.sh scripts/setup_article_pipeline.sh
cp /root/blog-metteyyaanalytics/scripts/metteyya-article-generator.service scripts/personal-article-generator.service
cp /root/blog-metteyyaanalytics/scripts/metteyya-article-generator.timer scripts/personal-article-generator.timer
chmod +x scripts/setup_article_pipeline.sh
```

In the existing fake-environment installer tests, expect:

```python
plugin = config.parent / "plugins/personal_article_approval"
self.assertEqual(plugin.resolve(), script.parents[1] / "automation/hermes-article-approval")
self.assertIn("enable --now personal-article-generator.timer", systemctl_log.read_text())
self.assertIn("disable --now personal-article-generator.timer", systemctl_log.read_text())
```

Also assert that `install` never adds a cron entry and preserves unrelated crontab content byte-for-byte.

- [ ] **Step 2: Run installer tests and confirm old names fail**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline.SetupScriptTests -v
```

Expected: failures reference the old canonical checkout, plugin name, or Metteyya timer.

- [ ] **Step 3: Adapt the installer without adding another scheduling mechanism**

Change the canonical checkout to `/root/dataengineergaurav.github.io`, the plugin destination to `plugins/personal_article_approval`, and all unit names to `personal-article-generator`. Remove legacy Metteyya cron-marker cleanup from the personal installer; retain `crontab -l` only if the existing regression needs to prove unrelated entries remain untouched. `install` must link and enable only the personal systemd timer, enable the personal Hermes plugin, restart Hermes, and run the coordinator doctor. `remove` must disable only personal units and remove only the matching personal plugin symlink.

Write the service exactly as:

```ini
[Unit]
Description=Generate a personal authority article draft

[Service]
Type=oneshot
WorkingDirectory=/root/dataengineergaurav.github.io
Environment=ARTICLE_MODEL=gpt-5.6-sol
ExecStart=/usr/bin/python3 /root/dataengineergaurav.github.io/scripts/article_pipeline.py generate
StandardOutput=append:/root/dataengineergaurav.github.io/.article-generator/article_generator.log
StandardError=append:/root/dataengineergaurav.github.io/.article-generator/article_generator.log
```

Write the weekly timer exactly as:

```ini
[Unit]
Description=Generate a personal authority article draft weekly

[Timer]
OnCalendar=Mon *-*-* 03:30:00 UTC
Persistent=true
AccuracySec=1m
Unit=personal-article-generator.service

[Install]
WantedBy=timers.target
```

- [ ] **Step 4: Verify installer behavior and unit syntax**

Run:

```bash
bash -n scripts/setup_article_pipeline.sh
systemd-analyze verify scripts/personal-article-generator.service scripts/personal-article-generator.timer
python3 -m unittest scripts.test_article_pipeline.SetupScriptTests -v
```

Expected: shell syntax and unit verification succeed; all installer tests pass without touching the real crontab or systemd state.

- [ ] **Step 5: Commit scheduling and installation**

```bash
git add scripts/setup_article_pipeline.sh scripts/personal-article-generator.service scripts/personal-article-generator.timer scripts/test_article_pipeline.py
git commit -m "feat: schedule weekly personal article drafts"
```

---

### Task 4: Verify the pipeline and retire the Metteyya scheduler safely

**Files:**
- Modify only if verification exposes a defect: files created in Tasks 1–3

**Interfaces:**
- Consumes: `scripts/setup_article_pipeline.sh`, coordinator doctor, Jekyll build, both systemd timer names
- Produces: one enabled `personal-article-generator.timer`, no enabled `metteyya-article-generator.timer`, and no live article publication

- [ ] **Step 1: Run all repository-local checks from a clean worktree**

Run:

```bash
python3 -m unittest scripts.test_article_pipeline -v
bash -n scripts/setup_article_pipeline.sh
systemd-analyze verify scripts/personal-article-generator.service scripts/personal-article-generator.timer
script/cibuild
git diff --check
git status --short
```

Expected: every test and build passes, `git diff --check` prints nothing, and `git status --short` prints nothing.

- [ ] **Step 2: Confirm the committed branch is synchronized before installation**

Run:

```bash
git fetch origin master
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)"
scripts/setup_article_pipeline.sh check
python3 scripts/article_pipeline.py doctor
```

Expected: local `HEAD` equals `origin/master`; all required executables, Git identity, Codex isolation, Telegram credentials, and upstream checks pass. If the branch is ahead, push the implementation commits before continuing.

- [ ] **Step 3: Install and verify the personal timer before touching Metteyya**

Run:

```bash
scripts/setup_article_pipeline.sh install
systemctl is-enabled personal-article-generator.timer
systemctl is-active personal-article-generator.timer
systemctl list-timers --all personal-article-generator.timer --no-pager
```

Expected: the personal timer is enabled and active, with its next Monday 03:30 UTC activation shown. Do not manually start the service; installation verification must not generate an article.

- [ ] **Step 4: Disable and unlink only the old Metteyya integration**

Run:

```bash
/root/blog-metteyyaanalytics/scripts/setup_article_pipeline.sh remove
systemctl is-enabled metteyya-article-generator.timer
systemctl is-active metteyya-article-generator.timer
```

Expected: both final checks report disabled/inactive with nonzero status; existing Metteyya posts, state, logs, and rejected drafts remain on disk.

- [ ] **Step 5: Confirm there is exactly one owned article timer and cron is unchanged**

Run:

```bash
systemctl list-unit-files '*article-generator.timer' --no-pager
systemctl list-timers --all '*article-generator.timer' --no-pager
crontab -l
```

Expected: `personal-article-generator.timer` is the only enabled article timer, Metteyya is disabled or absent, and the existing Hermes wiki cron entry remains unchanged.

- [ ] **Step 6: Record any verification-only repair**

If a defect required a code change, rerun Step 1 and commit only that repair:

```bash
git add scripts automation .gitignore
git commit -m "fix: complete personal article pipeline migration"
```

Expected: no commit is created when verification required no repair.
