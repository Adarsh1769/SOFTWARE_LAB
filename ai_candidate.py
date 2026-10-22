"""AI-generated candidate implementation for the grade-classification task."""

from typing import Union

Score = Union[int, float]


def validate_score(score: Score) -> None:
    """Raise a clear exception when a score is not between 0 and 100."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("score must be a number")
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")


def get_grade(score: Score) -> str:
    """Return the letter grade for a numeric score from 0 through 100."""
    validate_score(score)

    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
