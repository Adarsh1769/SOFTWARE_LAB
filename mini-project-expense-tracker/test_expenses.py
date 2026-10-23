"""Tests for expense validation, persistence, and CLI behavior."""

import contextlib
import io
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from cli import main
from models import Expense, parse_amount, parse_expense_date
from storage import load_expenses, save_expenses


class ExpenseModelTests(unittest.TestCase):
    def test_amount_parser_preserves_decimal_value(self):
        self.assertEqual(parse_amount("19.99"), Decimal("19.99"))

    def test_rejects_non_positive_or_non_finite_amount(self):
        for amount in ("0", "-1", "NaN", "Infinity", "invalid"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                parse_amount(amount)

    def test_rejects_blank_category_and_description(self):
        with self.assertRaisesRegex(ValueError, "category"):
            Expense(Decimal("1"), "  ", "Bus fare", date(2026, 1, 1))
        with self.assertRaisesRegex(ValueError, "description"):
            Expense(Decimal("1"), "Travel", "  ", date(2026, 1, 1))

    def test_date_parser_accepts_iso_and_rejects_invalid_date(self):
        self.assertEqual(parse_expense_date("2026-03-05"), date(2026, 3, 5))
        for invalid_date in ("2026-02-30", "20260305", "2026-W10-4"):
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                    parse_expense_date(invalid_date)


class ExpenseStorageTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "expenses.json"
            original = [
                Expense(
                    Decimal("19.99"),
                    "Food",
                    "Lunch",
                    date(2026, 3, 5),
                )
            ]

            save_expenses(path, original)

            self.assertEqual(load_expenses(path), original)

    def test_missing_file_is_empty_but_corrupt_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.json"
            self.assertEqual(load_expenses(path), [])
            path.write_text("{bad json", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "could not read"):
                load_expenses(path)


class ExpenseCliTests(unittest.TestCase):
    def test_add_list_and_summary_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.json"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    main(
                        [
                            "--data-file",
                            str(path),
                            "add",
                            "--amount",
                            "12.50",
                            "--category",
                            "Food",
                            "--description",
                            "Lunch",
                            "--date",
                            "2026-03-05",
                        ]
                    ),
                    0,
                )
                self.assertEqual(main(["--data-file", str(path), "list"]), 0)
                self.assertEqual(main(["--data-file", str(path), "summary"]), 0)

            result = output.getvalue()
            self.assertIn("Added 12.50", result)
            self.assertIn("2026-03-05 | 12.50 | Food | Lunch", result)
            self.assertIn("Total: 12.50", result)
            self.assertIn("Food: 12.50", result)


if __name__ == "__main__":
    unittest.main()
