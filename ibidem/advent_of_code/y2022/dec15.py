#!/usr/bin/env python
import re
from collections import namedtuple

from alive_progress import alive_it

from ibidem.advent_of_code.util import get_input_name, time_this

INPUT_PATTERN = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
TUNING_FREQ_MULTIPLIER = 4000000


class Coordinate(namedtuple("Coordinate", ["x", "y"])):
    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def manhattan(self):
        return abs(self.x) + abs(self.y)


def load(fobj):
    pairs = []
    for line in fobj:
        if m := INPUT_PATTERN.match(line.strip()):
            sensor = Coordinate(int(m.group(1)), int(m.group(2)))
            beacon = Coordinate(int(m.group(3)), int(m.group(4)))
            pairs.append((sensor, beacon))
    return pairs


@time_this
def part1(pairs, depth=2000000):
    line = {}
    for sensor, beacon in pairs:
        distance = (sensor - beacon).manhattan()
        if depth not in range(sensor.y - distance, sensor.y + distance):
            continue
        rem = distance - abs(sensor.y - depth)
        for x in range(sensor.x - rem, sensor.x + rem + 1):
            line[(x, depth)] = 1
        if beacon.y == depth:
            line[(beacon.x, beacon.y)] = 0
    return sum(line.values())


def remove(possible_row, slice):
    new_row = []
    for element in possible_row:
        if slice[1] < element[0]:
            new_row.append(element)
        elif slice[0] > element[1]:
            new_row.append(element)
        elif slice[0] > element[0] and slice[1] < element[1]:
            new_row.append((element[0], slice[0] - 1))
            new_row.append((slice[1] + 1, element[1]))
        elif slice[0] <= element[0] and slice[1] >= element[1]:
            pass
        elif slice[0] <= element[0] <= slice[1]:
            new_row.append((slice[1] + 1, element[1]))
        elif slice[0] <= element[1] <= slice[1]:
            new_row.append((element[0], slice[0] - 1))
    return new_row


@time_this
def part2(pairs, max=4000000):
    for y in alive_it(range(max + 1)):
        line = [(0, max)]
        for sensor, beacon in pairs:
            distance = (sensor - beacon).manhattan()
            if (sensor.y - distance) < y <= (sensor.y + distance):
                rem = distance - abs(sensor.y - y)
                line = remove(line, (sensor.x - rem, sensor.x + rem))
            if not line:
                break
        if line:
            coord = line[0]
            return coord[0] * TUNING_FREQ_MULTIPLIER + y


if __name__ == "__main__":
    with open(get_input_name(15, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
