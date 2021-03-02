import sys

from sorting import quick_sort, merge_sort, bubble_sort
from edit_distance import minimum_edit_distance
from utils import (
    plot_xs_vs_ys,
    gen_sort_method_data_points,
    gen_random_integers_with_seed,
)


def main(argv):
    # def generator(n):
    #     return gen_random_integers_with_seed(n, 10)

    # bubble_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, bubble_sort, "bubble_sort", generator
    # )
    # quick_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, quick_sort, "quick_sort", generator
    # )
    # merge_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, merge_sort, "merge_sort", generator
    # )
    # py_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, lambda l: l.sort(), "py_sort", generator
    # )

    # plot_xs_vs_ys(
    #     [
    #         bubble_sort_plot_data,
    #         merge_sort_plot_data,
    #         quick_sort_plot_data,
    #         py_sort_plot_data,
    #     ],
    #     "TIME",
    #     "N",
    # )

    print(minimum_edit_distance("ABC", "DEF"))


if __name__ == "__main__":
    main(sys.argv[1:])
