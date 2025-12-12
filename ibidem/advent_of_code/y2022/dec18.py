#!/usr/bin/env python
import itertools
from collections import namedtuple

from ibidem.advent_of_code.util import get_input_name, gen_list

Cube = namedtuple("Cube", ("x", "y", "z"))


@gen_list
def load(fobj):
    for line in fobj:
        x, y, z = line.strip().split(",")
        yield Cube(int(x), int(y), int(z))


def part1(cubes):
    total_sides = len(cubes) * 6
    for left, right in itertools.combinations(cubes, 2):
        for idx in range(3):
            if (
                left[idx] in (right[idx] - 1, right[idx] + 1)
                and left[idx - 1] == right[idx - 1]
                and left[idx - 2] == right[idx - 2]
            ):
                total_sides -= 2
                break
    return total_sides


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(18, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
