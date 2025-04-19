def calculate_min_run(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(arr, left, right):
    if left < right and arr[left] > arr[left+1]:
        is_desc = True
        for k in range(left, right):
            if arr[k] < arr[k+1]:
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
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def gallop(x, arr, start):
    hi = 1
    n = len(arr)
    while start + hi < n and x > arr[start + hi]:
        hi *= 2
    lo = hi // 2
    hi = min(start + hi, n)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > arr[mid]:
            lo = mid + 1
        else:
            hi = mid
    return lo

def merge(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = j = 0
    k = left
    min_gallop = 7
    count_left = count_right = 0

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
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
            pos = gallop(right_part[j], left_part, i)
            while i < pos:
                arr[k] = left_part[i]
                i += 1
                k += 1
            count_left = 0

        elif count_right >= min_gallop:
            pos = gallop(left_part[i], right_part, j)
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

def timsort(arr):
    n = len(arr)
    min_run = calculate_min_run(n)
    run_stack = []

    i = 0
    while i < n:
        run_end = min(i + min_run - 1, n - 1)
        insertion_sort(arr, i, run_end)
        run_stack.append((i, run_end))
        i = run_end + 1
        merge_collapse(arr, run_stack)

    while len(run_stack) > 1:
        merge_at(arr, run_stack, len(run_stack) - 2)

def merge_collapse(arr, run_stack):
    while len(run_stack) > 2:
        A = run_stack[-3]
        B = run_stack[-2]
        C = run_stack[-1]
        lenA = A[1] - A[0] + 1
        lenB = B[1] - B[0] + 1
        lenC = C[1] - C[0] + 1

        if lenA <= lenB + lenC or lenB <= lenC:
            if lenA < lenC:
                merge_at(arr, run_stack, len(run_stack) - 3)
            else:
                merge_at(arr, run_stack, len(run_stack) - 2)
        else:
            break

    if len(run_stack) == 2 and (run_stack[-2][1] - run_stack[-2][0] + 1) <= (run_stack[-1][1] - run_stack[-1][0] + 1):
        merge_at(arr, run_stack, len(run_stack) - 2)

def merge_at(arr, run_stack, i):
    start1, end1 = run_stack[i]
    start2, end2 = run_stack[i + 1]
    merge(arr, start1, end1, end2)
    run_stack[i] = (start1, end2)
    del run_stack[i + 1]

# main:
arr_size = int(input())
arr = [int(input()) for i in range(arr_size)]
timsort(arr)
print(*arr)
