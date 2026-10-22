/**
 * AI-optimized candidate using even-number handling and trial division
 * up to the square root of the input.
 */
public final class OptimizedPrimeChecker {
    private OptimizedPrimeChecker() {
    }

    public static CheckResult check(int number) {
        if (number < 2) {
            return new CheckResult(false, 0);
        }
        if (number == 2) {
            return new CheckResult(true, 0);
        }

        long divisorChecks = 1;
        if (number % 2 == 0) {
            return new CheckResult(false, divisorChecks);
        }

        for (int divisor = 3; divisor <= number / divisor; divisor += 2) {
            divisorChecks++;
            if (number % divisor == 0) {
                return new CheckResult(false, divisorChecks);
            }
        }
        return new CheckResult(true, divisorChecks);
    }
}
