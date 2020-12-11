#!/usr/bin/env python

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(11, 2020)) as fobj:
        return Board.from_string(fobj.read())


def step(board):
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


def part1(current):
    previous = None
    count = 0
    while current != previous:
        previous = current
        current = step(current)
        count += 1
    result = current.count("#")
    print(f"After {count} steps, {result} seats are occupied")
    return result


def part2():
    pass


if __name__ == "__main__":
    board = load()
    part1(board)
    part2()
