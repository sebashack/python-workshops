from collections import namedtuple
import random as rnd
import uuid
import csv


class Driver:
    def __init__(self, idx, name):
        self.idx = idx
        self.name = name

    def __str__(self):
        return f'Driver(idx={self.idx}, name="{self.name}")'

    def __repr__(self):
        return f'Driver(idx={self.idx}, name="{self.name}")'


def gen_random_drivers(n, names, surnames):
    drivers = []

    for i in range(n):
        drivers.append(gen_random_driver(names, surnames))

    return drivers


def read_driver_names(csv_file_path):
    male_names = []
    female_names = []
    surnames = []

    with open(csv_file_path, newline="\n") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            name = row["name"]

            if row["type"] == "male":
                male_names.append(name)

            if row["type"] == "female":
                female_names.append(name)

            if row["type"] == "surname":
                surnames.append(name)

        Names = namedtuple("Names", ["female_names", "male_names", "surnames"])

    return Names(female_names, male_names, surnames)


# Private Helpers
def gen_random_driver(names, surnames):
    name = rnd.choice(names)
    surname = rnd.choice(surnames)
    return Driver(gen_idx(), mk_full_name(name, surname))


def mk_full_name(name, surname):
    return name + " " + surname


def gen_idx():
    return uuid.uuid4()
