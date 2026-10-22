"""Tests verifying safe calculator behavior after the static-analysis fix."""

import unittest

from fixed_app import calculate


class SafeCalculatorTests(unittest.TestCase):
    def test_evaluates_supported_arithmetic(self) -> None:
        self.assertEqual(14, calculate("2 + 3 * 4"))
        self.assertEqual(-2.5, calculate("-(8 + 2) / 4"))

    def test_rejects_code_execution_syntax_without_evaluating_it(self) -> None:
        with self.assertRaises(ValueError):
            calculate("__import__('os').system('echo unsafe')")

    def test_rejects_unsupported_operators_and_names(self) -> None:
        with self.assertRaises(ValueError):
            calculate("2 ** 10")
        with self.assertRaises(ValueError):
            calculate("secret + 1")

    def test_rejects_oversized_expressions_and_results(self) -> None:
        with self.assertRaises(ValueError):
            calculate("1" * 201)
        with self.assertRaises(ValueError):
            calculate("9" * 200)
        with self.assertRaises(ValueError):
            calculate("1000000000000 * 2")

    def test_reports_division_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            calculate("1 / 0")

    def test_rejects_non_string_input(self) -> None:
        with self.assertRaises(TypeError):
            calculate(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)
