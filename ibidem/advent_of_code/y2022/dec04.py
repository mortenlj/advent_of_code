#!/usr/bin/env python
from collections import namedtuple

from ibidem.advent_of_code.util import get_input_name


class Pair(namedtuple("Pair", ("left", "right"))):
    def size(self):
        return self.right - self.left


def load(fobj):
    for line in fobj:
        if not line.strip():
            continue
        first, second = line.split(",")
        yield (parse(first), parse(second))


def parse(s):
    left, right = s.split("-")
    return Pair(int(left), int(right))


def part1(input):
    result = 0
    for first, second in input:
        print(first, second)
        if first.size() >= second.size():
            first, second = second, first
        if first.left >= second.left and first.right <= second.right:
            print(f"{first} is contained in {second}")
            result += 1
    return result


def part2(input):
    result = 0
    for first, second in input:
        print(first, second)
        if first.size() >= second.size():
            first, second = second, first
        if first.left >= second.left and first.left <= second.right:
            print(f"{first} overlaps with {second}")
            result += 1
            continue
        if first.right >= second.left and first.right <= second.right:
            print(f"{first} overlaps with {second}")
            result += 1
    return result


if __name__ == "__main__":
    with open(get_input_name(4, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(4, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
