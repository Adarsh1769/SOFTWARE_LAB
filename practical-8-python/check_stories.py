"""Check basic completeness and traceability of user stories against an SRS."""

import argparse
import re
from pathlib import Path


REQUIREMENT_PATTERN = re.compile(r"^\s*(REQ-\d+)\s*:", re.MULTILINE)
STORY_HEADING_PATTERN = re.compile(r"^## \[(REQ-\d+)\].*$", re.MULTILINE)
STORY_TEMPLATE_PATTERN = re.compile(
    r"^\s*As an?\s+.+?\s+I want\s+.+?\s+so that\s+.+[.!?]?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
CRITERIA_PATTERN = {
    label: re.compile(rf"\b{label}\s*:", re.IGNORECASE)
    for label in ("Given", "When", "Then")
}
ACCEPTANCE_BULLET_PATTERN = re.compile(r"^\s*[-*]\s+.+$", re.MULTILINE)


def extract_story_sections(stories_text):
    """Return each story's requirement ID and section text."""
    headings = list(STORY_HEADING_PATTERN.finditer(stories_text))
    sections = {}
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(stories_text)
        sections[heading.group(1)] = stories_text[heading.end() : end]
    return sections


def evaluate(srs_text, stories_text):
    """Return per-requirement completeness checks and their pass status."""
    requirement_ids = REQUIREMENT_PATTERN.findall(srs_text)
    sections = extract_story_sections(stories_text)
    results = []

    for requirement_id in requirement_ids:
        section = sections.get(requirement_id, "")
        acceptance_criteria = ACCEPTANCE_BULLET_PATTERN.findall(section)
        criteria = {
            label: bool(acceptance_criteria)
            and all(pattern.search(criterion) for criterion in acceptance_criteria)
            for label, pattern in CRITERIA_PATTERN.items()
        }
        results.append(
            {
                "id": requirement_id,
                "covered": bool(section),
                "story_format": bool(STORY_TEMPLATE_PATTERN.search(section)),
                "criteria": criteria,
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check user-story coverage, story format, and Given/When/Then criteria."
    )
    parser.add_argument(
        "stories",
        type=Path,
        help="Markdown file containing the user stories to evaluate",
    )
    parser.add_argument(
        "--srs",
        type=Path,
        default=Path(__file__).with_name("srs_excerpt.txt"),
        help="SRS text file (defaults to the included excerpt)",
    )
    args = parser.parse_args()

    results = evaluate(
        args.srs.read_text(encoding="utf-8"),
        args.stories.read_text(encoding="utf-8"),
    )
    if not results:
        parser.error(f"No requirement IDs found in {args.srs}")

    passed = 0
    total = len(results) * 5
    print("Completeness check")
    for result in results:
        checks = [
            ("covered", result["covered"]),
            ("story format", result["story_format"]),
            *result["criteria"].items(),
        ]
        for _, check_passed in checks:
            passed += check_passed
        details = ", ".join(
            f"{label}: {'PASS' if check_passed else 'FAIL'}"
            for label, check_passed in checks
        )
        print(f"{result['id']}: {details}")

    print(f"Completeness: {passed}/{total} checks passed")
    complete = passed == total
    print(f"Result: {'COMPLETE' if complete else 'INCOMPLETE'}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
