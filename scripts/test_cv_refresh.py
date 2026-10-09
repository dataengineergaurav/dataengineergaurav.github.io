"""Tests for the weekly CV refresh pipeline's deterministic scripts. No network.

Mirrors scripts/test_weekly_progress.py: the pipeline modules are loaded from
automation/weekly-progress/ by path, so nothing needs to be installed.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "automation" / "weekly-progress"


def load(name):
    spec = importlib.util.spec_from_file_location(name, PIPELINE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cv_policy = load("cv_policy")
cv_guard = load("cv_guard")


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


if __name__ == "__main__":
    unittest.main()
