#!/usr/bin/env python
from collections import namedtuple

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


Point = namedtuple('Point', 'x y')


def load(fobj):
    return Board.from_string(fobj.read())


def find_start(board):
    for y in range(board.size_y):
        for x in range(board.size_x):
            if board.get(x, y) == "S":
                return Point(x, y)


def move(board, pos, prev):
    """Use current and previous position to determine next position."""
    c = board.get(pos.x, pos.y)
    if c == "-":
        return [Point(pos.x + 1, pos.y), Point(pos.x - 1, pos.y)][pos.x + 1 == prev.x]
    if c == "|":
        return [Point(pos.x, pos.y + 1), Point(pos.x, pos.y - 1)][pos.y + 1 == prev.y]
    if c == "L":
        return [Point(pos.x + 1, pos.y), Point(pos.x, pos.y - 1)][pos.x != prev.x]
    if c == "J":
        return [Point(pos.x - 1, pos.y), Point(pos.x, pos.y - 1)][pos.x != prev.x]
    if c == "7":
        return [Point(pos.x - 1, pos.y), Point(pos.x, pos.y + 1)][pos.x != prev.x]
    if c == "F":
        return [Point(pos.x + 1, pos.y), Point(pos.x, pos.y + 1)][pos.x != prev.x]
    raise ValueError(f"I shouldn't be here: {pos} {c}")


def part1(input: Board):
    start = find_start(input)
    candidates = []
    for x, y in input.adjacent_indexes(start.x, start.y, False):
        c = input.get(x, y)
        if c == "-" and start.x != x:
            candidates.append(Point(x, y))
        elif c == "|" and start.y != y:
            candidates.append(Point(x, y))
        elif c == "L" and (start.x == x + 1 or start.y == y + 1):
            candidates.append(Point(x, y))
        elif c == "J" and (start.x == x - 1 or start.y == y + 1):
            candidates.append(Point(x, y))
        elif c == "7" and (start.x == x - 1 or start.y == y - 1):
            candidates.append(Point(x, y))
        elif c == "F" and (start.x == x + 1 or start.y == y - 1):
            candidates.append(Point(x, y))
    assert len(candidates) == 2
    a, b = candidates
    steps = 1
    prev_a = start
    prev_b = start
    while a != b:
        prev_a, a = a, move(input, a, prev_a)
        prev_b, b = b, move(input, b, prev_b)
        steps += 1
    return steps


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(10, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
