#!/usr/bin/env python
from collections import defaultdict

import numpy as np

from ibidem.advent_of_code.util import get_input_name


def part1(fobj):
    return simulate(fobj, 80)


def simulate(fobj, days):
    sim = np.fromstring(fobj.read(), dtype=int, sep=",")
    for day in range(days):
        spawners = (sim == 0).sum()
        sim -= 1
        sim = np.pad(sim, (0, spawners), mode="constant", constant_values=8)
        sim[sim == -1] = 6
    return len(sim)


def part2(fobj):
    counters = defaultdict(int)
    initial = np.fromstring(fobj.read(), dtype=int, sep=",")
    for v in initial:
        counters[v] += 1
    for day in range(256):
        new = defaultdict(int)
        for i in range(8):
            new[i] = counters[i+1]
        new[8] = counters[0]
        new[6] += counters[0]
        counters = new
    return sum(counters.values())


if __name__ == "__main__":
    with open(get_input_name(6, 2021)) as fobj:
        p1_result = part1(fobj)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2021)) as fobj:
        p2_result = part2(fobj)
        print(f"Part 2: {p2_result}")
