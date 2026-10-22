/**
 * Result of checking whether a number is prime, including work performed.
 */
public final class CheckResult {
    private final boolean prime;
    private final long divisorChecks;

    public CheckResult(boolean prime, long divisorChecks) {
        this.prime = prime;
        this.divisorChecks = divisorChecks;
    }

    public boolean isPrime() {
        return prime;
    }

    public long getDivisorChecks() {
        return divisorChecks;
    }
}
