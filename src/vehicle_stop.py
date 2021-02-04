from collections import namedtuple
import random as rnd
import csv
from datetime import datetime, timedelta


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
    utc = get_current_utc_time()
    utc = utc.replace(hour=0, minute=0, second=0, microsecond=0)
    t = advance_utc(day_index, utc, 0)

    for i in range(num_stops):
        arrival_time = advance_utc(0, t, gen_random_sec_increment())
        coord = rnd.choice(stop_coords)
        stop = VehicleStop(coord.latitude, coord.longitude, arrival_time)
        stops.append(stop)
        t = arrival_time

    return stops


# Private Helpers
def read_coordinates(csv_file_path):
    coordinates = []

    with open(csv_file_path, newline="\n") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            lat = float(row["latitude"])
            lon = float(row["longitude"])

            Coord = namedtuple("Coord", ["latitude", "longitude"])

            coordinates.append(Coord(lat, lon))

    return coordinates


def gen_random_sec_increment():
    inc_10_mins = 600
    # Pick out a random increment in a range
    # [10mins, 20mins, 30mins, ..., 120mins], 120mins = 2hs
    increment = rnd.choice(range(inc_10_mins, 13 * inc_10_mins, inc_10_mins))

    return increment


def advance_utc(day_index, start_time, increment_secs):
    one_day = 86400
    days = timedelta(seconds=one_day * day_index)
    secs = timedelta(seconds=increment_secs)

    return start_time + days + secs


def get_current_utc_time():
    return datetime.utcnow()
