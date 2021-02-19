import unittest

from simulator import (
    gen_vehicle_day_samples,
    read_csv_data,
)
from utils import mk_csv_file_path


class TestSimulator(unittest.TestCase):
    def test_no_duplicated_drivers_in_same_day_for_gen_vehicle_day_samples(self):
        vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
        names_csv_path = mk_csv_file_path("person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055

        # Run simulation for 10 days, a max number of 10 vehicles per day
        # and a max number of 10 stops per vehicle per day.
        # This creates locations approximately in "El area Metropolitana".
        # Medellin's center is located approximately at
        # (lat = 6.251404, lon = -75.575261)
        samples = gen_vehicle_day_samples(10, 10, 10, medellin_center, rad, csv_data)

        for vehicle_days in samples:
            drivers = list(map(lambda vd: vd.driver, vehicle_days))
            self.assertTrue(no_duplicates_check(drivers))


# Helpers
def no_duplicates_check(ls):
    return len(ls) == len(set(ls))
