#!/usr/bin/env python
import operator
from dataclasses import dataclass
from typing import Callable

from ibidem.advent_of_code.util import get_input_name

OPERATORS = {
    "L": operator.sub,
    "R": operator.add,
}


@dataclass
class Turn:
    op: Callable
    value: int


def load(fobj):
    turns = []
    for line in fobj:
        opcode, valuestr = line[0], line[1:]
        turns.append(Turn(OPERATORS.get(opcode), int(valuestr)))
    return turns


def part1(turns):
    dial = list(range(100))
    idx = 50
    password = 0
    for turn in turns:
        idx = turn.op(idx, turn.value) % 100
        if dial[idx] == 0:
            password += 1
    return password


def part2(turns):
    dial = list(range(100))
    idx = 50
    password = 0
    for turn in turns:
        for _ in range(turn.value):
            idx = turn.op(idx, 1) % 100
            if dial[idx] == 0:
                password += 1
    return password


if __name__ == "__main__":
    with open(get_input_name(1, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(1, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
