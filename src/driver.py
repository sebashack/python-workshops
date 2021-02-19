from collections import namedtuple
import random as rnd
import csv


class Driver:
    def __init__(self, idx, name):
        self.idx = idx
        self.name = name

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        idx = self.idx[:]
        return hash(idx)

    def __str__(self):
        return f'Driver(idx={self.idx}, name="{self.name}")'

    def __repr__(self):
        return f'Driver(idx={self.idx}, name="{self.name}")'


def gen_random_drivers(n, names, surnames):
    drivers = []

    while len(drivers) < n:
        driver = gen_random_driver(names, surnames)

        if driver not in drivers:
            drivers.append(driver)

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


def gen_random_driver(names, surnames):
    name = rnd.choice(names)
    surname = rnd.choice(surnames)
    return Driver(gen_idx(), mk_full_name(name, surname))


# Private Helpers
def mk_full_name(name, surname):
    return name + " " + surname


def gen_idx():
    idx = "" + str(rnd.randint(1, 9))
    for _ in range(10):
        idx += str(rnd.choice(range(1, 10)))

    return idx
