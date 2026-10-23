"""Tests for the Practical 11 build-log analysis."""

import unittest

from analyze_log import analyze


FAILING_LOG = """\
FAIL: test_total_includes_subtotal_and_tax (test_payments.PaymentTotalTests.test_total_includes_subtotal_and_tax)
AssertionError: 8.0 != 108.0
"""

FAILING_SOURCE = """\
def calculate_total(subtotal, tax_rate):
    tax = subtotal * tax_rate
    return round(tax, 2)
"""
FIXED_SOURCE = """\
def calculate_total(subtotal, tax_rate):
    tax = subtotal * tax_rate
    return round(subtotal + tax, 2)
"""


class AnalyzeLogTests(unittest.TestCase):
    def test_identifies_tax_only_return(self):
        report = analyze(FAILING_LOG, FAILING_SOURCE)

        self.assertIn("test_total_includes_subtotal_and_tax", report)
        self.assertIn("actual value `8`", report)
        self.assertIn("Probable cause", report)
        self.assertIn("return round(tax, 2)", report)
        self.assertIn("round(subtotal + tax, 2)", report)

    def test_can_analyze_pre_fix_log_after_source_is_corrected(self):
        report = analyze(FAILING_LOG, FIXED_SOURCE)

        self.assertIn("current source already contains the correction", report)
        self.assertIn("earlier failing revision", report)

    def test_rejects_log_without_assertion_failure(self):
        with self.assertRaises(ValueError):
            analyze("Ran 3 tests\nOK\n", FAILING_SOURCE)


if __name__ == "__main__":
    unittest.main()
