#!/usr/bin/env python

import re
from collections import namedtuple

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

Pos = namedtuple("Pos", ("x", "y"))


class Line:
    _PATTERN = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
    start: Pos
    end: Pos

    def __init__(self, line):
        m = self._PATTERN.match(line)
        if not m:
            raise RuntimeError("Invalid line: %r" % line)
        self.start = Pos(int(m.group(1)), int(m.group(2)))
        self.end = Pos(int(m.group(3)), int(m.group(4)))

    def points(self):
        y_start = min(self.start.y, self.end.y)
        y_end = max(self.start.y, self.end.y)
        x_start = min(self.start.x, self.end.x)
        x_end = max(self.start.x, self.end.x)
        for y in range(y_start, y_end + 1):
            for x in range(x_start, x_end + 1):
                yield Pos(x, y)

    def __repr__(self):
        return f"Line({self.start}, {self.end})"


class DiagonalLine(Line):
    def points(self):
        x_step = 1 if self.start.x <= self.end.x else -1
        y_step = 1 if self.start.y <= self.end.y else -1
        cur = Pos(self.start.x, self.start.y)
        yield cur
        while cur.x != self.end.x and cur.y != self.end.y:
            cur = Pos(cur.x + x_step, cur.y + y_step)
            yield cur


def load(with_diagonal):
    with open(get_input_name(5, 2021)) as fobj:
        return list(_load_input(fobj, with_diagonal))


def _load_input(fobj, with_diagonal):
    for s in fobj:
        line = Line(s)
        if line.start.x == line.end.x or line.start.y == line.end.y:
            yield line
        elif with_diagonal:
            yield DiagonalLine(s)


def part1(lines=None):
    if lines is None:
        lines = load(with_diagonal=False)
    return solve(lines)


def solve(lines):
    board = Board(do_translate=False, fill_value=0, dtype=np.int_)
    for line in lines:
        for point in line.points():
            cur = board.get(point.x, point.y)
            board.set(point.x, point.y, cur + 1)
    return np.sum(board.grid >= 2)


def part2(lines=None):
    if lines is None:
        lines = load(with_diagonal=True)
    return solve(lines)


if __name__ == "__main__":
    p1_result = part1()
    print(f"Part 1: {p1_result}")
    p2_result = part2()
    print(f"Part 2: {p2_result}")
