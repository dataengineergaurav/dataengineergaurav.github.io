import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


wiki = load_module("wiki_ingest_under_test", REPO_ROOT / "scripts" / "wiki_ingest.py")


class ConvertWikilinkTests(unittest.TestCase):
    def test_links_public_targets(self):
        out = wiki._convert_wikilinks("See [[hermes-runtime]].", {"hermes-runtime"})
        self.assertEqual(out, "See [hermes-runtime](/wiki/hermes-runtime/).")

    def test_private_target_is_unlinked(self):
        out = wiki._convert_wikilinks("See [[blog-automation]].", {"hermes-runtime"})
        self.assertEqual(out, "See blog-automation.")

    def test_aliased_link_uses_label(self):
        out = wiki._convert_wikilinks("See [[blog-automation|the notes]].", {"hermes-runtime"})
        self.assertEqual(out, "See the notes.")

    def test_no_allowlist_keeps_legacy_behaviour(self):
        out = wiki._convert_wikilinks("See [[anything]].")
        self.assertEqual(out, "See [anything](/wiki/anything/).")


class CollectNotesTests(unittest.TestCase):
    def setUp(self):
        self._orig_inbox = wiki.INBOX_DIR
        self._orig_memory = wiki.MEMORY_DIR
        self.tmp = tempfile.TemporaryDirectory()
        self.inbox = Path(self.tmp.name) / "inbox"
        self.memory = Path(self.tmp.name) / "memories"
        self.inbox.mkdir()
        self.memory.mkdir()
        wiki.INBOX_DIR = self.inbox
        wiki.MEMORY_DIR = self.memory
        self.state = {"processed_notes": {}}

    def tearDown(self):
        wiki.INBOX_DIR = self._orig_inbox
        wiki.MEMORY_DIR = self._orig_memory
        self.tmp.cleanup()

    def test_collects_inbox_and_memories(self):
        (self.inbox / "note.md").write_text("a personal note")
        (self.memory / "USER.md").write_text("Prefers polished, formal English.")
        names = {n["name"] for n in wiki._collect_notes(self.state)}
        self.assertEqual(names, {"note.md", "memory:USER.md"})

    def test_empty_memory_is_ignored(self):
        (self.memory / "MEMORY.md").write_text("   \n")
        self.assertEqual(wiki._collect_notes(self.state), [])

    def test_unchanged_memory_is_skipped(self):
        (self.memory / "MEMORY.md").write_text("a durable fact")
        for note in wiki._collect_notes(self.state):
            self.state["processed_notes"][note["name"]] = note["hash"]
        self.assertEqual(wiki._collect_notes(self.state), [])

    def test_changed_memory_is_recollected(self):
        (self.memory / "USER.md").write_text("v1")
        for note in wiki._collect_notes(self.state):
            self.state["processed_notes"][note["name"]] = note["hash"]
        (self.memory / "USER.md").write_text("v2")
        self.assertEqual([n["name"] for n in wiki._collect_notes(self.state)], ["memory:USER.md"])

    def test_missing_dirs_are_tolerated(self):
        wiki.INBOX_DIR = self.inbox / "absent"
        wiki.MEMORY_DIR = self.memory / "absent"
        self.assertEqual(wiki._collect_notes(self.state), [])


class BackupTests(unittest.TestCase):
    def setUp(self):
        self._orig_root = wiki.WIKI_ROOT
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "vault"
        self.root.mkdir()
        self._git("init", "-q")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test")
        self._git("config", "push.default", "current")
        wiki.WIKI_ROOT = self.root

    def tearDown(self):
        wiki.WIKI_ROOT = self._orig_root
        self.tmp.cleanup()

    def _git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)

    def test_non_repo_is_reported(self):
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        wiki.WIKI_ROOT = plain
        self.assertIn("not a git repository", wiki.backup())

    def test_commits_new_content(self):
        (self.root / "note.md").write_text("hello")
        self.assertEqual(wiki.backup(), "backup: committed")

    def test_dry_run_writes_nothing(self):
        (self.root / "note.md").write_text("hello")
        self.assertIn("would commit", wiki.backup(dry_run=True))
        self.assertEqual(wiki._run_git("status", "--porcelain", cwd=self.root).stdout.strip(), "?? note.md")

    def test_second_run_is_a_noop(self):
        (self.root / "note.md").write_text("hello")
        wiki.backup()
        self.assertEqual(wiki.backup(), "backup: no changes")

    def test_push_without_remote_is_not_fatal(self):
        (self.root / "note.md").write_text("hello")
        self.assertIn("no remote", wiki.backup(push=True))

    def test_pushes_to_remote(self):
        bare = Path(self.tmp.name) / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
        self._git("remote", "add", "origin", str(bare))
        (self.root / "note.md").write_text("hello")
        self.assertEqual(wiki.backup(push=True), "backup: committed, pushed")
        local_head = wiki._run_git("rev-parse", "HEAD", cwd=self.root).stdout.strip()
        remote_head = subprocess.run(
            ["git", "--git-dir", str(bare), "rev-parse", "master"],
            capture_output=True, text=True).stdout.strip()
        self.assertEqual(local_head, remote_head)


if __name__ == "__main__":
    unittest.main()
