/**
 * Dependency-free verification of both buggy examples and their fixes.
 */
public final class Practical3Test {
    private static int checks;

    private Practical3Test() {
    }

    public static void main(String[] args) {
        verifyBugOneAndFix();
        verifyBugTwoAndFix();
        System.out.printf("Passed %d debugging checks.%n", checks);
    }

    private static void verifyBugOneAndFix() {
        boolean threwExpectedException = false;
        try {
            Buggy.sum(new int[]{1, 2, 3, 4, 5});
        } catch (ArrayIndexOutOfBoundsException exception) {
            threwExpectedException = true;
        }
        assertEquals(true, threwExpectedException, "buggy array access");
        assertEquals(15, Fixed.sum(new int[]{1, 2, 3, 4, 5}), "fixed array sum");
        assertEquals(0, Fixed.sum(new int[]{}), "empty array sum");
    }

    private static void verifyBugTwoAndFix() {
        assertEquals("FAIL", Buggy2.resultFor(75), "buggy operator reproduces wrong result");
        assertEquals("PASS", Fixed2.resultFor(75), "score above pass mark");
        assertEquals("PASS", Fixed2.resultFor(40), "score at pass mark");
        assertEquals("FAIL", Fixed2.resultFor(39), "score below pass mark");
    }

    private static void assertEquals(int expected, int actual, String label) {
        if (expected != actual) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
        checks++;
    }

    private static void assertEquals(boolean expected, boolean actual, String label) {
        if (expected != actual) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
        checks++;
    }

    private static void assertEquals(String expected, String actual, String label) {
        if (!expected.equals(actual)) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
        checks++;
    }
}
