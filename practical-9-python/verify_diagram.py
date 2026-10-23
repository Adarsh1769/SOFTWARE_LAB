"""Verify the library ER diagram source and render it with Graphviz."""

import argparse
import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "library_er.dot"
DEFAULT_OUTPUT = HERE / "library_er.svg"
REQUIRED_ENTITIES = ("MEMBER", "BOOK", "AUTHOR", "BOOK_AUTHOR", "COPY", "LOAN")
REQUIRED_RELATIONSHIPS = (
    ("BOOK", "COPY"),
    ("MEMBER", "LOAN"),
    ("COPY", "LOAN"),
    ("BOOK", "BOOK_AUTHOR"),
    ("AUTHOR", "BOOK_AUTHOR"),
)


def find_graphviz():
    """Find Graphviz on PATH or in the standard Windows installation folder."""
    dot = shutil.which("dot")
    if dot:
        return dot
    program_files = Path(r"C:\Program Files")
    windows_install = program_files / "Graphviz" / "bin" / "dot.exe"
    return str(windows_install) if windows_install.is_file() else None


def verify_source(source_text):
    """Return a list of missing entities or relationship declarations."""
    issues = []
    for entity in REQUIRED_ENTITIES:
        if f"{entity} [label=<" not in source_text:
            issues.append(f"Missing entity definition: {entity}")
    for parent, child in REQUIRED_RELATIONSHIPS:
        if f"{parent} -> {child} [" not in source_text:
            issues.append(f"Missing relationship: {parent} to {child}")
    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Check the library ER diagram source and render it to SVG."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the Graphviz DOT source",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for the rendered SVG output",
    )
    args = parser.parse_args()

    try:
        source_text = args.source.read_text(encoding="utf-8")
    except OSError as error:
        parser.error(f"Could not read diagram source {args.source}: {error}")

    issues = verify_source(source_text)
    if issues:
        print("Diagram verification: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    dot = find_graphviz()
    if dot is None:
        parser.error(
            "Graphviz 'dot' was not found. Install Graphviz and ensure its bin "
            "directory is on PATH."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [dot, "-Tsvg", str(args.source), "-o", str(args.output)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() or str(error)
        print(f"Graphviz render failed: {message}")
        return 1
    except OSError as error:
        print(f"Could not run Graphviz: {error}")
        return 1

    if not args.output.is_file() or args.output.stat().st_size == 0:
        print(f"Graphviz did not create a non-empty output file: {args.output}")
        return 1

    rendered = args.output.read_text(encoding="utf-8")
    missing_entities = [name for name in REQUIRED_ENTITIES if name not in rendered]
    if missing_entities:
        print(
            "Rendered SVG is missing expected entities: "
            + ", ".join(missing_entities)
        )
        return 1

    print(
        f"Diagram source: PASS ({len(REQUIRED_ENTITIES)} entities, "
        f"{len(REQUIRED_RELATIONSHIPS)} relationships)"
    )
    print(f"Graphviz render: PASS ({args.output})")
    print("Rendered entity labels: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
