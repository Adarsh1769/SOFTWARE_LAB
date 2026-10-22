/**
 * Baseline prime checker that tests every possible divisor.
 */
public final class BasicPrimeChecker {
    private BasicPrimeChecker() {
    }

    public static CheckResult check(int number) {
        if (number < 2) {
            return new CheckResult(false, 0);
        }

        long divisorChecks = 0;
        for (int divisor = 2; divisor < number; divisor++) {
            divisorChecks++;
            if (number % divisor == 0) {
                return new CheckResult(false, divisorChecks);
            }
        }
        return new CheckResult(true, divisorChecks);
    }
}
