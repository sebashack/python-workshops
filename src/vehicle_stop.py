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


def gen_random_vehicle_stops(num_stops, day_index, stop_coords):
    stops = []
    utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    t = increment_utc_by_days(utc, day_index)

    for _ in range(num_stops):
        arrival_time = increment_utc_by_secs(t, gen_random_sec_increment())
        coord = rnd.choice(stop_coords)
        stop = VehicleStop(coord.latitude, coord.longitude, arrival_time)
        stops.append(stop)
        t = arrival_time

    return stops


# Generate random coords from a center outwards.
def gen_random_coords(size, center, rad):
    fake = Faker()
    coords = []
    Coord = namedtuple("Coord", ["latitude", "longitude"])

    for _ in range(size):
        lat = fake.coordinate(center=center[0], radius=rad)
        lon = fake.coordinate(center=center[1], radius=rad)
        coords.append(Coord(float(lat), float(lon)))

    return coords


# Private Helpers
def gen_random_sec_increment():
    inc_10_mins = 600
    # Pick out a random increment in a range
    # [10mins, 20mins, 30mins, ..., 120mins], 120mins = 2hs
    increment = rnd.choice(range(inc_10_mins, 13 * inc_10_mins, inc_10_mins))

    return increment


def increment_utc_by_days(utc, num_days):
    one_day = 86400
    days = timedelta(seconds=one_day * num_days)

    return utc + days


def increment_utc_by_secs(utc, secs):
    secs = timedelta(seconds=secs)

    return utc + secs
