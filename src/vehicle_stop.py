from collections import namedtuple
import random as rnd
from datetime import datetime, timedelta
from faker import Faker
from math import sin, cos, sqrt, atan2, radians


Coord = namedtuple("Coord", ["latitude", "longitude"])


class VehicleStop:
    def __init__(self, coord, arrival_time):
        self.coord = coord
        self.arrival_time = arrival_time

    def __str__(self):
        la = ("latitude", self.coord.latitude)
        lg = ("longitude", self.coord.longitude)
        at = ("arrival_time", self.arrival_time)
        s = f"VehicleStop({la[0]}={la[1]}, {lg[0]}={lg[1]}, {at[0]}={at[1]})"

        return s

    def __repr__(self):
        la = ("latitude", self.coord.latitude)
        lg = ("longitude", self.coord.longitude)
        at = ("arrival_time", self.arrival_time)
        s = f"VehicleStop({la[0]}={la[1]}, {lg[0]}={lg[1]}, {at[0]}={at[1]})"

        return s

    def latitude(self):
        return self.coord.latitude

    def longitude(self):
        return self.coord.longitude


def gen_random_vehicle_stops(num_stops, day_index, coord_gen):
    stops = []
    utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    init_time = increment_utc_by_days(utc, day_index)
    t = init_time

    for _ in range(num_stops):
        sec_increment = gen_random_sec_increment(num_stops)
        arrival_time = increment_utc_by_secs(t, sec_increment)
        coord = coord_gen()
        stop = VehicleStop(coord, arrival_time)
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


# Compute the distance, in Km, between two Geo Coords
def compute_coord_distance(c1, c2):
    EARTH_RADIUS = 6371.0  # approx. earth's radious in km

    lat1 = radians(c1.latitude)
    lon1 = radians(c1.longitude)
    lat2 = radians(c2.latitude)
    lon2 = radians(c2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c

    return distance
