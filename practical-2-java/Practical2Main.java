/**
 * Compare baseline and optimized prime checkers by result and divisor checks.
 */
public final class Practical2Main {
    private Practical2Main() {
    }

    public static void main(String[] args) {
        int[] numbers = {97, 100, 1_000_003, 1_000_005, 1_000_033};
        long basicTotal = 0;
        long optimizedTotal = 0;
        boolean allMatch = true;

        System.out.println("AI-Assisted Code Writing and Optimization (Java)");
        System.out.println("--------------------------------------------------------------");
        System.out.printf("%-12s%-12s%-14s%-18s%s%n",
                "Number", "Prime?", "Basic checks", "Optimized checks", "Result");
        System.out.println("--------------------------------------------------------------");

        for (int number : numbers) {
            CheckResult basic = BasicPrimeChecker.check(number);
            CheckResult optimized = OptimizedPrimeChecker.check(number);
            boolean matches = basic.isPrime() == optimized.isPrime();
            allMatch &= matches;
            basicTotal += basic.getDivisorChecks();
            optimizedTotal += optimized.getDivisorChecks();

            System.out.printf("%-12d%-12s%-14d%-18d%s%n",
                    number,
                    optimized.isPrime() ? "Yes" : "No",
                    basic.getDivisorChecks(),
                    optimized.getDivisorChecks(),
                    matches ? "PASS" : "FAIL");
        }

        double reduction = basicTotal == 0
                ? 0
                : (1.0 - (double) optimizedTotal / basicTotal) * 100;
        System.out.println("--------------------------------------------------------------");
        System.out.printf("Results match: %s%n", allMatch ? "YES" : "NO");
        System.out.printf("Total divisor checks: basic=%d, optimized=%d%n",
                basicTotal, optimizedTotal);
        System.out.printf("Divisor-check reduction: %.2f%%%n", reduction);
        System.out.println("Efficiency is measured by divisor checks, not elapsed time.");
    }
}
