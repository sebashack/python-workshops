# Bubble sort
def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, i, j)


# Merge sort
def merge_sort(ls):
    ls_len = len(ls)

    if ls_len > 1:
        m = ls_len // 2

        left_ls = ls[:m]
        right_ls = ls[m:]

        return merge(merge_sort(left_ls), merge_sort(right_ls))
    else:
        return ls


def merge(left_ls, right_ls):
    result = []
    left_len = len(left_ls)
    right_len = len(right_ls)

    i = 0
    j = 0

    while i < left_len and j < right_len:
        if left_ls[i] <= right_ls[j]:
            result.append(left_ls[i])
            i += 1
        else:
            result.append(right_ls[j])
            j += 1

    while i < left_len:
        result.append(left_ls[i])
        i += 1

    while j < right_len:
        result.append(right_ls[j])
        j += 1

    return result


# Quick sort
def quick_sort_by(ls, f):
    if len(ls) <= 1:
        return ls

    pivot = ls[0]
    higher = [x for x in ls[1:] if f(x) > f(pivot)]
    lower = [x for x in ls[1:] if f(x) <= f(pivot)]
    return quick_sort_by(lower, f) + [pivot] + quick_sort_by(higher, f)


def quick_sort(ls):
    if len(ls) <= 1:
        return ls

    pivot = ls[0]
    higher = [i for i in ls[1:] if i > pivot]
    lower = [i for i in ls[1:] if i <= pivot]
    return quick_sort(lower) + [pivot] + quick_sort(higher)


# Helpers
def inc_by_one(i):
    i += 1
    return i


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
