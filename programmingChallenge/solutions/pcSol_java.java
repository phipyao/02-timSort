import java.util.*;

public class pcSol_java {

    static int calculateMinRun(int n) {
        int r = 0;
        while (n >= 32) {
            r |= n & 1;
            n >>= 1;
        }
        return n + r;
    }

    static void insertionSort(List<Ship> arr, int left, int right, Comparator<Ship> key) {
        if (left < right && key.compare(arr.get(left), arr.get(left + 1)) > 0) {
            boolean isDesc = true;
            for (int k = left; k < right; k++) {
                if (key.compare(arr.get(k), arr.get(k + 1)) < 0) {
                    isDesc = false;
                    break;
                }
            }
            if (isDesc) {
                Collections.reverse(arr.subList(left, right + 1));
                return;
            }
        }

        for (int i = left + 1; i <= right; i++) {
            Ship temp = arr.get(i);
            int j = i - 1;
            while (j >= left && key.compare(arr.get(j), temp) > 0) {
                arr.set(j + 1, arr.get(j));
                j--;
            }
            arr.set(j + 1, temp);
        }
    }

    static int gallop(Ship x, List<Ship> arr, int start, Comparator<Ship> key) {
        int hi = 1;
        int n = arr.size();
        while (start + hi < n && key.compare(x, arr.get(start + hi)) > 0) {
            hi *= 2;
        }
        int lo = hi / 2;
        hi = Math.min(start + hi, n);
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (key.compare(x, arr.get(mid)) > 0) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    static void merge(List<Ship> arr, int left, int mid, int right, Comparator<Ship> key) {
        List<Ship> leftPart = new ArrayList<>(arr.subList(left, mid + 1));
        List<Ship> rightPart = new ArrayList<>(arr.subList(mid + 1, right + 1));

        int i = 0, j = 0, k = left;
        int minGallop = 7;
        int countLeft = 0, countRight = 0;

        while (i < leftPart.size() && j < rightPart.size()) {
            if (key.compare(leftPart.get(i), rightPart.get(j)) <= 0) {
                arr.set(k++, leftPart.get(i++));
                countLeft++;
                countRight = 0;
            } else {
                arr.set(k++, rightPart.get(j++));
                countRight++;
                countLeft = 0;
            }

            if (countLeft >= minGallop) {
                int pos = gallop(rightPart.get(j), leftPart, i, key);
                while (i < pos) arr.set(k++, leftPart.get(i++));
                countLeft = 0;
            } else if (countRight >= minGallop) {
                int pos = gallop(leftPart.get(i), rightPart, j, key);
                while (j < pos) arr.set(k++, rightPart.get(j++));
                countRight = 0;
            }
        }

        while (i < leftPart.size()) arr.set(k++, leftPart.get(i++));
        while (j < rightPart.size()) arr.set(k++, rightPart.get(j++));
    }

    static void timsort(List<Ship> arr, Comparator<Ship> key) {
        int n = arr.size();
        int minRun = calculateMinRun(n);
        List<int[]> runStack = new ArrayList<>();

        int i = 0;
        while (i < n) {
            int runEnd = Math.min(i + minRun - 1, n - 1);
            insertionSort(arr, i, runEnd, key);
            runStack.add(new int[]{i, runEnd});
            i = runEnd + 1;
            mergeCollapse(arr, runStack, key);
        }

        while (runStack.size() > 1) {
            mergeAt(arr, runStack, runStack.size() - 2, key);
        }
    }

    static void mergeCollapse(List<Ship> arr, List<int[]> runStack, Comparator<Ship> key) {
        while (runStack.size() > 2) {
            int[] A = runStack.get(runStack.size() - 3);
            int[] B = runStack.get(runStack.size() - 2);
            int[] C = runStack.get(runStack.size() - 1);
            int lenA = A[1] - A[0] + 1;
            int lenB = B[1] - B[0] + 1;
            int lenC = C[1] - C[0] + 1;

            if (lenA <= lenB + lenC || lenB <= lenC) {
                if (lenA < lenC) {
                    mergeAt(arr, runStack, runStack.size() - 3, key);
                } else {
                    mergeAt(arr, runStack, runStack.size() - 2, key);
                }
            } else {
                break;
            }
        }

        if (runStack.size() == 2) {
            int[] A = runStack.get(0);
            int[] B = runStack.get(1);
            if (A[1] - A[0] + 1 <= B[1] - B[0] + 1) {
                mergeAt(arr, runStack, 0, key);
            }
        }
    }

    static void mergeAt(List<Ship> arr, List<int[]> runStack, int i, Comparator<Ship> key) {
        int[] run1 = runStack.get(i);
        int[] run2 = runStack.get(i + 1);
        merge(arr, run1[0], run1[1], run2[1], key);
        run1[1] = run2[1];
        runStack.remove(i + 1);
    }

    static Comparator<Ship> polarAngleComparator = (a, b) -> {
        boolean ha = a.y > 0 || (a.y == 0 && a.x >= 0);
        boolean hb = b.y > 0 || (b.y == 0 && b.x >= 0);

        if (ha != hb) return ha ? -1 : 1;

        long cross = (long) a.x * b.y - (long) a.y * b.x;
        if (cross != 0) return cross > 0 ? -1 : 1;

        if (a.r != b.r) return Double.compare(a.r, b.r);

        return Integer.compare(a.index, b.index);
    };

    static class Ship {
        int x, y, index;
        double r;
        String name;

        Ship(int x, int y, String name, int index) {
            this.x = x;
            this.y = y;
            this.name = name;
            this.index = index;
            this.r = Math.sqrt(x * x + y * y);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numShips = sc.nextInt();
        int numQueries = sc.nextInt();

        Map<Ship, String> shipMap = new HashMap<>();
        List<Ship> shipsSorted = new ArrayList<>();

        for (int i = 0; i < numShips; i++) {
            int x = sc.nextInt();
            int y = sc.nextInt();
            String name = sc.next();
            Ship s = new Ship(x, y, name, i);
            shipsSorted.add(s);
            shipMap.put(s, name);
        }

        timsort(shipsSorted, polarAngleComparator);

        for (int i = 0; i < numQueries; i++) {
            double radius = sc.nextDouble();
            List<String> queried = new ArrayList<>();
            for (Ship s : shipsSorted) {
                if (s.r <= radius) queried.add(s.name);
            }
            if (queried.isEmpty()) System.out.println(-1);
            else System.out.println(String.join(" ", queried));
        }

        sc.close();
    }
}
