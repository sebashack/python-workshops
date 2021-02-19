import unittest

from simulator import (
    gen_vehicle_day_samples,
    gen_day_samples_as_dict,
    flatten_vehicle_day_samples,
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

    def test_gen_vehicle_day_samples_has_same_days_as_flattened_version(self):
        vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
        names_csv_path = mk_csv_file_path("person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        sample = gen_vehicle_day_samples(10, 10, 10, medellin_center, rad, csv_data)
        sample_flattened = flatten_vehicle_day_samples(sample)
        sample_elements = []

        for vehicle_days in sample:
            for v_day in vehicle_days:
                sample_elements.append(v_day)

        for (x, y) in zip(sample_elements, sample_flattened):
            self.assertEqual(x, y)

    def test_init_time_in_vehicle_day_less_than_stop_times(self):
        vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
        names_csv_path = mk_csv_file_path("person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        sample = flatten_vehicle_day_samples(gen_vehicle_day_samples(10, 10, 10, medellin_center, rad, csv_data))

        for vehicle_day in sample:
            init_time = vehicle_day.initial_time

            for stop in vehicle_day.stops:
                self.assertTrue(init_time < stop.arrival_time)

    def test_init_time_in_key_less_than_stop_times(self):
        vehicle_csv_path = mk_csv_file_path("vehicle_list.csv")
        names_csv_path = mk_csv_file_path("person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        sample = gen_day_samples_as_dict(10, 10, 10, medellin_center, rad, csv_data)

        for day in sample:
            for key in day:
                stops = day[key]
                (_, _, init_time, _) = key
                for t in stops:
                    self.assertTrue(init_time < t.arrival_time)


# Helpers
def no_duplicates_check(ls):
    return len(ls) == len(set(ls))
