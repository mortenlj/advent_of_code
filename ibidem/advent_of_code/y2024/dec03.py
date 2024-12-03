#!/usr/bin/env python
import re

from ibidem.advent_of_code.util import get_input_name

PART1_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
PART2_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def load(fobj):
    return fobj.read()


def part1(input):
    operations = PART1_PATTERN.findall(input)
    results = []
    for a, b in operations:
        print(f"{a} * {b} = {int(a) * int(b)}")
        results.append(int(a) * int(b))
    return sum(results)


def part2(input):
    results = []
    enabled = True
    for match in PART2_PATTERN.finditer(input):
        if match.group(0).startswith("mul"):
            if not enabled:
                continue
            a, b = match.groups()
            print(f"{a} * {b} = {int(a) * int(b)}")
            results.append(int(a) * int(b))
        elif match.group(0) == "don't()":
            enabled = False
        elif match.group(0) == "do()":
            enabled = True
    return sum(results)


if __name__ == "__main__":
    with open(get_input_name(3, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(3, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
