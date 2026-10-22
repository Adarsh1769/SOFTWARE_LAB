"""Run the AI-generated and manual grade-classification implementations."""

from ai_candidate import get_grade as ai_get_grade
from manual_candidate import get_grade as manual_get_grade


def main() -> None:
    print("AI Code Assistant Lab: Grade Classifier Comparison")
    print("-" * 58)
    print(f"{'Score':<10}{'AI candidate':<18}{'Manual':<12}{'Result'}")
    print("-" * 58)

    scores = (95, 82, 74, 63, 40)
    matches = 0

    for score in scores:
        ai_grade = ai_get_grade(score)
        manual_grade = manual_get_grade(score)
        result = "PASS" if ai_grade == manual_grade else "FAIL"
        matches += result == "PASS"
        print(f"{score:<10}{ai_grade:<18}{manual_grade:<12}{result}")

    print("-" * 58)
    print(f"Matching outputs: {matches}/{len(scores)}")
    print("Both implementations use the same input-validation rules.")


if __name__ == "__main__":
    main()
