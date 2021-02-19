import sys
import os
import time

from simulator import (
    gen_day_samples_as_dict,
    gen_vehicle_day_samples,
    gen_vehicle_day_samples_flattened,
    read_csv_data,
)

from sorting import quick_sort, merge_sort, bubble_sort
from utils import (
    gen_random_integers_with_seed,
    exec_time,
    is_asc_ordered,
    plot_xs_vs_ys,
    gen_sort_method_data_points,
)


def main(argv):
    vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
    names_csv_path = mk_csv_file_path("person_list.csv")
    csv_data = read_csv_data(vehicle_csv_path, names_csv_path)

    # Run simulation for 30 days, a max number of 1000 vehicles per day
    # and a max number of 40 stops per vehicle per day.
    # This creates locations approximately in "El area Metropolitana".
    # Medellin's center is located approximately at
    # (lat = 6.251404, lon = -75.575261)
    medellin_center = (6.251404, -75.575261)
    rad = 0.055

    start = time.time()
    samples = gen_day_samples_as_dict(2, 2, 3, medellin_center, rad, csv_data)
    end = time.time()

    diff = end - start

    print(f"End of simulation. {diff} sec(s) elapsed ...")
    print(f"{samples}")

    # bubble_sort_plot_data = gen_sort_method_data_points(
    #     4000, 200, bubble_sort, "bubble_sort", 10
    # )
    # quick_sort_plot_data = gen_sort_method_data_points(
    #     10000, 500, quick_sort, "quick_sort", 10
    # )
    # merge_sort_plot_data = gen_sort_method_data_points(
    #     10000, 500, merge_sort, "merge_sort", 10
    # )
    # py_sort_plot_data = gen_sort_method_data_points(
    #     10000, 500, lambda l: l.sort(), "py_sort", 10
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
    print("hello")


def mk_csv_file_path(path):
    return str(os.path.join(os.getcwd(), path))


if __name__ == "__main__":
    main(sys.argv[1:])
