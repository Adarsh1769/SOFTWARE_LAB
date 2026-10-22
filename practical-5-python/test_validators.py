"""AI-generated and manually designed unit tests for validators.py."""

import unittest

from validators import is_valid_age, is_valid_email, is_valid_username


class AIGeneratedValidatorTests(unittest.TestCase):
    """Representative cases suggested by an AI assistant."""

    def test_accepts_well_formed_email(self) -> None:
        self.assertTrue(is_valid_email("student@example.com"))

    def test_rejects_email_without_domain(self) -> None:
        self.assertFalse(is_valid_email("student@"))

    def test_accepts_valid_username(self) -> None:
        self.assertTrue(is_valid_username("lab_user7"))

    def test_rejects_username_with_spaces(self) -> None:
        self.assertFalse(is_valid_username("lab user"))

    def test_accepts_age_inside_range(self) -> None:
        self.assertTrue(is_valid_age(25))

    def test_rejects_age_outside_range(self) -> None:
        self.assertFalse(is_valid_age(121))


class ManualValidatorTests(unittest.TestCase):
    """Additional boundary and malformed-input cases chosen manually."""

    def test_email_rejects_whitespace_and_repeated_dots(self) -> None:
        self.assertFalse(is_valid_email("student name@example.com"))
        self.assertFalse(is_valid_email("student..name@example.com"))

    def test_username_length_boundaries(self) -> None:
        self.assertTrue(is_valid_username("abc"))
        self.assertTrue(is_valid_username("a" * 20))
        self.assertFalse(is_valid_username("ab"))
        self.assertFalse(is_valid_username("a" * 21))

    def test_age_boundaries(self) -> None:
        self.assertTrue(is_valid_age(0))
        self.assertTrue(is_valid_age(120))
        self.assertFalse(is_valid_age(-1))
        self.assertFalse(is_valid_age(121))

    def test_rejects_wrong_types_and_boolean_age(self) -> None:
        self.assertFalse(is_valid_email(None))
        self.assertFalse(is_valid_username(123))
        self.assertFalse(is_valid_age(True))
        self.assertFalse(is_valid_age("25"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
