#!/usr/bin/env python
from collections import Counter

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    left, right = [], []
    for line in fobj:
        parts = line.split()
        left.append(int(parts[0]))
        right.append(int(parts[1]))
    return left, right


def part1(input):
    left, right = input
    diff = 0
    for l, r in zip(sorted(left), sorted(right)):
        diff += abs(r - l)
    return diff


def part2(input):
    left, right = input
    counts = Counter(right)
    score = 0
    for loc in left:
        score += loc*counts[loc]
    return score

if __name__ == "__main__":
    with open(get_input_name(1, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(1, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
