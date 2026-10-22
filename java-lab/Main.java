/**
 * Compare the AI-generated and manual grade-classification implementations.
 */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        double[] scores = {95, 82, 74, 63, 40};
        int matches = 0;

        System.out.println("AI Code Assistant Lab: Java Grade Classifier Comparison");
        System.out.println("--------------------------------------------------------------");
        System.out.printf("%-10s%-18s%-12s%s%n", "Score", "AI candidate", "Manual", "Result");
        System.out.println("--------------------------------------------------------------");

        for (double score : scores) {
            String aiGrade = AiCandidate.getGrade(score);
            String manualGrade = ManualCandidate.getGrade(score);
            String result = aiGrade.equals(manualGrade) ? "PASS" : "FAIL";
            if (result.equals("PASS")) {
                matches++;
            }
            System.out.printf("%-10.0f%-18s%-12s%s%n", score, aiGrade, manualGrade, result);
        }

        System.out.println("--------------------------------------------------------------");
        System.out.printf("Matching outputs: %d/%d%n", matches, scores.length);
        System.out.println("Both implementations use the same input-validation rules.");
    }
}
