import unittest
from datetime import datetime

from test1 import add
from vehicle_stop import compute_coord_distance, Coord, VehicleStop
from vehicle_day import VehicleDay
from vehicle import Vehicle, Category
from driver import Driver


class TestSortingProblem(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 1), 2)

    def test_gen_route_by_distance_against_init_coord_gens_route_from_nearest_to_furthest(self):
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

        day = VehicleDay(vehicle, driver, dummy_date, init_coord, stops)

        (init_coord, stops) = day.gen_route_by_distance_against_init_coord()
        stop_coords = list(map(lambda s: s.coord, stops))

        for (prev_c, next_c) in zip(stop_coords, stop_coords[1:]):
            d1 = compute_coord_distance(init_coord, prev_c)
            d2 = compute_coord_distance(init_coord, next_c)

            self.assertLessEqual(d1, d2)
