#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name

NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def load(fobj):
    for line in fobj:
        yield line.strip()


def part1(input):
    calibrations = []
    for line in input:
        first, last = None, None
        for c in line:
            if c.isdigit():
                if first is None:
                    first = c
                last = c
        calibrations.append(int(first + last))
    return sum(calibrations)


def parse_line(line):
    for i, c in enumerate(line):
        if c.isdigit():
            yield c
        else:
            word = line[:i + 1]
            for number in NUMBERS.keys():
                if word.endswith(number):
                    yield NUMBERS[number]
                    break


def part2(input):
    calibrations = []
    for line in input:
        first, last = None, None
        for digit in parse_line(line):
            if first is None:
                first = digit
            last = digit
        calibrations.append(int(first + last))
    return sum(calibrations)


if __name__ == "__main__":
    with open(get_input_name(1, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(1, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
