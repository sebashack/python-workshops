import sys
import os

from simulator import read_csv_data, gen_day_samples


def main(argv):
    vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
    coord_csv_path = mk_csv_file_path("coord_list.csv")
    names_csv_path = mk_csv_file_path("person_list.csv")

    csv_data = read_csv_data(vehicle_csv_path, coord_csv_path, names_csv_path)
    # Run simulation for 30 days, a max number of 12 vehicles per day
    # and a max number of 8 stops per vehicle per day
    simulation_data = gen_day_samples(30, 11, 11, csv_data)

    for day in simulation_data:
        print(day)
        print("\n")


def mk_csv_file_path(path):
    return str(os.path.join(os.getcwd(), path))


if __name__ == "__main__":
    main(sys.argv[1:])
