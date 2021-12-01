#!/usr/bin/env python

from itertools import tee

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(1, 2021)) as fobj:
        for line in fobj:
            yield int(line)


def part1():
    last = 99999999999
    count = 0
    for depth in load():
        if depth > last:
            count += 1
        last = depth
    print(f"{count} measurements increased")


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def triplewise_sum(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield sum((a, b, c))


def part2():
    last = 99999999999
    count = 0
    for window in triplewise_sum(load()):
        if window > last:
            count += 1
        last = window
    print(f"{count} measurements increased")


if __name__ == "__main__":
    part1()
    part2()
