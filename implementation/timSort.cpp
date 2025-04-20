#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// returns a number equal to or slighly less than a power of 2 between 32 and 64
int calculateMinRun(int n) {
    int r = 0;
    while (n >= 32) {
        r |= n & 1; // record if a bit will be shifted off
        n >>= 1;    // divide n by 2
    }
    return n + r;
}

// augmented to also detect for descending runs and reverse them in place 
void insertionSort(vector<int>& arr, int left, int right) {
    // check for descending run if the first two elements are out of order
    if (left < right && arr[left] > arr[left + 1]) {
        bool isDesc = true;
        for (int k = left; k < right; k++) {
            if (arr[k] < arr[k + 1]) { // found an ascending pair so run is not descending
                isDesc = false;
                break;
            }
        }
        if (isDesc) {
            // reverse in-place
            int i = left, j = right;
            while (i < j) {
                swap(arr[i], arr[j]);
                i++;
                j--;
            }
            return; // sorted run
        }
    }
    // if run is not descending, use standard insertionsort implementation
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

int gallop(int x, const vector<int>& arr, int start) {
    int hi = 1;
    int n = arr.size();
    // multilpy hi by 2 until its idx is >= x, the current element in the "winning" or greater list,
    // or the end of the list is reached
    while (start + hi < n && x > arr[start + hi]) {
        hi *= 2;
    }
    // binary search between the second to last element checked and the element selected to pinpoint where x belongs
    int lo = hi / 2;
    hi = min(start + hi, n);
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (x > arr[mid]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo; // x's sorted position
}
// combine two sorted subarrays [left,mid] and [mid+1,right]
// track consecutive wins to trigger galloping mode to reduce the number of individual comparisons.
void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> leftPart(arr.begin() + left, arr.begin() + mid + 1);
    vector<int> rightPart(arr.begin() + mid + 1, arr.begin() + right + 1);

    int i = 0, j = 0, k = left;
    int minGallop = 7;
    int countLeft = 0, countRight = 0;

    while (i < leftPart.size() && j < rightPart.size()) {
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
        // if one side wins individual comparisons repeatedly, trigger galloping mode
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

    while (i < leftPart.size()) {
        arr[k] = leftPart[i];
        i++;
        k++;
    }

    while (j < rightPart.size()) {
        arr[k] = rightPart[j];
        j++;
        k++;
    }
}

void mergeCollapse(vector<int>& arr, vector<pair<int, int>>& runStack);

// merge top two runs on the stack
void mergeAt(vector<int>& arr, vector<pair<int, int>>& runStack, int i) {
    pair<int, int> run1 = runStack[i];
    pair<int, int> run2 = runStack[i + 1];
    merge(arr, run1.first, run1.second, run2.second);
    runStack[i] = make_pair(run1.first, run2.second);
    runStack.erase(runStack.begin() + i + 1);
}
// enforces timsort's merge policy
void mergeCollapse(vector<int>& arr, vector<pair<int, int>>& runStack) {
    while (runStack.size() > 2) {
        // get the length of the first three runs on the stack
        // C is at the top of the stack, A is closest to the bottom.
        pair<int, int> A = runStack[runStack.size() - 3];
        pair<int, int> B = runStack[runStack.size() - 2];
        pair<int, int> C = runStack[runStack.size() - 1];
        int lenA = A.second - A.first + 1;
        int lenB = B.second - B.first + 1;
        int lenC = C.second - C.first + 1;

        // per merge policy: 
        // A should be larger than B + C
        // B should be larger than C
        if (lenA <= lenB + lenC || lenB <= lenC) {
            if (lenA < lenC) {
                mergeAt(arr, runStack, runStack.size() - 3);
            } 
            else {
                mergeAt(arr, runStack, runStack.size() - 2);
            }
        } else {
            // merge policy holds, no merges necessary
            break;
        }
    }

    if (runStack.size() == 2 && (runStack[runStack.size() - 2].second - runStack[runStack.size() - 2].first + 1) <= (runStack[runStack.size() - 1].second - runStack[runStack.size() - 1].first + 1)) {
        mergeAt(arr, runStack, runStack.size() - 2);
    }
}
// split the array into runs, sort each, then merge according to policy
void timsort(vector<int>& arr) {
    int n = arr.size();
    int minRun = calculateMinRun(n);
    vector<pair<int, int>> runStack;

    int i = 0;
    while (i < n) {
        int runEnd = min(i + minRun - 1, n - 1);
        insertionSort(arr, i, runEnd);
        runStack.push_back(make_pair(i, runEnd));
        i = runEnd + 1;
        mergeCollapse(arr, runStack);
    }
    // merge the runs on the stack according to the merge policy until there is 1 run on the stack
    while (runStack.size() > 1) {
        mergeAt(arr, runStack, runStack.size() - 2);
    }
}

int main() {
    // read from stdin
    int arrSize;
    cin >> arrSize;
    vector<int> arr(arrSize);
    for (int i = 0; i < arrSize; i++) {
        cin >> arr[i];
    }

    timsort(arr);

    // output to stdout
    for (int i = 0; i < arrSize-1; i++) {
        cout << arr[i] << " ";
    }
    cout << arr[arrSize-1] << endl;

    return 0;
}
