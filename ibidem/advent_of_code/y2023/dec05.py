#!/usr/bin/env python
import itertools

from ibidem.advent_of_code.util import get_input_name


class Lookup:
    def __init__(self, name):
        self.name = name
        self.ranges = []

    def add(self, r):
        self.ranges.append(r)

    def lookup(self, value):
        for dest_start, source_start, length in self.ranges:
            if source_start <= value < source_start + length:
                return dest_start + value - source_start
        return value


def load(fobj):
    seeds = [int(c) for c in fobj.readline().split(":")[1].strip().split()]
    lookups = []
    lookup = None
    for line in fobj:
        line = line.strip()
        if line == "":
            continue
        if line.endswith("map:"):
            if lookup:
                lookups.append(lookup)
            lookup = Lookup(line[:-4])
            continue
        lookup.add(tuple(int(c) for c in line.split()))
    if lookup:
        lookups.append(lookup)
    return seeds, lookups


def part1(input):
    seeds, lookups = input
    locations = []
    for seed in seeds:
        value = seed
        for lookup in lookups:
            value = lookup.lookup(value)
        locations.append(value)
    return min(locations)


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def part2(input):
    seed_data, lookups = input
    seed_ranges = list(batched(seed_data, 2))
    locations = []
    for seed_start, length in seed_ranges:
        for seed in range(seed_start, seed_start + length):
            value = seed
            for lookup in lookups:
                value = lookup.lookup(value)
            locations.append(value)
    return min(locations)


if __name__ == "__main__":
    with open(get_input_name(5, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(5, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
