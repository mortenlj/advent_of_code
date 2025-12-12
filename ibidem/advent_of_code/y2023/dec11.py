#!/usr/bin/env python
import itertools
from collections import namedtuple

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Coordinate(namedtuple("Coordinate", ["x", "y"])):
    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def manhattan(self):
        return abs(self.x) + abs(self.y)


def load(fobj):
    return Board.from_string(fobj.read())


def part1(input):
    board = expand(input)
    galaxies = []
    for y in range(board.size_y):
        for x in range(board.size_x):
            if board.get(x, y) == "#":
                galaxies.append(Coordinate(x, y))
    distances = []
    for a, b in itertools.combinations(galaxies, 2):
        distances.append((a - b).manhattan())
    return sum(distances)


def part2(input, expand):
    board = input
    cols, rows = find_empty(board)
    galaxies = []
    for y in range(board.size_y):
        for x in range(board.size_x):
            if board.get(x, y) == "#":
                galaxies.append(Coordinate(x, y))
    distances = []
    for a, b in itertools.combinations(galaxies, 2):
        distance = (a - b).manhattan()
        for col in cols:
            if a.x < col < b.x or b.x < col < a.x:
                distance += expand - 1
        for row in rows:
            if a.y < row < b.y or b.y < row < a.y:
                distance += expand - 1
        distances.append(distance)
    return sum(distances)


def expand(board: Board) -> Board:
    cols, rows = find_empty(board)
    new_board = board.copy()
    for y in reversed(rows):
        new_board.grid = np.insert(new_board.grid, y, ["."], axis=0)
    for x in reversed(cols):
        new_board.grid = np.insert(new_board.grid, x, ["."], axis=1)
    return new_board


def find_empty(board):
    rows = []
    for y in range(board.size_y):
        if all(board.get(x, y) == "." for x in range(board.size_x)):
            rows.append(y)
    cols = []
    for x in range(board.size_x):
        if all(board.get(x, y) == "." for y in range(board.size_y)):
            cols.append(x)
    return cols, rows


if __name__ == "__main__":
    with open(get_input_name(11, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2023)) as fobj:
        p2_result = part2(load(fobj), 1000000)
        print(f"Part 2: {p2_result}")
