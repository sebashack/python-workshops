import os
from collections import namedtuple
import csv
from datetime import datetime

from driver import Driver
from vehicle_stop import VehicleStop, Coord
from vehicle import Vehicle, str_to_category, category_to_str
from vehicle_day import VehicleDay
from sorting import quick_sort_by, quick_sort


def read_csv_data(vehicles_path, names_path):
    names = read_driver_names(names_path)
    vehicles = read_vehicles(vehicles_path)

    CsvData = namedtuple("CsvData", ["names", "vehicles"])

    return CsvData(names, vehicles)


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


def read_vehicle_days(csv_file_path):
    entries = {}

    with open(csv_file_path, newline="\n") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            idx = row["citizen-id"]
            name = row["name"]
            plate = row["vehicle-plate"]
            category = str_to_category(row["vehicle-type"])
            t = datetime.strptime(row["time"], "%Y-%m-%d %H:%M:%S")
            stop = VehicleStop(
                Coord(float(row["latitude"]), float(row["longitude"])), t
            )

            key = (idx, name, plate, category, t.year, t.month, t.day)
            if key in entries:
                entries[key].append(stop)
            else:
                entries[key] = [stop]

    days = []
    for (key, stops) in entries.items():
        sorted_day = quick_sort_by(stops, lambda stop: stop.arrival_time)
        driver = Driver(key[0], key[1])
        vehicle = Vehicle(key[2], key[3])
        init = sorted_day.pop(0)

        days.append(
            VehicleDay(
                vehicle,
                driver,
                init.arrival_time,
                Coord(init.latitude(), init.longitude()),
                sorted_day,
            )
        )

    return quick_sort(days)


def write_vehicle_days(csv_path, days):
    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "citizen-id",
                "name",
                "vehicle-type",
                "vehicle-plate",
                "latitude",
                "longitude",
                "time",
            ]
        )

        for day in days:
            citizen_id = day.driver.idx
            name = day.driver.name
            init_t = str(day.initial_time)
            vehicle_type = category_to_str(day.vehicle.category)
            vehicle_plate = day.vehicle.plate
            (init_lat, init_lon) = day.initial_coord

            writer.writerow(
                [
                    citizen_id,
                    name,
                    vehicle_type,
                    vehicle_plate,
                    str(init_lat),
                    str(init_lon),
                    init_t,
                ]
            )

            for stop in day.stops:
                lat = str(stop.latitude())
                lon = str(stop.longitude())
                t = str(stop.arrival_time)

                writer.writerow(
                    [citizen_id, name, vehicle_type, vehicle_plate, lat, lon, t]
                )


def mk_csv_file_path(path):
    return str(os.path.join(os.getcwd(), path))
