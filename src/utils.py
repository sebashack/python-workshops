import random as rdn
import time


# Measure time
def exec_time(f):
    start = time.time()
    r = f() or None
    end = time.time()

    return (r, end - start)


# Generators
def gen_random_integers(n):
    nums = []
    for _ in range(n):
        nums.append(rdn.randint(1, n))

    return nums
