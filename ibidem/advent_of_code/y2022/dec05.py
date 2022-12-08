#!/usr/bin/env python
import dataclasses
import re
from collections import deque

from ibidem.advent_of_code.util import get_input_name


@dataclasses.dataclass
class Move:
    count: int
    source: int
    target: int

    PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")

    def __init__(self, line):
        if m := self.PATTERN.match(line):
            self.count = int(m.group(1))
            self.source = int(m.group(2))
            self.target = int(m.group(3))
        else:
            raise ValueError(f"{line} is not a valid Move")


@dataclasses.dataclass
class Input:
    moves: list[Move]
    stacks: list[deque]

    def top(self):
        top_of_stacks = []
        for stack in self.stacks:
            top_of_stacks.append(stack[-1])
        return "".join(top_of_stacks)


def load_moves(fobj):
    for line in fobj:
        if not line.strip():
            continue
        yield Move(line)


def load_stacks(fobj):
    rows = []
    num_stacks = 0
    for line in fobj:
        if line.strip().startswith("1"):
            num_stacks = len(line.split())
            max_index = num_stacks * 4
            break
        rows.append(line)
    stacks = [deque() for _ in range(num_stacks)]
    for stacknum, index in enumerate(range(1, max_index + 1, 4)):
        for row in reversed(rows):
            if row[index] != " ":
                stacks[stacknum].append(row[index])
    return stacks


def load(fobj) -> Input:
    stacks = load_stacks(fobj)
    moves = list(load_moves(fobj))
    return Input(moves, stacks)


def part1(input):
    for move in input.moves:
        source = input.stacks[move.source - 1]
        target = input.stacks[move.target - 1]
        for _ in range(move.count):
            target.append(source.pop())
    return input.top()


def part2(input):
    for move in input.moves:
        source = input.stacks[move.source - 1]
        target = input.stacks[move.target - 1]
        to_move = []
        for _ in range(move.count):
            to_move.append(source.pop())
        target.extend(reversed(to_move))
    return input.top()


if __name__ == "__main__":
    with open(get_input_name(5, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(5, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
