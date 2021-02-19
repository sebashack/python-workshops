import sys

from simulator import gen_vehicle_day_samples, flatten_vehicle_day_samples
from sorting import quick_sort, merge_sort, bubble_sort
from csv_utils import write_vehicle_days, mk_csv_file_path, read_csv_data
from utils import (
    plot_xs_vs_ys,
    gen_sort_method_data_points,
)


def main(argv):
    vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
    names_csv_path = mk_csv_file_path("person_list.csv")
    csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
    medellin_center = (6.251404, -75.575261)
    rad = 0.055

    sample = gen_vehicle_day_samples(30, 15, 15, medellin_center, rad, csv_data)
    sample_flattened = flatten_vehicle_day_samples(sample)

    csv_path = mk_csv_file_path("entries.csv")
    write_vehicle_days(csv_path, sample_flattened)
    # bubble_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, bubble_sort, "bubble_sort", 10
    # )
    # quick_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, quick_sort, "quick_sort", 10
    # )
    # merge_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, merge_sort, "merge_sort", 10
    # )
    # py_sort_plot_data = gen_sort_method_data_points(
    #     1000, 20, lambda l: l.sort(), "py_sort", 10
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


if __name__ == "__main__":
    main(sys.argv[1:])
