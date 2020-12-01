#!/usr/bin/env python
# -*- coding: utf-8

import itertools

from .util import get_input_name


class Planet(object):
    def __init__(self, name, parent_name, planets):
        self.name = name
        self._parent_name = parent_name
        self._planets = planets

    @property
    def parent(self):
        return self._planets[self._parent_name]

    @property
    def orbits(self):
        return self.parent.orbits + 1


class COM(object):
    def __init__(self):
        self.name = "COM"
        self.orbits = 0


def calculate_orbits(lines):
    planets = load_planets(lines)
    return sum(p.orbits for p in planets.values())


def load_planets(lines):
    planets = {"COM": COM()}
    for line in lines:
        parent_name, satellite_name = line.strip().split(")")
        satellite = Planet(satellite_name, parent_name, planets)
        planets[satellite_name] = satellite
    return planets


def find_path_to_com(planet):
    path = []
    current = planet.parent
    while current.name != "COM":
        path.append(current.name)
        current = current.parent
    return path


def part1():
    with open(get_input_name("dec06")) as fobj:
        total_orbits = calculate_orbits(fobj)
        print("Total orbits: {}".format(total_orbits))


def part2():
    with open(get_input_name("dec06")) as fobj:
        planets = load_planets(fobj)
        transfers = calculate_transfers(planets)
        print("Transfers: {}".format(transfers))


def calculate_transfers(planets):
    you_path = reversed(find_path_to_com(planets["YOU"]))
    san_path = reversed(find_path_to_com(planets["SAN"]))
    you_short = []
    san_short = []
    for y, s in itertools.dropwhile(lambda t: t[0] == t[1],
                                    itertools.zip_longest(you_path, san_path, fillvalue=None)):
        you_short.append(y)
        san_short.append(s)
    transfers = len(list(itertools.chain((p for p in you_short if p), (p for p in san_short if p))))
    return transfers


if __name__ == "__main__":
    part1()
    part2()
