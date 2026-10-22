"""Tests that check the refactored function against the legacy behavior."""

import unittest

from clean import summarize_orders
from messy import process


class RefactoringTests(unittest.TestCase):
    def test_refactored_output_matches_legacy_output(self) -> None:
        orders = [
            ("Notebook", 2, 25.00),
            ("Desk", 1, 150.00),
            ("Invalid quantity", 0, 12.00),
            ("Invalid price", 1, -5.00),
            ("Incomplete row", 10),
        ]
        self.assertEqual(process(orders), summarize_orders(orders))

    def test_empty_input_returns_zero_summary(self) -> None:
        self.assertEqual(
            {"total": 0, "units": 0, "average": 0},
            summarize_orders([]),
        )

    def test_discount_applies_only_above_threshold(self) -> None:
        orders = [("Threshold", 1, 100), ("Discounted", 1, 200)]
        self.assertEqual(
            {"total": 280.0, "units": 2, "average": 140.0},
            summarize_orders(orders),
        )


if __name__ == "__main__":
    unittest.main()
