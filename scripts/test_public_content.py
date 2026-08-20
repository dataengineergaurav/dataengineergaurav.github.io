import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


FORBIDDEN_NAMES = (
    "sagesure", "ishir", "cannasp yglass".replace(" ", ""), "petfolk",
    "tradetips", "casepoint", "nhs", "archetypal ai", "6overn.ai",
)

SOURCE_PATHS = (
    Path("index.md"), Path("work.md"), Path("_config.yml"),
    Path("_layouts"), Path("_projects"),
)

HOMEPAGE_PROOF = (
    "300+", "2M+", "7+ years", "Open to select strategic leadership roles",
)


def public_text_files(root: Path) -> list[Path]:
    if (root / "index.md").exists():
        paths = SOURCE_PATHS
        suffixes = {".md", ".html", ".yml", ".yaml"}
    else:
        paths = (Path("."),)
        suffixes = {".html", ".xml", ".txt"}
    files = []
    for relative in paths:
        candidate = root / relative
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*") if path.suffix in suffixes)
    return sorted(files)


def find_forbidden_names(root: Path) -> list[str]:
    findings = []
    for path in public_text_files(root):
        text = path.read_text(encoding="utf-8").casefold()
        for name in FORBIDDEN_NAMES:
            if name in text:
                findings.append(f"{path}: {name}")
    return findings


def find_public_content_findings(root: Path) -> list[str]:
    findings = find_forbidden_names(root)
    if not (root / "index.md").exists():
        homepage = root / "index.html"
        text = homepage.read_text(encoding="utf-8").casefold() if homepage.exists() else ""
        findings.extend(f"{homepage}: missing {proof}" for proof in HOMEPAGE_PROOF if proof.casefold() not in text)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public content for private organization names.")
    parser.add_argument("--root", type=Path, required=True)
    findings = find_public_content_findings(parser.parse_args().root)
    for finding in findings:
        print(finding)
    return int(bool(findings))


class PublicContentTests(unittest.TestCase):
    def test_discovers_source_files(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.md").write_text("home", encoding="utf-8")
            (root / "_layouts").mkdir()
            (root / "_layouts" / "default.html").write_text("layout", encoding="utf-8")
            (root / "ignored.txt").write_text("ignored", encoding="utf-8")

            self.assertEqual(public_text_files(root), [root / "_layouts" / "default.html", root / "index.md"])

    def test_finds_forbidden_names_case_insensitively(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.md").write_text("Worked at ISHIR.", encoding="utf-8")

            self.assertEqual(find_forbidden_names(root), [f"{root / 'index.md'}: ishir"])

    def test_clean_directory_has_no_findings(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.md").write_text("Independent data leader.", encoding="utf-8")

            self.assertEqual(find_forbidden_names(root), [])


if __name__ == "__main__":
    raise SystemExit(main())
