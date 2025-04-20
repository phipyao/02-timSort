from functools import cmp_to_key
import math

def calculate_min_run(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(arr, left, right, key):
    if left < right and key(arr[left]) > key(arr[left+1]):
        is_desc = True
        for k in range(left, right):
            if key(arr[k]) < key(arr[k+1]):
                is_desc = False
                break
        if is_desc:
            i, j = left, right
            while i < j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
            return

    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and key(arr[j]) > key(temp):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def gallop(x, arr, start, key):
    hi = 1
    n = len(arr)
    while start + hi < n and key(x) > key(arr[start + hi]):
        hi *= 2
    lo = hi // 2
    hi = min(start + hi, n)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(x) > key(arr[mid]):
            lo = mid + 1
        else:
            hi = mid
    return lo

def merge(arr, left, mid, right, key):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = j = 0
    k = left
    min_gallop = 7
    count_left = count_right = 0

    while i < len(left_part) and j < len(right_part):
        if key(left_part[i]) <= key(right_part[j]):
            arr[k] = left_part[i]
            i += 1
            count_left += 1
            count_right = 0
        else:
            arr[k] = right_part[j]
            j += 1
            count_right += 1
            count_left = 0
        k += 1

        if count_left >= min_gallop:
            pos = gallop(right_part[j], left_part, i, key)
            while i < pos:
                arr[k] = left_part[i]
                i += 1
                k += 1
            count_left = 0

        elif count_right >= min_gallop:
            pos = gallop(left_part[i], right_part, j, key)
            while j < pos:
                arr[k] = right_part[j]
                j += 1
                k += 1
            count_right = 0

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1

def timsort(arr, key=lambda x: x):
    n = len(arr)
    min_run = calculate_min_run(n)
    run_stack = []

    i = 0
    while i < n:
        run_end = min(i + min_run - 1, n - 1)
        insertion_sort(arr, i, run_end, key)
        run_stack.append((i, run_end))
        i = run_end + 1
        merge_collapse(arr, run_stack, key)

    while len(run_stack) > 1:
        merge_at(arr, run_stack, len(run_stack) - 2, key)

def merge_collapse(arr, run_stack, key):
    while len(run_stack) > 2:
        A = run_stack[-3]
        B = run_stack[-2]
        C = run_stack[-1]
        lenA = A[1] - A[0] + 1
        lenB = B[1] - B[0] + 1
        lenC = C[1] - C[0] + 1

        if lenA <= lenB + lenC or lenB <= lenC:
            if lenA < lenC:
                merge_at(arr, run_stack, len(run_stack) - 3, key)
            else:
                merge_at(arr, run_stack, len(run_stack) - 2, key)
        else:
            break

    if len(run_stack) == 2 and (run_stack[-2][1] - run_stack[-2][0] + 1) <= (run_stack[-1][1] - run_stack[-1][0] + 1):
        merge_at(arr, run_stack, len(run_stack) - 2, key)

def merge_at(arr, run_stack, i, key):
    start1, end1 = run_stack[i]
    start2, end2 = run_stack[i + 1]
    merge(arr, start1, end1, end2, key)
    run_stack[i] = (start1, end2)
    del run_stack[i + 1]


def polar_angle_comparator(a, b):
    ax, ay, ra, ia = a
    bx, by, rb, ib = b

    # Check Above/Below Lighthouse
    def half(x, y):
        return y > 0 or (y == 0 and x >= 0)

    ha = half(ax, ay)
    hb = half(bx, by)

    if ha != hb:
        return -1 if ha else 1

    # Cross product for angle
    cross = ax * by - ay * bx
    if cross != 0:
        return -1 if cross > 0 else 1

    # Sort by radius
    if ra != rb:
        return -1 if ra < rb else 1

    # Sort by order of appearance (i)
    if ia != ib:
        return -1 if ia < ib else 1

    return 0

# calculate radius for every point and append index (x, y) -> (x, y, r, i)
# and make a hashmap with a key of points "(x, y, r, i)" and value of "boatname"
num_ships, num_queries = list(map(int, input().split()))
ships = {}
ships_sorted_by_r = []

for i in range(num_ships):
    x, y, ship_name = input().split()
    x, y = int(x), int(y)
    r = math.sqrt(x**2 + y**2)
    point = (x, y, r, i)
    ships[point] = ship_name
    ships_sorted_by_r.append(point)

# timsort points by polar angle, radius, and index
timsort(ships_sorted_by_r, key=cmp_to_key(polar_angle_comparator))

for q in range(num_queries):
    # query ships under given radius
    radius = float(input())
    ships_queried = [ships[point] for point in ships_sorted_by_r if point[2] <= radius]
    print(*ships_queried if ships_queried else [-1])