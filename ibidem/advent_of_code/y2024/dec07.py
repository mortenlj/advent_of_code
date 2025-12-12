#!/usr/bin/env python
import operator

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    result = []
    for line in fobj:
        target, rest = line.strip().split(":")
        result.append((int(target), [int(v) for v in rest.split()]))
    return result


def is_valid(target, current, values, operators):
    if current > target:
        return False
    if not values:
        if current == target:
            return True
        return False
    head, tail = values[0], values[1:]
    for op in operators:
        if is_valid(target, op(current, head), tail, operators):
            return True
    return False


def part1(input):
    result = 0
    for target, values in input:
        if is_valid(target, values[0], values[1:], [operator.add, operator.mul]):
            result += target
    return result


def concat(a, b):
    return int(f"{a}{b}")


def part2(input):
    result = 0
    for target, values in input:
        if is_valid(
            target, values[0], values[1:], [operator.add, operator.mul, concat]
        ):
            result += target
    return result


if __name__ == "__main__":
    with open(get_input_name(7, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
