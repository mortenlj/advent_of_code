#!/usr/bin/env python
from itertools import pairwise

from ibidem.advent_of_code.util import get_input_name, gen_list


@gen_list
def load(fobj):
    for line in fobj:
        yield [int(c) for c in line.split()]


def solve1(case):
    if all(c == 0 for c in case):
        return 0
    differences = [b - a for a, b in pairwise(case)]
    return differences[-1] + solve1(differences)


def part1(input):
    result = 0
    for case in input:
        result += case[-1] + solve1(case)
    return result


def solve2(case):
    if all(c == 0 for c in case):
        return 0
    differences = [b - a for a, b in pairwise(case)]
    return differences[0] - solve2(differences)


def part2(input):
    result = 0
    for case in input:
        result += case[0] - solve2(case)
    return result


if __name__ == "__main__":
    with open(get_input_name(9, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
