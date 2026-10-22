/**
 * Dependency-free checks for grade boundaries and invalid inputs.
 */
public final class GradeClassifierTest {
    private static int checks;

    private GradeClassifierTest() {
    }

    public static void main(String[] args) {
        checkGrades();
        checkInvalidInputs();
        System.out.printf("Passed %d Java checks.%n", checks);
    }

    private static void checkGrades() {
        double[] scores = {0, 59, 60, 69, 70, 79, 80, 89, 90, 100};
        String[] expected = {"F", "F", "D", "D", "C", "C", "B", "B", "A", "A"};

        for (int i = 0; i < scores.length; i++) {
            String aiGrade = AiCandidate.getGrade(scores[i]);
            String manualGrade = ManualCandidate.getGrade(scores[i]);
            if (!expected[i].equals(aiGrade) || !expected[i].equals(manualGrade)) {
                throw new AssertionError("Unexpected grade for score " + scores[i]);
            }
            checks++;
        }
    }

    private static void checkInvalidInputs() {
        double[] invalidScores = {-1, 101, Double.NaN, Double.POSITIVE_INFINITY};

        for (double score : invalidScores) {
            expectIllegalArgument(() -> AiCandidate.getGrade(score));
            expectIllegalArgument(() -> ManualCandidate.getGrade(score));
        }
    }

    private static void expectIllegalArgument(Runnable action) {
        try {
            action.run();
        } catch (IllegalArgumentException exception) {
            checks++;
            return;
        }
        throw new AssertionError("Expected IllegalArgumentException");
    }
}
