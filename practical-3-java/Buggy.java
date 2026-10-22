/**
 * Bug 1: the loop uses <= and reads one position beyond the array.
 */
public final class Buggy {
    private Buggy() {
    }

    static int sum(int[] values) {
        int total = 0;
        for (int index = 0; index <= values.length; index++) {
            total += values[index];
        }
        return total;
    }

    public static void main(String[] args) {
        int[] values = {1, 2, 3, 4, 5};
        System.out.println("Sum: " + sum(values));
    }
}
