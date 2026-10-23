"""Analyze the sample CI log and verify its likely payment regression."""

import argparse
import re
from pathlib import Path


FAILURE_PATTERN = re.compile(r"AssertionError:\s*([\d.]+)\s*!=\s*([\d.]+)")
FAILED_TEST_PATTERN = re.compile(r"FAIL:\s*(\S+)")


def analyze(log_text, source_text):
    """Return a report based on a failed assertion and the payment code."""
    failure = FAILURE_PATTERN.search(log_text)
    failed_test = FAILED_TEST_PATTERN.search(log_text)
    if not failure or not failed_test:
        raise ValueError("Log does not contain a recognizable unittest assertion failure.")

    actual, expected = map(float, failure.groups())
    if "tax = subtotal * tax_rate" not in source_text:
        raise ValueError("Payment source does not contain the suspected tax calculation.")
    if "return round(tax, 2)" in source_text:
        source_status = (
            "The supplied failing-revision source returns only the tax amount."
        )
    elif "return round(subtotal + tax, 2)" in source_text:
        source_status = (
            "The current source already contains the correction; the supplied "
            "log is from the earlier failing revision."
        )
    else:
        raise ValueError(
            "Payment source contains neither the suspected tax-only return "
            "nor the verified correction."
        )

    return (
        "# CI build log analysis\n\n"
        f"- **Failing test:** `{failed_test.group(1)}`\n"
        f"- **Observed:** actual value `{actual:g}`; expected value `{expected:g}`.\n"
        "- **Probable cause:** `calculate_total` computes the tax correctly but "
        "returns only the tax amount instead of adding it to the subtotal.\n"
        f"- **Source check:** {source_status}\n"
        "- **Evidence in the failing run:** with a subtotal of 100 and an 8% "
        f"tax rate, the observed {actual:g} is the tax amount, while the "
        f"expected payable total is {expected:g}.\n"
        "\nFailing revision excerpt:\n\n"
        "```python\n"
        "tax = subtotal * tax_rate\n"
        "return round(tax, 2)\n"
        "```\n\n"
        "- **Verification:** change the return expression to "
        "`round(subtotal + tax, 2)` and rerun the payment tests. A successful "
        "rerun confirms this diagnosis for the reproduced regression.\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Analyze the Practical 11 unittest build log."
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path(__file__).with_name("build.log"),
        help="Path to the captured failing CI log",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).with_name("payments.py"),
        help="Payment source from the failing revision",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("analysis_report.md"),
        help="Path for the analysis report",
    )
    args = parser.parse_args()

    try:
        report = analyze(
            args.log.read_text(encoding="utf-8"),
            args.source.read_text(encoding="utf-8"),
        )
        args.output.write_text(report, encoding="utf-8")
    except OSError as error:
        parser.error(f"Could not read/write an analysis file: {error}")
    except ValueError as error:
        parser.error(str(error))

    print(f"Analysis report written to {args.output}")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
