#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


class Case:
    def __init__(self, line):
        signal_patterns, digit_outputs = line.split("|")
        self.signal_patterns = signal_patterns.strip().split()
        self.digit_outputs = digit_outputs.strip().split()


def load(fobj):
    for line in fobj:
        yield Case(line)


def part1(input):
    counts = 0
    for case in input:
        for output in case.digit_outputs:
            if len(output) in {2, 3, 4, 7}:
                counts += 1
    return counts


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(8, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
