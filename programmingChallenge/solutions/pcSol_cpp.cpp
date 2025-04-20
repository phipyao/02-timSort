#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <map>

using namespace std;

struct Ship {
    int x, y, index;
    double r;
    string name;

    Ship(int x, int y, string name, int index) {
        this->x = x;
        this->y = y;
        this->name = name;
        this->index = index;
        this->r = sqrt(x * x + y * y);
    }
};

// Define a custom comparator for Ship objects
struct ShipComparator {
    bool operator()(const Ship& a, const Ship& b) const {
        // Compare ships by their 'r' values first
        if (a.r != b.r) return a.r < b.r;
        // If 'r' values are equal, compare by 'x'
        if (a.x != b.x) return a.x < b.x;
        // If 'x' values are equal, compare by 'y'
        return a.y < b.y;
    }
};

int calculateMinRun(int n) {
    int r = 0;
    while (n >= 32) {
        r |= n & 1;
        n >>= 1;
    }
    return n + r;
}

int gallop(const Ship& x, vector<Ship>& arr, int start, bool (*key)(const Ship&, const Ship&)) {
    int hi = 1;
    int n = arr.size();
    while (start + hi < n && key(x, arr[start + hi])) {
        hi *= 2;
    }
    int lo = hi / 2;
    hi = min(start + hi, n);
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (key(x, arr[mid])) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

void insertionSort(vector<Ship>& arr, int left, int right, bool (*key)(const Ship&, const Ship&)) {
    if (left < right && key(arr[left + 1], arr[left])) {
        bool isDesc = true;
        for (int k = left; k < right; k++) {
            if (!key(arr[k], arr[k + 1])) {
                isDesc = false;
                break;
            }
        }
        if (isDesc) {
            reverse(arr.begin() + left, arr.begin() + right + 1);
            return;
        }
    }

    for (int i = left + 1; i <= right; i++) {
        Ship temp = arr[i];
        int j = i - 1;
        while (j >= left && key(temp, arr[j])) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = temp;
    }
}

void merge(vector<Ship>& arr, int left, int mid, int right, bool (*key)(const Ship&, const Ship&)) {
    vector<Ship> leftPart(arr.begin() + left, arr.begin() + mid + 1);
    vector<Ship> rightPart(arr.begin() + mid + 1, arr.begin() + right + 1);

    int i = 0, j = 0, k = left;
    int minGallop = 7;
    int countLeft = 0, countRight = 0;

    while (i < leftPart.size() && j < rightPart.size()) {
        if (key(leftPart[i], rightPart[j])) {
            arr[k++] = leftPart[i++];
            countLeft++;
            countRight = 0;
        } else {
            arr[k++] = rightPart[j++];
            countRight++;
            countLeft = 0;
        }

        if (countLeft >= minGallop) {
            int pos = gallop(rightPart[j], leftPart, i, key);
            while (i < pos) arr[k++] = leftPart[i++];
            countLeft = 0;
        } else if (countRight >= minGallop) {
            int pos = gallop(leftPart[i], rightPart, j, key);
            while (j < pos) arr[k++] = rightPart[j++];
            countRight = 0;
        }
    }

    while (i < leftPart.size()) arr[k++] = leftPart[i++];
    while (j < rightPart.size()) arr[k++] = rightPart[j++];
}

void mergeCollapse(vector<Ship>& arr, vector<vector<int>>& runStack, bool (*key)(const Ship&, const Ship&)) {
    while (runStack.size() > 2) {
        vector<int> A = runStack[runStack.size() - 3];
        vector<int> B = runStack[runStack.size() - 2];
        vector<int> C = runStack[runStack.size() - 1];
        int lenA = A[1] - A[0] + 1;
        int lenB = B[1] - B[0] + 1;
        int lenC = C[1] - C[0] + 1;

        if (lenA <= lenB + lenC || lenB <= lenC) {
            if (lenA < lenC) {
                merge(arr, A[0], A[1], C[1], key);
            } else {
                merge(arr, B[0], B[1], C[1], key);
            }
        } else {
            break;
        }
    }

    if (runStack.size() == 2) {
        vector<int> A = runStack[0];
        vector<int> B = runStack[1];
        if (A[1] - A[0] + 1 <= B[1] - B[0] + 1) {
            merge(arr, A[0], A[1], B[1], key);
        }
    }
}

void mergeAt(vector<Ship>& arr, vector<vector<int>>& runStack, int i, bool (*key)(const Ship&, const Ship&)) {
    vector<int> run1 = runStack[i];
    vector<int> run2 = runStack[i + 1];
    merge(arr, run1[0], run1[1], run2[1], key);
    run1[1] = run2[1];
    runStack.erase(runStack.begin() + i + 1);
}

bool polarAngleComparator(const Ship& a, const Ship& b) {
    bool ha = a.y > 0 || (a.y == 0 && a.x >= 0);
    bool hb = b.y > 0 || (b.y == 0 && b.x >= 0);

    if (ha != hb) return ha ? true : false;

    long long cross = (long long) a.x * b.y - (long long) a.y * b.x;
    if (cross != 0) return cross > 0;

    if (a.r != b.r) return a.r < b.r;

    return a.index < b.index;
}

void timsort(vector<Ship>& arr, bool (*key)(const Ship&, const Ship&)) {
    int n = arr.size();
    int minRun = calculateMinRun(n);
    vector<vector<int>> runStack;

    int i = 0;
    while (i < n) {
        int runEnd = min(i + minRun - 1, n - 1);
        insertionSort(arr, i, runEnd, key);
        runStack.push_back({i, runEnd});
        i = runEnd + 1;
        mergeCollapse(arr, runStack, key);
    }

    while (runStack.size() > 1) {
        mergeAt(arr, runStack, runStack.size() - 2, key);
    }
}

int main() {
    int numShips, numQueries;
    cin >> numShips >> numQueries;

    map<Ship, string, ShipComparator> shipMap;
    vector<Ship> shipsSorted;

    for (int i = 0; i < numShips; i++) {
        int x, y;
        string name;
        cin >> x >> y >> name;
        Ship s(x, y, name, i);
        shipsSorted.push_back(s);
        shipMap[s] = name;
    }

    timsort(shipsSorted, polarAngleComparator);

    for (int i = 0; i < numQueries; i++) {
        double radius;
        cin >> radius;
        vector<string> queried;
        for (Ship s : shipsSorted) {
            if (s.r <= radius) queried.push_back(s.name);
        }
        if (queried.empty()) cout << -1 << endl;
        else {
            for (size_t j = 0; j < queried.size(); j++) {
                cout << queried[j];
                if (j < queried.size() - 1) cout << " ";
            }
            cout << endl;
        }
    }

    return 0;
}
