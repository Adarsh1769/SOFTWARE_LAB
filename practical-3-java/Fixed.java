/**
 * Fix for Bug 1: stop before the array length.
 */
public final class Fixed {
    private Fixed() {
    }

    static int sum(int[] values) {
        int total = 0;
        for (int index = 0; index < values.length; index++) {
            total += values[index];
        }
        return total;
    }

    public static void main(String[] args) {
        int[] values = {1, 2, 3, 4, 5};
        System.out.println("Sum: " + sum(values));
    }
}
