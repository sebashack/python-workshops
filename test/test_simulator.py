import unittest
from datetime import datetime

from simulator import (
    gen_day_samples,
    gen_day_samples_with_variable_size,
    flatten_day_samples,
)
from sorting import quick_sort
from csv_utils import mk_csv_file_path, read_csv_data, read_vehicle_days, write_vehicle_days
from vehicle_stop import compute_coord_distance, Coord, VehicleStop
from vehicle_day import VehicleDay, sort_vehicle_days_by_route_distance
from vehicle import Vehicle, Category
from driver import Driver


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

    def test_day_samples_have_stops_in_asc_order_by_time(self):
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        samples = flatten_day_samples(gen_day_samples(30, 30, 20, medellin_center, rad, csv_data))

        for day in samples:
            self.assertTrue(is_asc_ordered(day.stops))

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

    def test_compute_coord_distance_returns_expected_values(self):
        tolerance = 0.001

        c1 = Coord(6.222833, -75.530807)
        c2 = Coord(6.20579, -75.584041)
        d = compute_coord_distance(c1, c2)
        expected_distance = 6.182  # Km

        self.assertLessEqual(abs(d - expected_distance), tolerance)

        c1 = Coord(6.240636, -75.579491)
        c2 = Coord(6.271504, -75.565508)
        d = compute_coord_distance(c1, c2)
        expected_distance = 3.764  # Km

        self.assertLessEqual(abs(d - expected_distance), tolerance)

        c1 = Coord(6.253964, -75.581604)
        c2 = Coord(6.199261, -75.564502)
        d = compute_coord_distance(c1, c2)
        expected_distance = 6.37  # Km

        self.assertLessEqual(abs(d - expected_distance), tolerance)

        c1 = Coord(6.201947, -75.547499)
        c2 = Coord(6.248299, -75.549634)
        d = compute_coord_distance(c1, c2)
        expected_distance = 5.16  # Km

        self.assertLessEqual(abs(d - expected_distance), tolerance)

    def test_compute_route_distance_returns_expected_value(self):
        tolerance = 0.001

        dummy_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        vehicle = Vehicle("XSD124", Category.SmallTruck)
        driver = Driver("12239812", "Michael Heart")
        init_coord = Coord(6.222833, -75.530807)

        c0 = Coord(6.20579, -75.584041)
        c1 = Coord(6.240636, -75.579491)
        c2 = Coord(6.271504, -75.565508)
        c3 = Coord(6.253964, -75.581604)
        c4 = Coord(6.199261, -75.564502)
        c5 = Coord(6.201947, -75.547499)
        c6 = Coord(6.248299, -75.549634)

        stops = [VehicleStop(c0, dummy_date),
                 VehicleStop(c1, dummy_date),
                 VehicleStop(c2, dummy_date),
                 VehicleStop(c3, dummy_date),
                 VehicleStop(c4, dummy_date),
                 VehicleStop(c5, dummy_date),
                 VehicleStop(c6, dummy_date)]

        expected_distance = compute_coord_distance(init_coord, c0) + \
            compute_coord_distance(c0, c1) + compute_coord_distance(c1, c2) + \
            compute_coord_distance(c2, c3) + compute_coord_distance(c3, c4) + \
            compute_coord_distance(c4, c5) + compute_coord_distance(c5, c6)

        day = VehicleDay(vehicle, driver, dummy_date, init_coord, stops)

        self.assertEqual(stops, day.stops)
        self.assertLessEqual(abs(day.compute_route_distance() - expected_distance), tolerance)

    def test_day_samples_have_asc_order_by_route_distance(self):
        # Run simulation for 30 days, a max of 100 vehicles per day and
        # a max of 20 stops per vehicle per day.
        vehicle_csv_path = mk_csv_file_path("test_data/vehicle_list.csv")
        names_csv_path = mk_csv_file_path("test_data/person_list.csv")
        csv_data = read_csv_data(vehicle_csv_path, names_csv_path)
        medellin_center = (6.251404, -75.575261)
        rad = 0.055
        samples = flatten_day_samples(gen_day_samples_with_variable_size(30, 10, 20, medellin_center, rad, csv_data))

        def f(day):
            return day.compute_route_distance()

        self.assertTrue(is_asc_ordered_by(sort_vehicle_days_by_route_distance(samples), f))


# Helpers
def no_duplicates_check(ls):
    return len(ls) == len(set(ls))


def is_asc_ordered_by(ls, f):
    tail = ls[1:]

    for (x, y) in zip(ls, tail):
        if f(x) > f(y):
            return False

    return True


def is_asc_ordered(ls):
    tail = ls[1:]

    for (x, y) in zip(ls, tail):
        if x > y:
            return False

    return True
