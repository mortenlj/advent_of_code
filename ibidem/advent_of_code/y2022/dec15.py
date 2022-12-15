#!/usr/bin/env python
import re
from collections import namedtuple

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
            print(f"Sensor at {sensor} with closest beacon at {beacon} is out of range from depth {depth}, ignoring")
            continue
        for y in range(sensor.y - distance, sensor.y + distance + 1):
            if y != depth:
                continue
            rem = distance - abs(sensor.y - y)
            for x in range(sensor.x - rem, sensor.x + rem + 1):
                line[(x, y)] = 1
        if sensor.y == depth:
            line[(sensor.x, sensor.y)] = 1
        if beacon.y == depth:
            line[(beacon.x, beacon.y)] = 0
    return sum(line.values())


def part2(pairs, max=4000000):
    return None


if __name__ == "__main__":
    with open(get_input_name(15, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
