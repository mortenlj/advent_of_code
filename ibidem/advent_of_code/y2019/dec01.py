#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name

# I don't remember how this was done, and the code is nowhere to be found. Added file for AoCTiles.


def load(fobj):
    return fobj.read()


def part1(input):
    return None


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(1, 2019)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(1, 2019)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
