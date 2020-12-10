#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(10, 2020)) as fobj:
        return [int(l) for l in fobj]


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


def part2():
    pass


if __name__ == "__main__":
    adapters = load()
    part1(adapters)
    part2()
