from sorting import quick_sort_by
from vehicle_stop import compute_coord_distance, VehicleStop


class VehicleDay:
    def __init__(self, vehicle, driver, initial_time, initial_coord, stops):
        self.vehicle = vehicle
        self.driver = driver
        self.initial_time = initial_time
        self.initial_coord = initial_coord
        self.stops = stops

    def __eq__(self, other):
        return self.vehicle == other.vehicle and self.initial_time == other.initial_time

    def __lt__(self, other):
        return self.initial_time < other.initial_time

    def __le__(self, other):
        return self.initial_time <= other.initial_time

    def __gt__(self, other):
        return self.initial_time > other.initial_time

    def __ge__(self, other):
        return self.initial_time >= other.initial_time

    def __str__(self):
        v = self.vehicle
        d = self.driver
        it = self.initial_time
        ic = self.initial_coord
        ss = self.stops

        s = f"VehicleDay(vehicle={v}, driver={d}, initial_time={it}, initial_coord={ic}, stops={ss})"
        return s

    def __repr__(self):
        v = self.vehicle
        d = self.driver
        it = self.initial_time
        ic = self.initial_coord
        ss = self.stops

        s = f"VehicleDay(vehicle={v}, driver={d}, initial_time={it}, initial_coord={ic}, stops={ss})"
        return s

    def gen_route_by_distance_against_init_coord(self):
        stops = quick_sort_by(
            self.stops,
            lambda stop: compute_coord_distance(self.initial_coord, stop.coord),
        )

        return (self.initial_coord, stops)

    def sort_stops_by_arrival_time(self):
        self.stops = quick_sort_by(self.stops, lambda stop: stop.arrival_time)

    # This method assumes that the stops are sorted by arrival_time.
    # The output is in Kilometers.
    def compute_route_distance(self):
        stops = [VehicleStop(self.initial_coord, self.initial_time)] + self.stops
        tail = stops[1:]
        d = 0

        for (stop1, stop2) in zip(stops, tail):
            d += compute_coord_distance(stop1.coord, stop2.coord)

        return d

    def stops_length(self):
        return len(self.stops)


def sort_vehicle_days_by_route_distance(days):
    return quick_sort_by(days, lambda v: v.compute_route_distance())
