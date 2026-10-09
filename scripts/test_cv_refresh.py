"""Tests for the weekly CV refresh pipeline's deterministic scripts. No network.

Mirrors scripts/test_weekly_progress.py: the pipeline modules are loaded from
automation/weekly-progress/ by path, so nothing needs to be installed.
"""
import importlib.util
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "automation" / "weekly-progress"
sys.path.insert(0, str(PIPELINE))


def load(name):
    spec = importlib.util.spec_from_file_location(name, PIPELINE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cv_policy = load("cv_policy")
cv_guard = load("cv_guard")
cv_publish = load("cv_publish")
cv_sync = load("cv_sync")


class CvPolicyTests(unittest.TestCase):
    def test_flags_a_client_name(self):
        self.assertEqual(cv_policy.text_violations("Work at SageSure"), ["sagesure"])

    def test_allows_an_employer_name(self):
        self.assertEqual(cv_policy.text_violations("Senior Data Engineer, ISHIR"), [])

    def test_empty_extraction_fails_closed(self):
        self.assertEqual(cv_policy.pdf_text_violations(""), ["unreadable pdf"])

    def test_flags_a_retired_claim(self):
        self.assertEqual(cv_policy.text_violations("$3B+ delivered"), ["$3b+"])

    def test_clean_text_passes(self):
        self.assertEqual(cv_policy.text_violations("Senior Data Engineer, 7+ years"), [])


class CvGuardTests(unittest.TestCase):
    def test_highlights_change_is_allowed(self):
        old = {"engagements": [{"id": "e1", "highlights": ["a"]}]}
        new = {"engagements": [{"id": "e1", "highlights": ["a", "b"]}]}
        self.assertEqual(cv_guard.violations(old, new), [])

    def test_date_change_is_rejected(self):
        old = {"engagements": [{"id": "e1", "start": "2024-04", "highlights": []}]}
        new = {"engagements": [{"id": "e1", "start": "2023-01", "highlights": []}]}
        self.assertEqual(cv_guard.violations(old, new), ["engagements[e1].start changed"])

    def test_meta_summary_change_is_rejected(self):
        old = {"meta": {"summary": "a"}}
        new = {"meta": {"summary": "b"}}
        self.assertEqual(cv_guard.violations(old, new), ["meta.summary changed"])

    def test_cap_rejects_sixth_highlight(self):
        new = {"engagements": [{"id": "e1", "highlights": ["a", "b", "c", "d", "e", "f"]}]}
        self.assertEqual(
            cv_guard.cap_violations(new), ["engagements[e1]: 6 highlights (cap 5)"]
        )

    def test_cap_allows_a_highlight_swapped_for_another(self):
        new = {"engagements": [{"id": "e1", "highlights": ["a", "b", "c", "d", "e"]}]}
        self.assertEqual(cv_guard.cap_violations(new), [])

    def test_moving_a_highlight_between_engagements_is_allowed(self):
        old = {"engagements": [{"id": "a", "highlights": ["x"]}, {"id": "b", "highlights": []}]}
        new = {"engagements": [{"id": "a", "highlights": []}, {"id": "b", "highlights": ["x"]}]}
        self.assertEqual(cv_guard.violations(old, new), [])

    def test_reordering_a_list_of_records_is_not_a_change(self):
        old = {"engagements": [{"id": "a", "start": "2024-01"}, {"id": "b", "start": "2020-01"}]}
        new = {"engagements": [{"id": "b", "start": "2020-01"}, {"id": "a", "start": "2024-01"}]}
        self.assertEqual(cv_guard.violations(old, new), [])

    def test_adding_an_engagement_is_rejected(self):
        old = {"engagements": [{"id": "a"}]}
        new = {"engagements": [{"id": "a"}, {"id": "b"}]}
        self.assertEqual(cv_guard.violations(old, new), ["engagements[b] added"])


class CvPublishTests(unittest.TestCase):
    def test_allow_list_accepts_the_expected_set(self):
        cv_publish.assert_only(cv_publish.CV_FILES, cv_publish.CV_FILES)

    def test_allow_list_rejects_an_unexpected_path(self):
        with self.assertRaises(SystemExit):
            cv_publish.assert_only(cv_publish.CV_FILES, cv_publish.CV_FILES + ["notes.txt"])

    def test_allow_list_rejects_a_missing_artifact(self):
        with self.assertRaises(SystemExit):
            cv_publish.assert_only(cv_publish.CV_FILES, cv_publish.CV_FILES[:-1])

    def test_branch_name_is_idempotent(self):
        self.assertEqual(cv_publish.branch_for("2026-10-12"), "cv-refresh/2026-10-12")

    def test_allow_list_names_the_source_of_truth(self):
        self.assertIn("data/experience.yaml", cv_publish.CV_FILES)


class CvSyncTests(unittest.TestCase):
    def _roots(self, temporary, with_source=True):
        cv_root = Path(temporary) / "cv"
        site_root = Path(temporary) / "site"
        cv_root.mkdir()
        site_root.mkdir()
        if with_source:
            (cv_root / cv_sync.CV_SOURCE).write_bytes(b"rendered-pdf")
        return cv_root, site_root

    def test_writes_a_marker_that_matches_the_copied_pdf(self):
        with TemporaryDirectory() as temporary:
            cv_root, site_root = self._roots(temporary)
            cv_sync.sync(cv_root, site_root)

            marker = json.loads((site_root / cv_sync.SITE_VERSION).read_text(encoding="utf-8"))
            self.assertEqual(marker["sha256"], cv_sync.sha256_file(site_root / cv_sync.SITE_PDF))
            self.assertTrue(marker["cv_commit"])

    def test_marker_check_passes_after_a_sync(self):
        with TemporaryDirectory() as temporary:
            cv_root, site_root = self._roots(temporary)
            cv_sync.sync(cv_root, site_root)

            self.assertEqual(cv_sync.marker_violations(site_root), [])

    def test_marker_check_rejects_a_swapped_pdf(self):
        with TemporaryDirectory() as temporary:
            cv_root, site_root = self._roots(temporary)
            cv_sync.sync(cv_root, site_root)
            (site_root / cv_sync.SITE_PDF).write_bytes(b"tampered")

            self.assertEqual(
                cv_sync.marker_violations(site_root),
                [f"{cv_sync.SITE_PDF}: sha256 does not match {cv_sync.SITE_VERSION}"],
            )

    def test_missing_marker_is_reported(self):
        with TemporaryDirectory() as temporary:
            _, site_root = self._roots(temporary)
            (site_root / cv_sync.SITE_PDF).write_bytes(b"x")

            self.assertEqual(
                cv_sync.marker_violations(site_root), [f"missing {cv_sync.SITE_VERSION}"]
            )

    def test_failure_leaves_the_site_pdf_untouched(self):
        with TemporaryDirectory() as temporary:
            cv_root, site_root = self._roots(temporary, with_source=False)
            (site_root / cv_sync.SITE_PDF).write_bytes(b"previous")

            with self.assertRaises(SystemExit):
                cv_sync.sync(cv_root, site_root)

            self.assertEqual((site_root / cv_sync.SITE_PDF).read_bytes(), b"previous")


if __name__ == "__main__":
    unittest.main()
