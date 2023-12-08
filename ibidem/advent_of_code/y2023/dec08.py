#!/usr/bin/env python
import math
import re
from itertools import cycle

from ibidem.advent_of_code.util import get_input_name

LOAD_PATTERN = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def load(fobj):
    directions = fobj.readline().strip()
    map = {}
    for line in fobj:
        if m := LOAD_PATTERN.match(line):
            map[m.group(1)] = {"L": m.group(2), "R": m.group(3)}
    return directions, map


def part1(input):
    directions, map = input
    current = "AAA"
    for step, direction in enumerate(cycle(directions)):
        current = map[current][direction]
        if current == "ZZZ":
            return step + 1
    raise RuntimeError("No ZZZ found")


def part2(input):
    directions, map = input
    current = [node for node in map.keys() if node.endswith("A")]
    print(f"Stepping {len(current)} nodes: {current}")
    cycle_lengths = [get_steps(start, directions, map) for start in current]
    return math.lcm(*cycle_lengths)


def get_steps(start, directions, map):
    current = start
    for step, direction in enumerate(cycle(directions)):
        current = map[current][direction]
        if current.endswith("Z"):
            return step + 1
    raise RuntimeError("No end location found")


if __name__ == "__main__":
    with open(get_input_name(8, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
