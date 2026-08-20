import argparse
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest


FORBIDDEN_NAMES = (
    "sagesure", "ishir", "cannasp yglass".replace(" ", ""), "petfolk",
    "tradetips", "casepoint", "nhs", "archetypal ai", "6overn.ai",
)

SOURCE_EXCLUDED_DIRS = {
    ".git", ".github", ".pytest_cache", ".superdesign", ".superpowers", "_site",
    "automation", "docs", "script", "scripts", "vendor",
}

TESTIMONIAL_NAMES = (
    ("ai squared", "Benjamin Harvey, Ph.D.", "Founder of AI Squared"),
    ("department of justice", "Ivette Basterrechea", "Department of Justice"),
    ("google", "Le Zhang", ""),
)

HOMEPAGE_PROOF = (
    "300+", "2M+", "7+ years", "Open to select strategic leadership roles",
)


def public_text_files(root: Path) -> list[Path]:
    if (root / "index.md").exists():
        suffixes = {".md", ".html", ".yml", ".yaml"}
        return sorted(
            path for path in root.rglob("*")
            if path.suffix in suffixes
            and not SOURCE_EXCLUDED_DIRS.intersection(path.relative_to(root).parts)
            and path.relative_to(root) not in {Path("README.md"), Path("_projects/README.md")}
        )
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
        text = re.sub(r"google[ _-](analytics|cloud|maps)", r"\1", text)
        for name, author, attribution in TESTIMONIAL_NAMES:
            text = re.sub(
                rf"(<cite\b[^>]*>\s*<strong>\s*<a\b[^>]*>{re.escape(author.casefold())}</a>\s*</strong>\s*·\s*{re.escape(attribution.casefold()[:-len(name)])}){re.escape(name)}(?=\s*</cite>)",
                lambda match: match.group(1),
                text,
                flags=re.DOTALL,
            )
        for name in FORBIDDEN_NAMES + tuple(name for name, _, _ in TESTIMONIAL_NAMES):
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
            (root / "_includes").mkdir()
            (root / "_includes" / "head.html").write_text("include", encoding="utf-8")
            (root / "_posts").mkdir()
            (root / "_posts" / "post.md").write_text("post", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "private.md").write_text("private", encoding="utf-8")
            (root / "scripts").mkdir()
            (root / "scripts" / "private.md").write_text("private", encoding="utf-8")
            (root / "ignored.txt").write_text("ignored", encoding="utf-8")

            self.assertEqual(public_text_files(root), [
                root / "_includes" / "head.html",
                root / "_layouts" / "default.html",
                root / "_posts" / "post.md",
                root / "index.md",
            ])

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

    def test_allows_google_technology_references(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "index.md"
            page.write_text("<cite><strong><a>Le Zhang</a></strong> · Google</cite>", encoding="utf-8")

            self.assertEqual(find_forbidden_names(root), [])

            page.write_text("Google Analytics, Google Cloud, and Google Maps", encoding="utf-8")

            self.assertEqual(find_forbidden_names(root), [])

            page.write_text("Google engagement", encoding="utf-8")
            self.assertEqual(find_forbidden_names(root), [f"{page}: google"])

    def test_allows_approved_testimonial_attribution_only(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "index.md"
            page.write_text("<cite>Jane Doe · Founder of AI Squared</cite>", encoding="utf-8")

            self.assertEqual(find_forbidden_names(root), [f"{page}: ai squared"])

            page.write_text(
                "<cite>Benjamin Harvey, Ph.D. · Founder of AI Squared</cite>",
                encoding="utf-8",
            )
            self.assertEqual(find_forbidden_names(root), [f"{page}: ai squared"])

            page.write_text(
                "<cite><strong><a>Benjamin Harvey, Ph.D.</a></strong> · Founder of AI Squared</cite>",
                encoding="utf-8",
            )

            self.assertEqual(find_forbidden_names(root), [])

            page.write_text(
                "<cite><strong><a>Benjamin Harvey, Ph.D.</a></strong> advised the AI Squared engagement · Founder of AI Squared</cite>",
                encoding="utf-8",
            )
            self.assertEqual(find_forbidden_names(root), [f"{page}: ai squared"])

            page.write_text(
                "<cite><strong><a>Benjamin Harvey, Ph.D.</a></strong> · Founder of AI Squared</cite>\nAI Squared engagement",
                encoding="utf-8",
            )
            self.assertEqual(find_forbidden_names(root), [f"{page}: ai squared"])

    def test_generated_site_requires_proof_and_scans_nested_pages(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text(
                "300+ 2M+ 7+ years Open to select strategic leadership roles",
                encoding="utf-8",
            )
            (root / "blog").mkdir()
            (root / "blog" / "index.html").write_text("ISHIR", encoding="utf-8")

            self.assertEqual(
                find_public_content_findings(root),
                [f"{root / 'blog' / 'index.html'}: ishir"],
            )

    def test_generated_site_reports_missing_homepage_proof(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            homepage = root / "index.html"
            homepage.write_text("300+ 2M+ 7+ years", encoding="utf-8")

            self.assertEqual(
                find_public_content_findings(root),
                [f"{homepage}: missing Open to select strategic leadership roles"],
            )

    def test_generated_site_rejects_google_engagement(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text(
                "300+ 2M+ 7+ years Open to select strategic leadership roles Google engagement",
                encoding="utf-8",
            )

            self.assertEqual(find_public_content_findings(root), [f"{root / 'index.html'}: google"])


if __name__ == "__main__":
    raise SystemExit(main())
