import unittest

from ai_candidate import get_grade as ai_get_grade
from manual_candidate import get_grade as manual_get_grade


class GradeComparisonTests(unittest.TestCase):
    def test_both_implementations_match_at_grade_boundaries(self) -> None:
        expected = {
            0: "F",
            59: "F",
            60: "D",
            69: "D",
            70: "C",
            79: "C",
            80: "B",
            89: "B",
            90: "A",
            100: "A",
        }
        for score, grade in expected.items():
            with self.subTest(score=score):
                self.assertEqual(ai_get_grade(score), grade)
                self.assertEqual(manual_get_grade(score), grade)

    def test_both_implementations_reject_invalid_values_consistently(self) -> None:
        invalid_values = (
            (-1, ValueError),
            (101, ValueError),
            ("90", TypeError),
            (True, TypeError),
        )
        for score, error in invalid_values:
            with self.subTest(score=score):
                with self.assertRaises(error):
                    ai_get_grade(score)
                with self.assertRaises(error):
                    manual_get_grade(score)


if __name__ == "__main__":
    unittest.main()
