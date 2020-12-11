#!/usr/bin/env python

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Part2Stepper():
    def __init__(self, board):
        self.board = board
        self._directions = list(self._generate_directions())

    def step(self):
        b = self.board.copy()
        changed = 0
        for y in range(self.board.size_y):
            for x in range(self.board.size_x):
                v = self.board.get(x, y)
                if v == ".":
                    continue
                count_occupied = self._count_occupied(x, y)
                if v == "L":
                    if count_occupied == 0:
                        changed += 1
                        b.set(x, y, "#")
                elif v == "#":
                    if count_occupied >= 5:
                        changed += 1
                        b.set(x, y, "L")
        self.board = b
        return changed

    def _count_occupied(self, x, y):
        count_occupied = 0
        for dir in self._directions:
            seat = self._look((x, y), dir)
            if seat == "#":
                count_occupied += 1
        return count_occupied

    def _generate_directions(self):
        for j in (1, 0, -1):
            for i in (1, 0, -1):
                if i == j == 0:
                    continue
                yield i, j

    def _look(self, pos, dir):
        cur = np.array(pos)
        dv = np.array(dir)
        while True:
            cur += dv
            try:
                v = self.board.get(cur[0], cur[1])
                if v == ".":
                    continue
                return v
            except IndexError:
                return "."


def load():
    with open(get_input_name(11, 2020)) as fobj:
        return Board.from_string(fobj.read())


def step1(board):
    b = board.copy()
    for y in range(board.size_y):
        for x in range(board.size_x):
            v = board.get(x, y)
            adjacent = board.adjacent(x, y)
            if v == ".":
                continue
            elif v == "L":
                if "#" not in adjacent:
                    b.set(x, y, "#")
            elif v == "#":
                occupied = adjacent.count("#")
                if occupied >= 4:
                    b.set(x, y, "L")
    return b


def count(current, stepper):
    previous = None
    count = 0
    while current != previous:
        previous = current
        current = stepper(current)
        count += 1
    result = current.count("#")
    return result


def part1(board):
    result = count(board, step1)
    print(f"Part 1: After many steps, {result} seats are occupied")


def part2(board):
    stepper = Part2Stepper(board)
    changed = 1
    count = 0
    while changed > 0:
        changed = stepper.step()
        count += 1
    result = stepper.board.count("#")
    print(f"Part 2: After {count} steps, {result} seats are occupied")
    return result


if __name__ == "__main__":
    board = load()
    part1(board)
    part2(board)
