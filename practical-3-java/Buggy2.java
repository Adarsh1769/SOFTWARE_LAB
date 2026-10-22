/**
 * Bug 2: the comparison operator is reversed for a passing score.
 */
public final class Buggy2 {
    private static final int PASS_MARK = 40;

    private Buggy2() {
    }

    static String resultFor(int score) {
        if (score <= PASS_MARK) {
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
