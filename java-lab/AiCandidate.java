/**
 * AI-generated candidate implementation for the grade-classification task.
 */
public final class AiCandidate {
    private AiCandidate() {
    }

    private static void validateScore(double score) {
        if (!Double.isFinite(score) || score < 0 || score > 100) {
            throw new IllegalArgumentException("score must be between 0 and 100");
        }
    }

    public static String getGrade(double score) {
        validateScore(score);

        if (score >= 90) {
            return "A";
        }
        if (score >= 80) {
            return "B";
        }
        if (score >= 70) {
            return "C";
        }
        if (score >= 60) {
            return "D";
        }
        return "F";
    }
}
