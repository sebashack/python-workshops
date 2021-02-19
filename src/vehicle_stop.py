from collections import namedtuple
import random as rnd
from datetime import datetime, timedelta
from faker import Faker


class VehicleStop:
    def __init__(self, latitude, longitude, arrival_time):
        self.latitude = latitude
        self.longitude = longitude
        self.arrival_time = arrival_time

    def __str__(self):
        la = ("latitude", self.latitude)
        lg = ("longitude", self.longitude)
        at = ("arrival_time", self.arrival_time)
        s = f"VehicleStop({la[0]}={la[1]}, {lg[0]}={lg[1]}, {at[0]}={at[1]})"

        return s

    def __repr__(self):
        la = ("latitude", self.latitude)
        lg = ("longitude", self.longitude)
        at = ("arrival_time", self.arrival_time)
        s = f"VehicleStop({la[0]}={la[1]}, {lg[0]}={lg[1]}, {at[0]}={at[1]})"

        return s


def gen_random_vehicle_stops(num_stops, day_index, coord_gen):
    stops = []
    utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    init_time = increment_utc_by_days(utc, day_index)
    t = init_time

    for _ in range(num_stops):
        sec_increment = gen_random_sec_increment(num_stops)
        arrival_time = increment_utc_by_secs(t, sec_increment)
        coord = coord_gen()
        stop = VehicleStop(coord.latitude, coord.longitude, arrival_time)
        stops.append(stop)
        t = arrival_time

    return (init_time, stops)


def gen_random_coords(size, coord_gen):
    coords = []

    for _ in range(size):
        coords.append(coord_gen())

    return coords


def create_coord_generator(center, rad):
    gen = Faker()

    def f():
        return gen_random_coord(center, rad, gen)

    return f


Coord = namedtuple("Coord", ["latitude", "longitude"])


# Generate random coords from a center outwards.
def gen_random_coord(center, rad, generator):
    lat = generator.coordinate(center=center[0], radius=rad)
    lon = generator.coordinate(center=center[1], radius=rad)

    return Coord(float(lat), float(lon))


def gen_random_sec_increment(num_stops):
    hour_mins = 60
    day_mins = 24 * hour_mins
    steps = round(day_mins / num_stops)
    secs = rnd.choice(range(1, steps + 1)) * hour_mins

    return secs


def increment_utc_by_days(utc, num_days):
    one_day = 86400
    days = timedelta(seconds=one_day * num_days)

    return utc + days


def increment_utc_by_secs(utc, secs):
    secs = timedelta(seconds=secs)

    return utc + secs
