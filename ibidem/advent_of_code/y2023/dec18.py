#!/usr/bin/env python
import re
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, gen_list

INSTRUCTION_PATTERN = re.compile(r"([UDLR]) (\d+) \(#([0-9a-f]{6})\)")
CROSSINGS_CACHE = {}


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def delta(self):
        return Coordinate(self.dx, self.dy)

    @classmethod
    def from_first_char(cls, char):
        match char:
            case "U":
                return cls.UP
            case "L":
                return cls.LEFT
            case "R":
                return cls.RIGHT
            case "D":
                return cls.DOWN
            case _:
                raise ValueError(f"Invalid character {char!r}")


class Coordinate(namedtuple("Coordinate", ["x", "y"])):
    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)


@dataclass(eq=True, frozen=True)
class Instruction:
    direction: Direction
    distance: int


@gen_list
def load(fobj):
    for line in fobj:
        if m := INSTRUCTION_PATTERN.match(line.strip()):
            yield Instruction(Direction.from_first_char(m.group(1)), int(m.group(2)))


def is_inside(board, coord):
    return crossings(board, coord.x, coord.y) % 2 == 1


def crossings(board, x, y):
    if (x, y) in CROSSINGS_CACHE:
        return CROSSINGS_CACHE[(x, y)]
    if x < 0:
        value = 0
    elif board.get(x, y) == "#":
        if board.get(x - 1, y) == "#":  # We are on a horizontal line, so ignore this "crossing"
            value = crossings(board, x - 1, y)
        else:
            value = 1 + crossings(board, x - 1, y)
    else:
        value = crossings(board, x - 1, y)
    return CROSSINGS_CACHE.setdefault((x, y), value)


def find_inside(board, min, max):
    x = min.x + (max.x - min.x) // 2
    y = min.y + (max.y - min.y) // 2
    while not is_inside(board, Coordinate(x, y)):
        x += 1
        y += 1
    return Coordinate(x, y)


def fill_board(board, vis_board, start):
    seen = set()
    queue = [start]
    while queue:
        pos = queue.pop()
        seen.add(pos)
        for x, y in board.adjacent_indexes(pos.x, pos.y, True):
            if (x, y) in seen:
                continue
            if board.get(x, y) == "#":
                continue
            vis_board.set(x, y, "X")
            queue.append(Coordinate(x, y))


def part1(input):
    board = Board()
    pos = Coordinate(0, 0)
    max_x = max_y = 0
    min_x = min_y = 0
    board.set(pos.x, pos.y, "#")
    coords = [pos]
    for instruction in input:
        for _ in range(instruction.distance):
            pos = pos + instruction.direction.delta()
            board.set(pos.x, pos.y, "#")
            coords.append(pos)
            max_x, max_y = max(max_x, pos.x), max(max_y, pos.y)
            min_x, min_y = min(min_x, pos.x), min(min_y, pos.y)
    print("Board after dig plan")
    board.print()
    vis_board = board.copy()
    start = find_inside(board, Coordinate(min_x, min_y), Coordinate(max_x, max_y))
    vis_board.set(start.x, start.y, "X")
    fill_board(board, vis_board, start)
    print("Board after fill")
    vis_board.print()
    return vis_board.count("#") + vis_board.count("X")


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(18, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
