#!/usr/bin/env python
from functools import cmp_to_key
from itertools import chain

from ibidem.advent_of_code.util import get_input_name

DIVIDER_PACKAGES = (
    [[2]],
    [[6]],
)


def load(fobj):
    pairs = []
    current = []
    for line in fobj:
        if not line.strip():
            pairs.append(tuple(current))
            current = []
            continue
        value = eval(line)
        current.append(value)
    if current:
        pairs.append(tuple(current))
    return pairs


def compare(pair):
    match pair:
        case [int(l), int(r)]:
            return l - r
        case [int(l), list(r)]:
            return compare(([l], r))
        case [list(l), int(r)]:
            return compare((l, [r]))
        case [list(l), list(r)]:
            for pair in zip(l, r):
                if (cmp := compare(pair)) != 0:
                    return cmp
            if len(l) != len(r):
                return len(l) - len(r)
    return 0


def part1(pairs):
    indexes = []
    for i, pair in enumerate(pairs):
        if compare(pair) < 0:
            indexes.append(i + 1)
    return sum(indexes)


def part2(pairs):
    packets = list(chain(DIVIDER_PACKAGES, *pairs))
    packets = sorted(
        packets, key=cmp_to_key(lambda left, right: compare((left, right)))
    )
    indexes = []
    for i, packet in enumerate(packets):
        if packet in DIVIDER_PACKAGES:
            indexes.append(i + 1)
    return indexes[0] * indexes[1]


if __name__ == "__main__":
    with open(get_input_name(13, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(13, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
