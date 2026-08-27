import argparse
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from urllib.parse import urlparse


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

RETIRED_CLAIMS = ("$3b+",)

GOOGLE_SERVICE_HOSTS = {"www.googletagmanager.com", "maps.googleapis.com", "fonts.googleapis.com"}


class RenderedTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def rendered_text(markup):
    parser = RenderedTextParser()
    parser.feed(markup)
    parser.close()
    return "".join(parser.parts)


def mask_approved_google_service_host(match):
    url = match.group()
    try:
        parsed = urlparse(url)
    except ValueError:
        return url
    if parsed.hostname not in GOOGLE_SERVICE_HOSTS:
        return url
    before, hostname, after = parsed.netloc.rpartition(parsed.hostname)
    return parsed._replace(netloc=before + hostname.replace("google", "") + after).geturl()


def public_text_files(root: Path) -> list[Path]:
    if (root / "index.md").exists():
        suffixes = {".md", ".html", ".yml", ".yaml"}
        return sorted(
            path for path in root.rglob("*")
            if path.suffix in suffixes
            and not SOURCE_EXCLUDED_DIRS.intersection(path.relative_to(root).parts)
            and path.relative_to(root) not in {Path("README.md"), Path("final-review.md")}
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
        for name, author, attribution in TESTIMONIAL_NAMES:
            text = re.sub(
                rf"(<cite\b[^>]*>\s*<strong>\s*<a\b[^>]*>{re.escape(author.casefold())}</a>\s*</strong>\s*·\s*{re.escape(attribution.casefold()[:-len(name)])}){re.escape(name)}(?=\s*</cite>)",
                lambda match: match.group(1),
                text,
                flags=re.DOTALL,
            )
        searchable_texts = (unescape(text).casefold(), rendered_text(text).casefold())
        searchable_texts = tuple(
            re.sub(
                r"google[ _-](analytics|cloud|maps|sheets)",
                r"\1",
                re.sub(
                    r"https?://[^\s\"'<>]+",
                    mask_approved_google_service_host,
                    searchable,
                ),
            )
            for searchable in searchable_texts
        )
        forbidden = FORBIDDEN_NAMES + tuple(name for name, _, _ in TESTIMONIAL_NAMES) + RETIRED_CLAIMS
        for name in forbidden:
            if any(name in searchable for searchable in searchable_texts):
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
    def test_work_page_distinguishes_maintained_and_contributed_projects(self):
        root = Path(__file__).resolve().parents[1]
        work = (root / "work.md").read_text(encoding="utf-8")

        maintained = work.index("Maintained projects")
        contributed = work.index("Open-source contributions")
        self.assertLess(maintained, contributed)
        for repository in (
            "rental-market-dynamics-dubai", "hermes-gsheets", "setu",
            "sportsdataverse/sportsdataverse-py/pull/82",
            "catalyst-cooperative/pudl/pull/3931",
            "catalyst-cooperative/pudl/pull/3983",
            "catalyst-cooperative/pudl/pull/2951",
            "catalyst-cooperative/pudl/pull/2953",
        ):
            with self.subTest(repository=repository):
                self.assertIn(repository, work)
        self.assertIn("closed without merge", work)

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
            (root / "final-review.md").write_text("review", encoding="utf-8")
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

            page.write_text(
                "Google Analytics, Google Cloud, Google Maps, and Google Sheets",
                encoding="utf-8",
            )

            self.assertEqual(find_forbidden_names(root), [])

            page.write_text("Google engagement", encoding="utf-8")
            self.assertEqual(find_forbidden_names(root), [f"{page}: google"])

    def test_google_service_urls_require_exact_hosts_in_source_and_generated_content(self):
        with TemporaryDirectory() as temporary:
            cases = (
                (
                    "exact hosts",
                    "https://www.googletagmanager.com/gtag/js "
                    "https://maps.googleapis.com/maps/api/js",
                    False,
                ),
                (
                    "user-info lookalikes",
                    "https://www.googletagmanager.com@attacker.example/gtag.js "
                    "https://maps.googleapis.com@attacker.example/maps.js",
                    True,
                ),
                (
                    "subdomain and lookalike hosts",
                    "https://notgoogletagmanager.com/gtag/js "
                    "https://maps.googleapis.com.example/maps/api/js",
                    True,
                ),
                (
                    "organization leak on service URL",
                    "https://maps.googleapis.com/projects/Google-migration",
                    True,
                ),
                ("organization leak", "Google migration", True),
            )
            for mode, suffix, scanner in (
                ("source", "index.md", find_forbidden_names),
                ("generated", "index.html", find_public_content_findings),
            ):
                root = Path(temporary) / mode
                root.mkdir()
                page = root / suffix
                prefix = "" if mode == "source" else (
                    "300+ 2M+ 7+ years Open to select strategic leadership roles "
                )
                for case, content, rejected in cases:
                    with self.subTest(mode=mode, case=case):
                        page.write_text(prefix + content, encoding="utf-8")
                        expected = [f"{page}: google"] if rejected else []
                        self.assertEqual(scanner(root), expected)

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

    def test_generated_site_scans_normalized_rendered_text(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            homepage = root / "index.html"
            proof = "300+ 2M+ 7+ years Open to select strategic leadership roles "
            for case, content, finding in (
                ("HTML entity", "ISH&#73;R", "ishir"),
                ("element boundary", "Case<strong>point</strong>", "casepoint"),
            ):
                with self.subTest(case=case):
                    homepage.write_text(proof + content, encoding="utf-8")
                    self.assertEqual(
                        find_public_content_findings(root),
                        [f"{homepage}: {finding}"],
                    )

    def test_rejects_retired_claim_in_source_and_generated_content(self):
        with TemporaryDirectory() as temporary:
            for mode, suffix, scanner, prefix in (
                ("source", "index.md", find_forbidden_names, ""),
                (
                    "generated",
                    "index.html",
                    find_public_content_findings,
                    "300+ 2M+ 7+ years Open to select strategic leadership roles ",
                ),
            ):
                with self.subTest(mode=mode):
                    root = Path(temporary) / mode
                    root.mkdir()
                    page = root / suffix
                    page.write_text(prefix + "$3B+ worth of data projects delivered", encoding="utf-8")
                    self.assertEqual(scanner(root), [f"{page}: $3b+"])

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
