#!/usr/bin/env python
import functools
import itertools
from collections import namedtuple
from typing import Iterable

from ibidem.advent_of_code.util import get_input_name


class Range(namedtuple("Range", ("start", "length"))):
    @property
    def end(self):
        return self.start + self.length


@functools.total_ordering
class RangeMap:
    def __init__(self, dest_start, source_start, length):
        self.dest_start = dest_start
        self.source_start = source_start
        self.length = length
        self._source_end = source_start + length

    def __eq__(self, other):
        return (self.dest_start, self.source_start, self.length) == (
            other.dest_start,
            other.source_start,
            other.length,
        )

    def __lt__(self, other):
        return (self.dest_start, self.source_start, self.length) < (
            other.dest_start,
            other.source_start,
            other.length,
        )

    def cut(self, range: Range) -> (Iterable[Range], Iterable[Range]):
        """Divide range into mapped and unmapped parts."""
        if range.end <= self.source_start:  # Range is fully before
            return [range], []
        if range.start > self._source_end:  # Range is fully after
            return [range], []
        if (
            range.start >= self.source_start and range.end <= self._source_end
        ):  # Range is fully inside
            return [], [
                Range(self.dest_start + range.start - self.source_start, range.length)
            ]

        if (
            range.start < self.source_start and range.end < self._source_end
        ):  # Range overlaps before
            return [Range(range.start, self.source_start - range.start)], [
                Range(self.dest_start, range.length - (self.source_start - range.start))
            ]
        if (
            self.source_start <= range.start < self._source_end < range.end
        ):  # Range overlaps after
            return [Range(self._source_end, range.end - self._source_end)], [
                Range(
                    self.dest_start + range.start - self.source_start,
                    self._source_end - range.start,
                )
            ]
        # Range completely contains
        return [
            Range(range.start, self.source_start - range.start),
            Range(self._source_end, range.end - self._source_end),
        ], [Range(self.dest_start, self.length)]


class Lookup:
    def __init__(self, name):
        self.name = name
        self.ranges = []

    def add(self, r):
        self.ranges.append(RangeMap(*r))

    def lookup(self, value):
        for range_map in self.ranges:
            if (
                range_map.source_start
                <= value
                < range_map.source_start + range_map.length
            ):
                return range_map.dest_start + value - range_map.source_start
        return value

    def lookup_range(self, range: Range) -> Iterable[Range]:
        unmapped = [range]
        for range_map in self.ranges:
            new_unmapped = []
            while unmapped:
                u, mapped = range_map.cut(unmapped.pop())
                yield from mapped
                new_unmapped.extend(u)
            unmapped = new_unmapped
        if unmapped:
            yield from unmapped


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
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def part2(input):
    seed_data, lookups = input
    seed_ranges = [Range(*r) for r in batched(seed_data, 2)]
    locations = []
    for range in seed_ranges:
        values = [range]
        for lookup in lookups:
            new_values = []
            for value in values:
                new_values.extend(lookup.lookup_range(value))
            values = new_values
        locations.extend(values)
    return min(location.start for location in locations)


if __name__ == "__main__":
    with open(get_input_name(5, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(5, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
