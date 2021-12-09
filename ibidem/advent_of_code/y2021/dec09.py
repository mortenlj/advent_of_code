#!/usr/bin/env python
import operator
from functools import reduce

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), fill_value=0, dtype=int, growable=False)


def part1(board):
    risk = 0
    low_points = []
    for x in range(board.size_x):
        for y in range(board.size_y):
            value = board.get(x, y)
            adjacent = board.adjacent(x, y, include_diagonal=False)
            if all(value < v for v in adjacent):
                risk += (value + 1)
                low_points.append((x, y))
    return risk, low_points


def find_basin(board, low_point):
    size = 1
    visited = {low_point}
    adjacent = set(board.adjacent_indexes(*low_point, include_diagonal=False))
    while adjacent:
        next = adjacent.pop()
        if next in visited:
            continue
        visited.add(next)
        value = board.get(*next)
        if value < 9:
            size += 1
            adjacent.update(board.adjacent_indexes(*next, include_diagonal=False))
    return size


def part2(board, low_points):
    basins = []
    for lp in low_points:
        basins.append(find_basin(board, lp))
    largest = sorted(basins, reverse=True)[:3]
    return reduce(operator.mul, largest)


if __name__ == "__main__":
    with open(get_input_name(9, 2021)) as fobj:
        p1_result, low_points = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2021)) as fobj:
        p2_result = part2(load(fobj), low_points)
        print(f"Part 2: {p2_result}")
