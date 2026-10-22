/**
 * Dependency-free checks for prime results and optimization behavior.
 */
public final class Practical2Test {
    private static int checks;

    private Practical2Test() {
    }

    public static void main(String[] args) {
        checkKnownValues();
        checkImplementationsAgree();
        checkOptimizationWork();
        System.out.printf("Passed %d Java checks.%n", checks);
    }

    private static void checkKnownValues() {
        int[] numbers = {-5, 0, 1, 2, 3, 4, 9, 97, 100, 1_000_003};
        boolean[] expected = {false, false, false, true, true, false, false, true, false, true};

        for (int i = 0; i < numbers.length; i++) {
            assertEquals(expected[i], BasicPrimeChecker.check(numbers[i]).isPrime(),
                    "basic checker for " + numbers[i]);
            assertEquals(expected[i], OptimizedPrimeChecker.check(numbers[i]).isPrime(),
                    "optimized checker for " + numbers[i]);
        }
    }

    private static void checkImplementationsAgree() {
        for (int number = -10; number <= 5_000; number++) {
            assertEquals(BasicPrimeChecker.check(number).isPrime(),
                    OptimizedPrimeChecker.check(number).isPrime(),
                    "implementations disagree for " + number);
        }
    }

    private static void checkOptimizationWork() {
        CheckResult basic = BasicPrimeChecker.check(1_000_003);
        CheckResult optimized = OptimizedPrimeChecker.check(1_000_003);
        assertTrue(basic.getDivisorChecks() > optimized.getDivisorChecks(),
                "optimized checker should use fewer divisor checks for a large prime");
    }

    private static void assertEquals(boolean expected, boolean actual, String message) {
        if (expected != actual) {
            throw new AssertionError(message + ": expected " + expected + ", got " + actual);
        }
        checks++;
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
        checks++;
    }
}
