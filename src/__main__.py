import sys

from sorting import quick_sort, merge_sort, bubble_sort
from utils import (
    plot_xs_vs_ys,
    gen_sort_method_data_points,
)


def main(argv):
    bubble_sort_plot_data = gen_sort_method_data_points(
        1000, 20, bubble_sort, "bubble_sort", 10
    )
    quick_sort_plot_data = gen_sort_method_data_points(
        1000, 20, quick_sort, "quick_sort", 10
    )
    merge_sort_plot_data = gen_sort_method_data_points(
        1000, 20, merge_sort, "merge_sort", 10
    )
    py_sort_plot_data = gen_sort_method_data_points(
        1000, 20, lambda l: l.sort(), "py_sort", 10
    )

    plot_xs_vs_ys(
        [
            bubble_sort_plot_data,
            merge_sort_plot_data,
            quick_sort_plot_data,
            py_sort_plot_data,
        ],
        "TIME",
        "N",
    )


if __name__ == "__main__":
    main(sys.argv[1:])
