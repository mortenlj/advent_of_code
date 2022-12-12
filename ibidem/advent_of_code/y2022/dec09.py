#!/usr/bin/env python
import enum
import re

import vectormath

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

PATTERN = re.compile(r"([RUDL]) (\d+)")


class Moves(enum.Enum):
    def __new__(cls, value, change):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.change = change
        return obj

    Right = ("R", vectormath.Vector2(1, 0))
    Left = ("L", vectormath.Vector2(-1, 0))
    Up = ("U", vectormath.Vector2(0, 1))
    Down = ("D", vectormath.Vector2(0, -1))

    Stay = ("S", vectormath.Vector2(0, 0))
    UpRight = ("7", vectormath.Vector2(1, 1))
    UpLeft = ("F", vectormath.Vector2(-1, 1))
    DownRight = ("J", vectormath.Vector2(1, -1))
    DownLeft = ("Z", vectormath.Vector2(-1, -1))


def load(fobj):
    for line in fobj:
        if m := PATTERN.match(line.strip()):
            for _ in range(int(m.group(2))):
                yield m.group(1)


def calculate_tail_move(tail, head):
    offset = head - tail
    match tuple(offset):
        case (0., 2.):
            return Moves.Up
        case (0., -2.):
            return Moves.Down
        case (2., 0.):
            return Moves.Right
        case (-2., 0.):
            return Moves.Left
        case (1., 2.) | (2., 1.):
            return Moves.UpRight
        case (-1., 2.) | (-2., 1.):
            return Moves.UpLeft
        case (1., -2.) | (2., -1.):
            return Moves.DownRight
        case (-1., -2.) | (-2., -1.):
            return Moves.DownLeft
    return Moves.Stay


def part1(steps):
    visited = Board(size_x=14, size_y=10, fill_value=".")
    head = vectormath.Vector2(0, 0)
    tail = vectormath.Vector2(0, 0)
    for step in steps:
        move = Moves(step)
        head += move.change
        tail_move = calculate_tail_move(tail, head)
        tail += tail_move.change

        old_head = visited.set(int(head.x), int(head.y), "H")
        visited.set(int(tail.x), int(tail.y), "T")
        # visited.print(include_empty=True)
        # print("-"*40)
        visited.set(int(head.x), int(head.y), old_head)
        visited.set(int(tail.x), int(tail.y), "#")
    return visited.count("#")


def part2(steps):
    return None


if __name__ == "__main__":
    with open(get_input_name(9, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
