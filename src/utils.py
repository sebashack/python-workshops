import matplotlib.pyplot as plt
import random as rnd
import time


# Plotting
def plot_xs_vs_ys(data, x_label, y_label):
    for (xs, ys, label) in data:
        plt.plot(xs, ys)
        plt.annotate(label, xy=(xs[-1], ys[-1]))

    plt.ylabel(x_label)
    plt.xlabel(y_label)
    plt.show()


def gen_sort_method_data_points(upper, step, sort_method, label, seed):
    assert upper > step

    xs = []
    ys = []

    for n in range(0, upper, step):
        ls = gen_random_integers_with_seed(n, seed)
        t = gen_sort_method_data_point(ls, sort_method)
        xs.append(n)
        ys.append(t)

    return (xs, ys, label)


def gen_sort_method_data_point(ls, sort_method):
    start = time.time()
    sort_method(ls)
    end = time.time()
    diff = round(end - start, 5)

    return diff


# Measure time
def exec_time(f):
    start = time.time()
    r = f() or None
    end = time.time()

    return (r, end - start)


# Generators
def gen_random_integers_with_seed(n, seed):
    rnd.seed(seed)

    nums = []
    for _ in range(n):
        nums.append(rnd.randint(1, n))

    return nums


def gen_random_integers(n):
    nums = []
    for _ in range(n):
        nums.append(rnd.randint(1, n))

    return nums


# Predicates
def is_asc_ordered(ls):
    tail = ls[1:]

    for (x, y) in zip(ls, tail):
        if x > y:
            return False

    return True
