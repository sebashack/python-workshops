from enum import Enum
import csv


class Category(Enum):
    MotorBike = 0
    SmallTruck = 1
    BigTruck = 2


class Vehicle:
    def __init__(self, plate, category):
        self.category = category
        self.plate = plate

    def __str__(self):
        return f'Vehicle(plate="{self.plate}", category={self.category})'

    def __repr__(self):
        return f'Vehicle(plate="{self.plate}", category={self.category})'


def read_vehicles(csv_file_path):
    vehicles = []

    with open(csv_file_path, newline="\n") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            plate = row["plate"]
            category = str_to_category(row["category"])
            vehicle = Vehicle(plate, category)

            vehicles.append(vehicle)

    return vehicles


# Private Helpers
def str_to_category(s):
    if s == "motor-bike":
        return Category.MotorBike

    if s == "small-truck":
        return Category.SmallTruck

    if s == "big-truck":
        return Category.BigTruck

    raise Exception(f'Invalid Vehicle category "{s}"')
