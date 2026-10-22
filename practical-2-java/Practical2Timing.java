import java.util.Arrays;

/**
 * Measure warmed-up prime-checking algorithms using repeated batches.
 */
public final class Practical2Timing {
    private static final int NUMBER = 1_000_033;
    private static final int WARMUP_ROUNDS = 3;
    private static final int MEASUREMENT_ROUNDS = 7;
    private static final int ITERATIONS_PER_ROUND = 5;
    private static volatile long resultSink;

    private Practical2Timing() {
    }

    public static void main(String[] args) {
        CheckFunction basic = BasicPrimeChecker::check;
        CheckFunction optimized = OptimizedPrimeChecker::check;

        for (int round = 0; round < WARMUP_ROUNDS; round++) {
            runBatch(basic);
            runBatch(optimized);
        }

        long[] basicTimes = new long[MEASUREMENT_ROUNDS];
        long[] optimizedTimes = new long[MEASUREMENT_ROUNDS];

        for (int round = 0; round < MEASUREMENT_ROUNDS; round++) {
            if (round % 2 == 0) {
                basicTimes[round] = measureBatch(basic);
                optimizedTimes[round] = measureBatch(optimized);
            } else {
                optimizedTimes[round] = measureBatch(optimized);
                basicTimes[round] = measureBatch(basic);
            }
        }

        long basicMedian = median(basicTimes);
        long optimizedMedian = median(optimizedTimes);
        double speedup = (double) basicMedian / optimizedMedian;

        System.out.println("Java execution-time comparison (median of warmed-up batches)");
        System.out.printf("Input: %,d (prime); %d calls per measurement batch%n",
                NUMBER, ITERATIONS_PER_ROUND);
        System.out.printf("Basic checker median:     %.3f ms/call%n", toMilliseconds(basicMedian));
        System.out.printf("Optimized checker median: %.3f ms/call%n", toMilliseconds(optimizedMedian));
        System.out.printf("Measured speedup: %.2fx%n", speedup);
        System.out.println("Timing is machine- and load-dependent; divisor counts are deterministic.");
        if (resultSink == Long.MIN_VALUE) {
            System.out.println("Result sink: " + resultSink);
        }
    }

    private static long measureBatch(CheckFunction checker) {
        long start = System.nanoTime();
        runBatch(checker);
        return (System.nanoTime() - start) / ITERATIONS_PER_ROUND;
    }

    private static void runBatch(CheckFunction checker) {
        long checksum = 0;
        for (int iteration = 0; iteration < ITERATIONS_PER_ROUND; iteration++) {
            CheckResult result = checker.check(NUMBER);
            if (!result.isPrime()) {
                throw new IllegalStateException("Expected " + NUMBER + " to be prime");
            }
            checksum += result.getDivisorChecks();
        }
        resultSink += checksum;
    }

    private static long median(long[] samples) {
        long[] sorted = samples.clone();
        Arrays.sort(sorted);
        return sorted[sorted.length / 2];
    }

    private static double toMilliseconds(long nanoseconds) {
        return nanoseconds / 1_000_000.0;
    }

    @FunctionalInterface
    private interface CheckFunction {
        CheckResult check(int number);
    }
}
