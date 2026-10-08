import importlib.util
import sys
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


if __name__ == "__main__":
    unittest.main()
