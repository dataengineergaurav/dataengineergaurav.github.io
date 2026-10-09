import importlib.util
import json
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION = REPO_ROOT / "automation" / "weekly-progress"
SKILLS_DIR = REPO_ROOT / ".commandcode" / "skills"
SKILL_NAMES = (
    "github-progress-collector",
    "progress-analyzer",
    "technical-blog-writer",
    "github-project-context",
    "blog-editor",
    "publish-weekly-progress",
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


collect = load_module("weekly_collect", AUTOMATION / "collect.py")
publish = load_module("weekly_publish", AUTOMATION / "publish.py")

SINCE = "2026-10-01T00:00:00Z"
UNTIL = "2026-10-08T00:00:00Z"


def raw_fixture():
    return {
        "user": "dataengineergaurav",
        "since": SINCE,
        "until": UNTIL,
        "repos": [
            {
                "full_name": "me/proj", "private": False,
                "created_at": "2026-09-01T00:00:00Z",
                "pushed_at": "2026-10-07T00:00:00Z",
                "updated_at": "2026-10-07T00:00:00Z",
                "archived": False, "html_url": "https://github.com/me/proj",
            },
            {
                "full_name": "me/old", "private": True,
                "created_at": "2024-01-01T00:00:00Z",
                "pushed_at": "2026-09-01T00:00:00Z",
                "updated_at": "2026-10-06T00:00:00Z",
                "archived": True, "html_url": "https://github.com/me/old",
            },
        ],
        "commits": {
            "me/proj": [
                {"sha": "a1", "commit": {"message": "Add regulatory ingestion\n\nlong body",
                                         "author": {"date": "2026-10-07T10:00:00Z"}}},
                {"sha": "a2", "commit": {"message": "Merge pull request #4 from feature",
                                         "author": {"date": "2026-10-06T10:00:00Z"}}},
                {"sha": "a3", "commit": {"message": "dependabot bump lodash",
                                         "author": {"date": "2026-10-05T10:00:00Z"}}},
            ],
        },
        "commit_details": {
            "a1": {"files": [{"filename": "ingest.py"}, {"filename": "README.md"}]},
            "a3": {"files": [{"filename": "package-lock.json"}]},
        },
        "search_issues": [
            {"repository_url": "https://api.github.com/repos/me/proj", "number": 4,
             "title": "Add ingestion", "state": "closed",
             "html_url": "https://github.com/me/proj/pull/4",
             "created_at": "2026-10-05T00:00:00Z", "updated_at": "2026-10-06T00:00:00Z",
             "pull_request": {"merged_at": "2026-10-06T00:00:00Z"}},
            {"repository_url": "https://api.github.com/repos/me/proj", "number": 5,
             "title": "Duplicates on re-ingest", "state": "open",
             "html_url": "https://github.com/me/proj/issues/5",
             "created_at": "2026-10-06T00:00:00Z", "updated_at": "2026-10-06T00:00:00Z"},
        ],
        "releases": {
            "me/proj": [{"tag_name": "v1.0", "name": "v1.0",
                         "published_at": "2026-10-05T00:00:00Z",
                         "html_url": "https://github.com/me/proj/releases/tag/v1.0"}],
        },
        "events": [
            {"type": "CreateEvent", "repo": {"name": "me/proj"},
             "payload": {"ref_type": "repository"}},
        ],
    }


class ProjectCatalogTests(unittest.TestCase):
    def test_parses_real_catalog(self):
        projects = collect.load_projects(collect.PROJECTS_FILE)
        self.assertIn("setu", projects)
        self.assertIn("Python", projects["setu"]["stack"])
        self.assertIn("site", projects["setu"]["links"])

    def test_parses_inline_list_and_map(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "projects.yaml"
            path.write_text(
                "demo:\n"
                "  purpose: A demo  # trailing comment\n"
                "  stack: [Python, DuckDB]\n"
                "  links: {site: \"https://example.com\", docs: \"\"}\n",
                encoding="utf-8",
            )
            projects = collect.load_projects(path)
            self.assertEqual(projects["demo"]["stack"], ["Python", "DuckDB"])
            self.assertEqual(projects["demo"]["purpose"], "A demo")
            self.assertEqual(projects["demo"]["links"]["site"], "https://example.com")


class BuildPackTests(unittest.TestCase):
    def setUp(self):
        self.pack = collect.build_pack(raw_fixture(), {"me/proj": {"purpose": "x"}}, SINCE, UNTIL)

    def test_merge_commits_are_dropped(self):
        shas = [commit["sha"] for commit in self.pack["commits"]]
        self.assertNotIn("a2", shas)

    def test_churn_detection_and_stats(self):
        by_sha = {commit["sha"]: commit for commit in self.pack["commits"]}
        self.assertFalse(by_sha["a1"]["flags"]["churn"])
        self.assertTrue(by_sha["a3"]["flags"]["churn"])
        self.assertTrue(by_sha["a1"]["flags"]["readme"])
        self.assertEqual(self.pack["stats"]["commits"], 1)
        self.assertEqual(self.pack["stats"]["churn_commits"], 1)
        self.assertEqual(self.pack["stats"]["files_changed"], 3)

    def test_pr_issue_release_and_new_project(self):
        self.assertEqual(len(self.pack["pull_requests"]), 1)
        self.assertTrue(self.pack["pull_requests"][0]["merged"])
        self.assertEqual(len(self.pack["issues"]), 1)
        self.assertEqual(len(self.pack["releases"]), 1)
        self.assertEqual(self.pack["new_projects"], ["me/proj"])
        self.assertEqual(self.pack["archived_projects"], ["me/old"])
        self.assertIn("projects_context", self.pack)

    def test_inactive_repo_excluded(self):
        names = [repo["full_name"] for repo in self.pack["repos"]]
        self.assertIn("me/proj", names)
        self.assertNotIn("me/old", names)

    def test_quiet_week_summary(self):
        empty = collect.build_pack(
            {"repos": [], "commits": {}, "commit_details": {}, "search_issues": [],
             "releases": {}, "events": []}, {}, SINCE, UNTIL,
        )
        self.assertIn("no non-churn activity", collect.summarize(empty))

    def test_truncate_strips_files_then_commits(self):
        raw = raw_fixture()
        raw["commits"]["me/proj"] = [
            {"sha": f"s{i}", "commit": {"message": f"Feature {i}",
                                        "author": {"date": "2026-10-07T10:00:00Z"}}}
            for i in range(200)
        ]
        raw["commit_details"] = {f"s{i}": {"files": [{"filename": f"f{i}.py"}]} for i in range(200)}
        pack = collect.build_pack(raw, {}, SINCE, UNTIL)
        pack = collect._truncate(pack, limit=5000)
        self.assertLessEqual(len(json.dumps(pack)), 5000)


class PeriodTests(unittest.TestCase):
    def test_default_period_is_a_window(self):
        since, until = collect.default_period(7, now=datetime(2026, 10, 8, tzinfo=timezone.utc))
        self.assertTrue(since.startswith("2026-10-01"))
        self.assertTrue(until.startswith("2026-10-08"))


class RemoteParseTests(unittest.TestCase):
    def test_https_and_ssh_remotes(self):
        self.assertEqual(
            publish.parse_remote("https://github.com/dataengineergaurav/dataengineergaurav.github.io.git"),
            ("dataengineergaurav", "dataengineergaurav.github.io"),
        )
        self.assertEqual(
            publish.parse_remote("git@github.com:owner/repo.git"),
            ("owner", "repo"),
        )


class PublishGuardTests(unittest.TestCase):
    def _init_repo(self, root):
        for args in (("init", "-q"), ("config", "user.email", "t@e.st"),
                     ("config", "user.name", "t")):
            subprocess.run(["/usr/bin/git", *args], cwd=root, check=True, capture_output=True)

    def test_guard_accepts_single_untracked_post(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._init_repo(root)
            (root / "_posts").mkdir()
            (root / "_posts" / "2026-10-05-weekly-progress.md").write_text("x", encoding="utf-8")
            publish.only_change_guard(
                ["_posts/2026-10-05-weekly-progress.md"], repo_root=root)

    def test_guard_rejects_extra_path(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._init_repo(root)
            (root / "_posts").mkdir()
            (root / "_posts" / "2026-10-05-weekly-progress.md").write_text("x", encoding="utf-8")
            (root / "stray.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(SystemExit):
                publish.only_change_guard(
                    ["_posts/2026-10-05-weekly-progress.md"], repo_root=root)

    def test_guard_rejects_wrong_post_name(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._init_repo(root)
            (root / "_posts").mkdir()
            (root / "_posts" / "2026-10-05-weekly-progress.md").write_text("x", encoding="utf-8")
            with self.assertRaises(SystemExit):
                publish.only_change_guard(["_posts/2026-10-05-other.md"], repo_root=root)

    def test_guard_accepts_the_post_plus_the_synced_cv(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._init_repo(root)
            (root / "_posts").mkdir()
            (root / "_posts" / "2026-10-05-weekly-progress.md").write_text("x", encoding="utf-8")
            (root / publish.CV_PDF).write_text("x", encoding="utf-8")
            (root / publish.CV_VERSION).write_text("x", encoding="utf-8")

            publish.only_change_guard(
                ["_posts/2026-10-05-weekly-progress.md", publish.CV_PDF, publish.CV_VERSION],
                required=["_posts/2026-10-05-weekly-progress.md"],
                repo_root=root,
            )

    def test_guard_requires_the_post_to_be_present(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._init_repo(root)
            with self.assertRaises(SystemExit):
                publish.only_change_guard(
                    ["_posts/2026-10-05-weekly-progress.md"], repo_root=root)


class SkillContractTests(unittest.TestCase):
    def test_every_skill_has_frontmatter(self):
        for name in SKILL_NAMES:
            path = SKILLS_DIR / name / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(path.is_file(), f"missing {path}")
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                self.assertIn(f"name: {name}", text)
                self.assertIn("description:", text.split("---", 2)[1])

    def test_orchestrator_forbids_git(self):
        text = (SKILLS_DIR / "publish-weekly-progress" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("never commit", text.lower())
        self.assertIn("publish.py", text)


class SetupScriptTests(unittest.TestCase):
    def test_refuses_outside_canonical_checkout(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            dest = root / "automation" / "weekly-progress"
            dest.mkdir(parents=True)
            (dest / "setup.sh").write_bytes((AUTOMATION / "setup.sh").read_bytes())
            result = subprocess.run(
                ["/bin/bash", str(dest / "setup.sh"), "install"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("canonical checkout", result.stderr)

    def test_unknown_command_usage(self):
        result = subprocess.run(
            ["/bin/bash", str(AUTOMATION / "setup.sh"), "bogus"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()
