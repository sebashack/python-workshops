import random as rnd


class Driver:
    def __init__(self, idx, name):
        self.idx = idx
        self.name = name

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return hash(self.idx)

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
