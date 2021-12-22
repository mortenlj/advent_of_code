#!/usr/bin/env python
import re
from collections import namedtuple

import numpy as np

from ibidem.advent_of_code.util import get_input_name

PATTERN = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")

Step = namedtuple("Step", ("action", "x_slice", "y_slice", "z_slice"))


def load(fobj):
    for line in fobj:
        m = PATTERN.search(line)
        assert m
        action = m.group(1)
        x_slice = slice(int(m.group(2)) + 50, int(m.group(3)) + 1 + 50)
        y_slice = slice(int(m.group(4)) + 50, int(m.group(5)) + 1 + 50)
        z_slice = slice(int(m.group(6)) + 50, int(m.group(7)) + 1 + 50)
        if not all(0 <= s.start <= 101 and 0 <= s.stop <= 101 for s in (x_slice, y_slice, z_slice)):
            continue
        yield Step(action == "on", x_slice, y_slice, z_slice)


def part1(steps):
    g = np.zeros((101, 101, 101), dtype=bool)
    for step in steps:
        g[step.z_slice, step.y_slice, step.x_slice] = step.action
    flat = g.flatten()
    return flat.sum()


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(22, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(22, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
