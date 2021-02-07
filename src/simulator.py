from collections import namedtuple
import random as rnd

from vehicle import read_vehicles
from vehicle_stop import (
    create_coord_generator,
    gen_random_coords,
    gen_random_vehicle_stops,
)
from driver import read_driver_names, gen_random_drivers


def read_csv_data(vehicles_path, names_path):
    names = read_driver_names(names_path)
    vehicles = read_vehicles(vehicles_path)

    CsvData = namedtuple("CsvData", ["names", "vehicles"])

    return CsvData(names, vehicles)


# The data structure generated by this function is the following:
# [Dict<(Vehicle, Driver, Coord), [VehicleStop]>], i.e., a list of dictionaries
# where the key is a 3-tuple related to a list of vehicle stops. Each
# dictionary is meant to represent a simulated day indexed by the position
# in the list. The `Coord` in the key is the vehicle's start coordinate.
def gen_day_samples(num_days, max_vehicle_sz, max_stops, center, rad, data):
    NUM_DAYS_UPPER_BOUND = 365
    STOP_UPPER_BOUND = 48

    if num_days < 1 or num_days > NUM_DAYS_UPPER_BOUND:
        raise Exception(f"# of days isn't in [1, {NUM_DAYS_UPPER_BOUND}]")

    if max_stops < 1 or max_stops > STOP_UPPER_BOUND:
        raise Exception(f"# of stops isn't in [1, {STOP_UPPER_BOUND}]")

    day_stops = []

    coord_gen = create_coord_generator(center, rad)

    for i in range(num_days):
        s = gen_day_sample(max_vehicle_sz, max_stops, i, coord_gen, data)
        day_stops.append(s)

    return day_stops


# Private Helpers
def gen_day_sample(max_vehicle_size, max_stops, day_idx, coord_gen, data):
    vehicles = data.vehicles

    assert max_vehicle_size > 0 and max_vehicle_size <= len(vehicles)

    vehicle_size = rnd.choice(range(1, max_vehicle_size + 1))
    names = data.names.female_names + data.names.male_names

    stop_coords = gen_random_coords(vehicle_size, coord_gen)
    drivers = gen_random_drivers(vehicle_size, names, data.names.surnames)

    keys = list(zip(vehicles, drivers, stop_coords))
    vehicle_stops = {}

    for key in keys:
        num_stops = rnd.choice(range(1, max_stops + 1))
        stops = gen_random_vehicle_stops(num_stops, day_idx, coord_gen)
        vehicle_stops[key] = stops

    return vehicle_stops
