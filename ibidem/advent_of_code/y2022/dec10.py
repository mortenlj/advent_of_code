#!/usr/bin/env python
import re

from ibidem.advent_of_code.util import get_input_name

ADDX_PAT = re.compile(r"addx (-?\d+)")


def load(fobj):
    for line in fobj:
        line = line.strip()
        if line == "noop":
            yield 0
        if m := ADDX_PAT.match(line):
            yield 0
            yield int(m.group(1))


def part1(operations):
    x = 1
    signal_sum = 0
    for i, change in enumerate(operations):
        cycle = i + 1
        if cycle in (20, 60, 100, 140, 180, 220):
            signal_strength = cycle * x
            print(f"Signal strength at cycle {cycle}: {signal_strength}")
            signal_sum += signal_strength
        x += change
    return signal_sum


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(10, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
