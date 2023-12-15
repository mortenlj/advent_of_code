#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return fobj.read().strip().split(",")


def hash(step):
    cv = 0
    for c in step:
        cv += ord(c)
        cv = cv * 17
        cv = cv % 256
    return cv


def part1(input):
    return sum(hash(step) for step in input)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(15, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
