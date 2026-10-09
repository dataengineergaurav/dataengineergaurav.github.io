"""Public-content policy: the organization names and claims that must not ship.

Kept dependency-free so both the CI content check and the CV pipeline can import it
without pulling in a PDF library they do not need.
"""

FORBIDDEN_NAMES = (
    "sagesure", "ishir", "cannasp yglass".replace(" ", ""), "petfolk",
    "tradetips", "casepoint", "nhs", "archetypal ai", "6overn.ai",
)

TESTIMONIAL_NAMES = (
    ("ai squared", "Benjamin Harvey, Ph.D.", "Founder of AI Squared"),
    ("department of justice", "Ivette Basterrechea", "Department of Justice"),
    ("google", "Le Zhang", ""),
)

RETIRED_CLAIMS = ("$3b+",)

# Names that are acceptable on the published CV but forbidden in site prose:
# employers-of-record are already public, clients are not. The testimonial
# restrictions above do not apply to a CV, so its denylist is scoped explicitly.
CV_ALLOWED_NAMES = ("ishir", "cannaspyglass", "casepoint", "ai squared")


def cv_forbidden_names() -> tuple[str, ...]:
    """The denylist for a PDF: the full list minus the names a CV may carry."""
    return tuple(
        name for name in FORBIDDEN_NAMES + RETIRED_CLAIMS if name not in CV_ALLOWED_NAMES
    )
