#!/usr/bin/env python
import multiprocessing
import os
import re
import time
from collections import namedtuple

import numpy as np
from tqdm import tqdm

from ibidem.advent_of_code.util import get_input_name

PATTERN = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")

Step = namedtuple("Step", ("action", "x_range", "y_range", "z_range"))


class Range:
    __getitem__ = __setitem__ = __delitem__ = None

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __contains__(self, item):
        return self.start <= item <= self.stop

    def __len__(self):
        return self.stop - self.start

    def __iter__(self):
        return (i for i in range(self.start, self.stop))

    def as_slice(self, shift=0):
        return slice(self.start - shift, self.stop - shift)


def load(fobj, bounds=50):
    for line in fobj:
        m = PATTERN.search(line)
        assert m
        action = m.group(1)
        x_range = Range(int(m.group(2)) + bounds, int(m.group(3)) + 1 + bounds)
        y_range = Range(int(m.group(4)) + bounds, int(m.group(5)) + 1 + bounds)
        z_range = Range(int(m.group(6)) + bounds, int(m.group(7)) + 1 + bounds)
        if not all(
                0 <= s.start <= bounds * 2 + 1 and 0 <= s.stop <= bounds * 2 + 1 for s in (x_range, y_range, z_range)):
            continue
        yield Step(action == "on", x_range, y_range, z_range)


def part1(steps):
    g = np.zeros((101, 101, 101), dtype=bool)
    for step in steps:
        g[step.z_range.as_slice(), step.y_range.as_slice(), step.x_range.as_slice()] = step.action
    flat = g.flatten()
    return flat.sum()


def gen_coord(step):
    for x in step.x_range:
        for y in step.y_range:
            for z in step.z_range:
                yield x, y, z


def select_steps(steps, x_lim, y_lim):
    for step in steps:
        if x_lim not in step.x_range:
            continue
        if y_lim not in step.y_range:
            continue
        yield step


def find_bound(slices):
    slices = list(slices)
    return min(s.start for s in slices), max(s.stop for s in slices)


def activate_row(steps, x, y):
    start, stop = find_bound((s.z_range for s in steps))
    row = np.array((stop - start,), dtype=bool)
    for step in select_steps(steps, x, y):
        row[step.z_range.as_slice(start)] = step.action
    result = row.sum()
    return result


def gen_values(slices):
    for slice in slices:
        for v in slice:
            yield v


def part2(input):
    bound = 200000
    steps = list(load(input, bound))
    start = time.monotonic()
    with multiprocessing.Pool(os.cpu_count() // 2) as pool:
        count = 0
        for x in tqdm(gen_values((s.x_range for s in steps))):
            results = []
            for y in gen_values((s.y_range for s in steps)):
                results.append(pool.apply_async(activate_row, (steps, x, y)))
            print(f"Started processing of {len(results)} rows")
            for result in tqdm(results):
                count += result.get()
                if time.monotonic() - start > 600:
                    raise RuntimeError("Timed out")
    return count


if __name__ == "__main__":
    with open(get_input_name(22, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(22, 2021)) as fobj:
        p2_result = part2(fobj)
        print(f"Part 2: {p2_result}")
