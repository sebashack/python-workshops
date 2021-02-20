import unittest

from simulator import (
    gen_day_samples,
    gen_day_samples_with_variable_size,
    flatten_day_samples,
)
from sorting import quick_sort
from csv_utils import mk_csv_file_path, read_csv_data, read_vehicle_days, write_vehicle_days


class TestSimulator(unittest.TestCase):
    def test_day_samples_have_correct_size_when_no_variable_size(self):
        # Run simulation for 30 days, 100 vehicles per day and 20 stops per vehicle per day.
        # This creates locations approximately in "El area Metropolitana".
        # Medellin's center is located approximately at (lat = 6.251404, lon = -75.575261)
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        samples = flatten_day_samples(gen_day_samples(30, 100, 20, medellin_center, rad, csv_data))
        total_stops = sum(map(lambda vd: vd.stops_length(), samples))
        self.assertEqual(total_stops, 30 * 100 * 20)

    def test_day_samples_have_size_equal_or_less_than_max_when_variable_size(self):
        # Run simulation for 30 days, a max of 100 vehicles per day and
        # a max of 20 stops per vehicle per day.
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        samples = flatten_day_samples(gen_day_samples_with_variable_size(30, 100, 20, medellin_center, rad, csv_data))
        total_stops = sum(map(lambda vd: vd.stops_length(), samples))
        self.assertLessEqual(total_stops, 30 * 100 * 20)

    def test_no_duplicated_drivers_in_same_day_for_gen_vehicle_day_samples(self):
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        samples = gen_day_samples(10, 10, 10, medellin_center, rad, csv_data)

        for vehicle_days in samples:
            drivers = list(map(lambda vd: vd.driver, vehicle_days))
            self.assertTrue(no_duplicates_check(drivers))

    def test_gen_vehicle_day_samples_has_same_days_as_flattened_version(self):
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        sample = gen_day_samples(10, 10, 10, medellin_center, rad, csv_data)
        sample_flattened = flatten_day_samples(sample)
        sample_elements = []

        for vehicle_days in sample:
            for v_day in vehicle_days:
                sample_elements.append(v_day)

        for (x, y) in zip(sample_elements, sample_flattened):
            self.assertEqual(x, y)

    def test_init_time_in_vehicle_day_less_than_stop_times(self):
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        sample = flatten_day_samples(gen_day_samples(10, 10, 10, medellin_center, rad, csv_data))

        for vehicle_day in sample:
            init_time = vehicle_day.initial_time

            for stop in vehicle_day.stops:
                self.assertTrue(init_time < stop.arrival_time)

    def test_read_vehicle_days_are_equal_to_sorted_flattened_data(self):
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055

        sample = gen_day_samples(30, 100, 15, medellin_center, rad, csv_data)
        sample_flattened = flatten_day_samples(sample)
        entries_path = mk_csv_file_path("test_data/entries.csv")

        write_vehicle_days(entries_path, sample_flattened)
        vehicle_days = read_vehicle_days(entries_path)

        self.assertTrue(vehicle_days == quick_sort(sample_flattened))
        self.assertTrue(is_asc_ordered(vehicle_days))


# Helpers
def no_duplicates_check(ls):
    return len(ls) == len(set(ls))


def is_asc_ordered(ls):
    tail = ls[1:]

    for (x, y) in zip(ls, tail):
        if x > y:
            return False

    return True
