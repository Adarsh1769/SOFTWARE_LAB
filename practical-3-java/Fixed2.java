/**
 * Fix for Bug 2: a score at or above the pass mark passes.
 */
public final class Fixed2 {
    private static final int PASS_MARK = 40;

    private Fixed2() {
    }

    static String resultFor(int score) {
        if (score >= PASS_MARK) {
            return "PASS";
        }
        return "FAIL";
    }

    public static void main(String[] args) {
        int score = 75;
        System.out.println("Score: " + score);
        System.out.println("Expected result: PASS");
        System.out.println("Actual result: " + resultFor(score));
    }
}
