import sys
import os

from simulator import read_csv_data, gen_day_samples


def main(argv):
    vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
    names_csv_path = mk_csv_file_path("person_list.csv")
    csv_data = read_csv_data(vehicle_csv_path, names_csv_path)

    # Run simulation for 30 days, a max number of 200 vehicles per day
    # and a max number of 20 stops per vehicle per day.
    # This creates locations approximately in "El area Metropolitana".
    # Medellin's center is located approximately at
    # (lat = 6.251404, lon = -75.575261)
    medellin_center = (6.251404, -75.575261)
    rad = 0.055
    sim_data = gen_day_samples(30, 120, 30, medellin_center, rad, csv_data)

    for day in sim_data:
        print(day)
        print("\n")


def mk_csv_file_path(path):
    return str(os.path.join(os.getcwd(), path))


if __name__ == "__main__":
    main(sys.argv[1:])
