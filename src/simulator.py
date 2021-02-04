from collections import namedtuple
import random as rnd

from vehicle import read_vehicles
from vehicle_stop import (
    gen_random_vehicle_stops,
    read_coordinates,
)
from driver import read_driver_names, gen_random_drivers


def read_csv_data(vehicles_path, coords_path, names_path):
    names = read_driver_names(names_path)
    vehicles = read_vehicles(vehicles_path)
    coords = read_coordinates(coords_path)

    CsvData = namedtuple("CsvData", ["names", "vehicles", "coords"])

    return CsvData(names, vehicles, coords)


def gen_day_samples(num_days, vehicle_size, max_stops, csv_data):
    day_stops = []

    for day_i in range(num_days - 1):
        day_sample = gen_day_sample(vehicle_size, max_stops, day_i, csv_data)
        day_stops.append(day_sample)

    return day_stops


# Private Helpers

def gen_day_sample(max_vehicle_size, max_stops, day_index, csv_data):
    vehicles = csv_data.vehicles

    assert max_vehicle_size > 0 and max_vehicle_size <= len(vehicles)
    assert max_stops > 0 and max_stops < 100
    assert day_index >= 0 and day_index < 100

    vehicle_size = rnd.choice(range(1, max_vehicle_size + 1))
    names = csv_data.names.female_names + csv_data.names.male_names
    start_coords = csv_data.coords[:vehicle_size]
    stop_coords = csv_data.coords[vehicle_size:]
    drivers = gen_random_drivers(vehicle_size, names, csv_data.names.surnames)

    rnd.shuffle(start_coords)
    rnd.shuffle(stop_coords)
    rnd.shuffle(vehicles)
    rnd.shuffle(drivers)

    keys = list(zip(vehicles, drivers, start_coords))
    vehicle_stops = {}

    for key in keys:
        num_stops = rnd.choice(range(1, max_stops + 1))
        stops = gen_random_vehicle_stops(num_stops, day_index, stop_coords)
        vehicle_stops[key] = stops

    return vehicle_stops
