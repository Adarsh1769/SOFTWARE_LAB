/**
 * Concise, manually written implementation of the same task.
 */
public final class ManualCandidate {
    private ManualCandidate() {
    }

    public static String getGrade(double score) {
        if (!Double.isFinite(score) || score < 0 || score > 100) {
            throw new IllegalArgumentException("score must be between 0 and 100");
        }
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
