#!/usr/bin/env python
import operator
import re

from ibidem.advent_of_code.util import get_input_name

VALUE_PATTERN = re.compile(r"([a-z]+): (\d+)")
EXPR_PATTERN = re.compile(r"([a-z]+): ([a-z]+) ([-+*/]) ([a-z]+)")


class Monkey:
    def __init__(self, name):
        self.name = name


class ValueMonkey(Monkey):

    def __init__(self, name, value):
        super().__init__(name)
        self._value = value

    def value(self, _) -> int:
        return self._value


class ExpressionMonkey(Monkey):

    def __init__(self, name, left_name, right_name, op):
        super().__init__(name)
        self.left_name = left_name
        self.right_name = right_name
        self.op = op

    def value(self, monkies: dict[Monkey]) -> int:
        left = monkies[self.left_name]
        right = monkies[self.right_name]
        return self.op(left.value(monkies), right.value(monkies))


def op(p):
    return {
        "-": operator.sub,
        "+": operator.add,
        "*": operator.mul,
        "/": operator.floordiv,
    }[p]


def load(fobj):
    monkies = {}
    for line in fobj:
        if m := VALUE_PATTERN.search(line):
            monkies[m.group(1)] = ValueMonkey(m.group(1), int(m.group(2)))
        if m := EXPR_PATTERN.search(line):
            monkies[m.group(1)] = ExpressionMonkey(m.group(1), m.group(2), m.group(4), op(m.group(3)))
    return monkies


def part1(monkies):
    return monkies["root"].value(monkies)


def part2(monkies):
    return None


if __name__ == "__main__":
    with open(get_input_name(21, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(21, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
