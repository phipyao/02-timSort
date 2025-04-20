package implementation;

import java.util.*;

public class timSort {

    public static int calculateMinRun(int n) {
        int r = 0;
        while (n >= 32) {
            r |= n & 1;
            n >>= 1;
        }
        return n + r;
    }

    public static void insertionSort(int[] arr, int left, int right) {
        if (left < right && arr[left] > arr[left + 1]) {
            boolean isDesc = true;
            for (int k = left; k < right; k++) {
                if (arr[k] < arr[k + 1]) {
                    isDesc = false;
                    break;
                }
            }
            if (isDesc) {
                int i = left, j = right;
                while (i < j) {
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                    i++;
                    j--;
                }
                return;
            }
        }

        for (int i = left + 1; i <= right; i++) {
            int temp = arr[i];
            int j = i - 1;
            while (j >= left && arr[j] > temp) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = temp;
        }
    }

    public static int gallop(int x, int[] arr, int start) {
        int hi = 1;
        int n = arr.length;
        while (start + hi < n && x > arr[start + hi]) {
            hi *= 2;
        }
        int lo = hi / 2;
        hi = Math.min(start + hi, n);
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (x > arr[mid]) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    public static void merge(int[] arr, int left, int mid, int right) {
        int[] leftPart = Arrays.copyOfRange(arr, left, mid + 1);
        int[] rightPart = Arrays.copyOfRange(arr, mid + 1, right + 1);

        int i = 0, j = 0, k = left;
        int minGallop = 7;
        int countLeft = 0, countRight = 0;

        while (i < leftPart.length && j < rightPart.length) {
            if (leftPart[i] <= rightPart[j]) {
                arr[k] = leftPart[i];
                i++;
                countLeft++;
                countRight = 0;
            } else {
                arr[k] = rightPart[j];
                j++;
                countRight++;
                countLeft = 0;
            }
            k++;

            if (countLeft >= minGallop) {
                int pos = gallop(rightPart[j], leftPart, i);
                while (i < pos) {
                    arr[k] = leftPart[i];
                    i++;
                    k++;
                }
                countLeft = 0;
            } else if (countRight >= minGallop) {
                int pos = gallop(leftPart[i], rightPart, j);
                while (j < pos) {
                    arr[k] = rightPart[j];
                    j++;
                    k++;
                }
                countRight = 0;
            }
        }

        while (i < leftPart.length) {
            arr[k] = leftPart[i];
            i++;
            k++;
        }

        while (j < rightPart.length) {
            arr[k] = rightPart[j];
            j++;
            k++;
        }
    }

    public static void timsort(int[] arr) {
        int n = arr.length;
        int minRun = calculateMinRun(n);
        List<int[]> runStack = new ArrayList<>();

        int i = 0;
        while (i < n) {
            int runEnd = Math.min(i + minRun - 1, n - 1);
            insertionSort(arr, i, runEnd);
            runStack.add(new int[]{i, runEnd});
            i = runEnd + 1;
            mergeCollapse(arr, runStack);
        }

        while (runStack.size() > 1) {
            mergeAt(arr, runStack, runStack.size() - 2);
        }
    }

    public static void mergeCollapse(int[] arr, List<int[]> runStack) {
        while (runStack.size() > 2) {
            int[] A = runStack.get(runStack.size() - 3);
            int[] B = runStack.get(runStack.size() - 2);
            int[] C = runStack.get(runStack.size() - 1);
            int lenA = A[1] - A[0] + 1;
            int lenB = B[1] - B[0] + 1;
            int lenC = C[1] - C[0] + 1;

            if (lenA <= lenB + lenC || lenB <= lenC) {
                if (lenA < lenC) {
                    mergeAt(arr, runStack, runStack.size() - 3);
                } else {
                    mergeAt(arr, runStack, runStack.size() - 2);
                }
            } else {
                break;
            }
        }

        if (runStack.size() == 2 && (runStack.get(runStack.size() - 2)[1] - runStack.get(runStack.size() - 2)[0] + 1) <= (runStack.get(runStack.size() - 1)[1] - runStack.get(runStack.size() - 1)[0] + 1)) {
            mergeAt(arr, runStack, runStack.size() - 2);
        }
    }

    public static void mergeAt(int[] arr, List<int[]> runStack, int i) {
        int[] run1 = runStack.get(i);
        int[] run2 = runStack.get(i + 1);
        merge(arr, run1[0], run1[1], run2[1]);
        runStack.set(i, new int[]{run1[0], run2[1]});
        runStack.remove(i + 1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int arrSize = sc.nextInt();
        int[] arr = new int[arrSize];
        for (int i = 0; i < arrSize; i++) {
            arr[i] = sc.nextInt();
        }
        sc.close();

        timsort(arr);

        for (int i = 0; i < arr.length-1; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println(arr[arr.length-1]);
    }
}

