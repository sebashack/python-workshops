from enum import Enum


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


def category_to_str(cat):
    if cat == Category.MotorBike:
        return "motor-bike"

    if cat == Category.SmallTruck:
        return "small-truck"

    if cat == Category.BigTruck:
        return "big-truck"


def str_to_category(s):
    if s == "motor-bike":
        return Category.MotorBike

    if s == "small-truck":
        return Category.SmallTruck

    if s == "big-truck":
        return Category.BigTruck

    raise Exception(f'Invalid Vehicle category "{s}"')
