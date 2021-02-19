class VehicleDay:
    def __init__(self, vehicle, driver, initial_coord, stops):
        self.vehicle = vehicle
        self.driver = driver
        self.initial_coord = initial_coord
        self.stops = stops

    def __eq__(self, other):
        return self.driver == other.driver

    def __str__(self):
        v = self.vehicle
        d = self.driver
        ic = self.initial_coord
        ss = self.stops

        s = f"VehicleDay(vehicle={v}, driver={d}, initial_coord={ic}, stops={ss})"
        return s

    def __repr__(self):
        v = self.vehicle
        d = self.driver
        ic = self.initial_coord
        ss = self.stops

        s = f"VehicleDay(vehicle={v}, driver={d}, initial_coord={ic}, stops={ss})"
        return s
