#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    elves = []
    current_elf = []
    for line in fobj:
        if not line.strip():
            elves.append(current_elf)
            current_elf = []
            continue
        current_elf.append(int(line.strip()))
    if current_elf:
        elves.append(current_elf)
    return elves


def part1(elves):
    max_calories = 0
    for elf in elves:
        max_calories = max(max_calories, sum(elf))
    return max_calories


def part2(elves):
    calories = list(reversed(sorted(sum(elf) for elf in elves)))
    return sum(calories[:3])


if __name__ == "__main__":
    with open(get_input_name(1, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(1, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
