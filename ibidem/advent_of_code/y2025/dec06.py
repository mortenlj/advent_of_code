#!/usr/bin/env python
import itertools
from math import prod

from ibidem.advent_of_code.util import get_input_name, gen_list

OPERATORS = {
    "*": prod,
    "+": sum,
}


@gen_list
def load1(fobj):
    for line in fobj:
        if "*" in line or "+" in line:
            yield [c for c in line.strip().split()]
        else:
            yield [int(c) for c in line.strip().split()]


def part1(input):
    problem_values = [list(t) for t in itertools.zip_longest(*input[:-1])]
    grand_total = 0
    for i, op_char in enumerate(input[-1]):
        op = OPERATORS[op_char]
        values = problem_values[i]
        result = op(values)
        grand_total += result
    return grand_total


def load2(fobj):
    lines = fobj.read().splitlines()
    problem_lines = ["".join(t) for t in zip(*lines)]
    problems = []
    values = []
    op = None
    for line in problem_lines:
        if not line.strip():
            problems.append((op, values))
            values = []
            op = None
            continue
        if line.endswith("+"):
            op = sum
            value = line[:-1]
        elif line.endswith("*"):
            op = prod
            value = line[:-1]
        else:
            value = line
        values.append(int(value))
    if op:
        problems.append((op, values))
    return problems


def part2(problems):
    grand_total = 0
    for op, values in problems:
        grand_total += op(values)
    return grand_total


if __name__ == "__main__":
    with open(get_input_name(6, 2025)) as fobj:
        p1_result = part1(load1(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2025)) as fobj:
        p2_result = part2(load2(fobj))
        print(f"Part 2: {p2_result}")
