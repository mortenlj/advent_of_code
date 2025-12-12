#!/usr/bin/env python
from collections import defaultdict

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(10, 2020)) as fobj:
        return [int(line) for line in fobj]


def part1(adapters):
    adapters.sort()
    ones = threes = 0
    previous = 0
    for i, adapter in enumerate(adapters):
        diff = adapter - previous
        ones += int(diff == 1)
        threes += int(diff == 3)
        previous = adapter
    threes += 1  # The adapter is 3 above the highest
    result = ones * threes
    print(f"Part 1 result: {result}")
    return result


def part2(adapters):
    adapters = list(reversed(sorted(adapters)))
    paths_from = defaultdict(int)
    paths_from[max(adapters) + 3] = 1
    for i in adapters:
        paths_from[i] = paths_from[i + 1] + paths_from[i + 2] + paths_from[i + 3]
    result = paths_from[1] + paths_from[2] + paths_from[3]
    print(f"Part 2 result: {result}")
    return result


if __name__ == "__main__":
    adapters = load()
    part1(adapters)
    part2(adapters)
