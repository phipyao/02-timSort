package implementations;

import java.util.Arrays;
import java.util.Scanner;

public class timSort {
    static int MIN_RUN = 32;

    public static int calculateMinRun(int n) {
        int r = 0;
        while (n >= MIN_RUN) {
            r |= (n & 1);
            n >>= 1;
        }
        return n + r;
    }

    public static void insertionSort(int[] arr, int left, int right) {
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

    public static void merge(int[] arr, int left, int mid, int right) {
        int[] leftPart = Arrays.copyOfRange(arr, left, mid + 1);
        int[] rightPart = Arrays.copyOfRange(arr, mid + 1, right + 1);

        int i = 0, j = 0, k = left;
        while (i < leftPart.length && j < rightPart.length) {
            if (leftPart[i] <= rightPart[j]) {
                arr[k++] = leftPart[i++];
            } else {
                arr[k++] = rightPart[j++];
            }
        }

        while (i < leftPart.length) arr[k++] = leftPart[i++];
        while (j < rightPart.length) arr[k++] = rightPart[j++];
    }

    public static void TimSort(int[] arr) {
        int n = arr.length;
        int minRun = calculateMinRun(n);

        for (int i = 0; i < n; i += minRun)
            insertionSort(arr, i, Math.min(i + minRun - 1, n - 1));

        for (int size = minRun; size < n; size *= 2) {
            for (int left = 0; left < n; left += 2 * size) {
                int mid = Math.min(n - 1, left + size - 1);
                int right = Math.min(n - 1, left + 2 * size - 1);
                if (mid < right)
                    merge(arr, left, mid, right);
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int arr_size = sc.nextInt();
        int[] arr = new int[arr_size];
        for (int i = 0; i < arr_size; i++) {
            arr[i] = sc.nextInt();
        }
        sc.close();

        TimSort(arr);

        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i]);
            if (i < arr.length - 1) {
                System.out.print(" ");
            }
        }
        System.out.println();
        
    }
}
