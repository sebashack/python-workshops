def kmp_search(pattern, text):
    n = len(text)
    m = len(pattern)
    lps = [0] * m

    compute_lps(pattern, m, lps)

    i = 0
    j = 0

    result = []

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]

    return result


def compute_lps(pattern, m, lps):
    length = 0
    i = 1
    lps[0] = 0

    while i < m:
        if pattern[i] == pattern[length]:
            lps[i] = length + 1
            length += 1
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
