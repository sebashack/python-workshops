def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, i, j)


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


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
