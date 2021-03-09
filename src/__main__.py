import sys

from queens import make_board, solve_queens
from http_utils import create_http_connection, create_https_connection
from scraping import scrape_html_doc
from kmp import kmp_search
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

    # print(minimum_edit_distance("kitten", "saturday"))

    # conn = create_https_connection("www.eafit.edu.co")
    # conn.request("GET", "/")
    # res = conn.getresponse()
    # html_doc = res.read()

    # scrape_html_doc(html_doc)
    # print(kmp_search("A", "AABB"))
    board = make_board(4)

    print(solve_queens(board))
    print(board)


if __name__ == "__main__":
    main(sys.argv[1:])
