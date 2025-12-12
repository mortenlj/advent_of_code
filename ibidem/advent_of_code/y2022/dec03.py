#!/usr/bin/env python
from itertools import zip_longest

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return fobj.read()


def priority(item):
    if item.islower():
        return ord(item) - ord("a") + 1
    return ord(item) - ord("A") + 27


def part1(input):
    result = 0
    for line in clean_lines(input):
        midway = int(len(line) / 2)
        print(f"midway is: {midway}")
        first = line[:midway]
        second = line[midway:]
        print(f"first: {first}")
        print(f"secnd: {second}")
        diff = set(first).intersection(set(second)).pop()
        print(f"odd one out: {diff}")
        prio = priority(diff)
        print(f"prio is {prio}")
        result += prio
    return result


def clean_lines(input):
    for line in input.splitlines():
        line = line.strip()
        if line:
            yield line


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


def part2(input):
    result = 0
    for group in grouper(clean_lines(input), 3):
        group = list(group)
        common = set(group.pop())
        for line in group:
            common = common.intersection(line)
        result += priority(common.pop())
    return result


if __name__ == "__main__":
    with open(get_input_name(3, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(3, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
