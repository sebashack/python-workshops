import numpy as np


def minimum_edit_distance(source, target):

    s = "#" + source
    t = "#" + target

    solution = np.zeros((len(s), len(t)))

    solution[0] = [j for j in range(len(t))]
    solution[:, 0] = [j for j in range(len(s))]

    for r in range(1, len(s)):
        for c in range(1, len(t)):
            if t[c] != s[r]:
                solution[r, c] = min(solution[r - 1, c], solution[r, c - 1]) + 1
            else:
                solution[r, c] = solution[r - 1, c - 1]

    return solution[len(s) - 1, len(t) - 1]
