import random as rnd
from vehicle_stop import (
    create_coord_generator,
    gen_random_coords,
    gen_random_vehicle_stops,
)
from driver import gen_random_drivers
from vehicle_day import VehicleDay


# Constants
NUM_DAYS_UPPER_BOUND = 365
STOP_UPPER_BOUND = 48


# The data structure generated by this function is `[VehicleDay]`
def flatten_day_samples(sample):
    return [item for sublist in sample for item in sublist]


# The data structure generated by this function is `[[VehicleDay]]`
def gen_day_samples_with_variable_size(
    num_days, max_vehicle_size, max_stops, center, rad, data, variable_stops=True
):
    check_num_days_max_stops(max_vehicle_size, max_stops)
    vehicle_size = rnd.choice(range(1, max_vehicle_size + 1))

    return gen_day_samples(
        num_days, vehicle_size, max_stops, center, rad, data, variable_stops
    )


# The data structure generated by this function is `[[VehicleDay]]`
def gen_day_samples(
    num_days, vehicle_size, max_stops, center, rad, data, variable_stops=False
):
    check_num_days_max_stops(num_days, max_stops)

    vehicle_days = []
    coord_gen = create_coord_generator(center, rad)

    names = data.names.female_names + data.names.male_names
    drivers = gen_random_drivers(vehicle_size, names, data.names.surnames)

    assert vehicle_size > 0 and vehicle_size <= len(data.vehicles)

    for i in range(num_days):
        s = gen_day_sample(
            max_stops, i, coord_gen, drivers, data.vehicles, variable_stops
        )
        vehicle_days.append(s)

    return vehicle_days


# Private Helpers
def gen_day_sample(max_stops, day_idx, coord_gen, drivers, vehicles, variable_stops):
    init_coords = gen_random_coords(len(drivers), coord_gen)

    keys = list(zip(vehicles, drivers, init_coords))
    vehicle_days = []

    for key in keys:
        num_stops = max_stops

        if variable_stops:
            num_stops = rnd.choice(range(1, max_stops + 1))

        (init_time, stops) = gen_random_vehicle_stops(num_stops, day_idx, coord_gen)
        vehicle_days.append(VehicleDay(key[0], key[1], init_time, key[2], stops))

    return vehicle_days


def check_num_days_max_stops(num_days, max_stops):
    if num_days < 1 or num_days > NUM_DAYS_UPPER_BOUND:
        raise Exception(f"# of days isn't in [1, {NUM_DAYS_UPPER_BOUND}]")

    if max_stops < 1 or max_stops > STOP_UPPER_BOUND:
        raise Exception(f"# of stops isn't in [1, {STOP_UPPER_BOUND}]")
