"""Regression tests for the Practical 11 payment helper."""

import unittest

from payments import calculate_total


class PaymentTotalTests(unittest.TestCase):
    def test_total_includes_subtotal_and_tax(self):
        self.assertEqual(calculate_total(100.0, 0.08), 108.0)

    def test_zero_tax_returns_subtotal(self):
        self.assertEqual(calculate_total(25.0, 0.0), 25.0)

    def test_tax_is_rounded_to_cents(self):
        self.assertEqual(calculate_total(19.99, 0.075), 21.49)


if __name__ == "__main__":
    unittest.main()
