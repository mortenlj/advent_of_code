#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return [int(v.strip()) for v in fobj if v.strip()]


def mix(sn, value):
    return sn ^ value


def prune(value):
    return value % 16777216


def next_secret_number(sn):
    sn = prune(mix(sn, sn * 64))
    sn = prune(mix(sn, sn // 32))
    sn = prune(mix(sn, sn * 2048))
    return sn


def part1(secret_numbers: list[int]):
    new_numbers = []
    for sn in secret_numbers:
        for i in range(2000):
            sn = next_secret_number(sn)
        new_numbers.append(sn)

    return sum(new_numbers)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(22, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(22, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
