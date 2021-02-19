from vehicle import Vehicle, str_to_category
from collections import namedtuple
import csv


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
