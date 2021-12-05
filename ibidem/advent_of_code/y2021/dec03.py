#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.util import get_input_name
from ibidem.advent_of_code.board import Board


def load():
    with open(get_input_name(3, 2021)) as fobj:
        return Board.from_string(fobj.read(), fill_value=0, dtype=np.int_)


def to_decimal(grid):
    bin = "".join(str(v) for v in np.int_(grid))
    return int(bin, 2)


def part1(board):
    mid = board.size_y / 2
    summed = np.sum(board.grid, axis=0)
    gamma = to_decimal(summed > mid)
    epsilon = to_decimal(summed < mid)
    return gamma * epsilon


def part2():
    return None

    
if __name__ == "__main__":
    board = load()
    p1_result = part1(board)
    print(f"Part 1: {p1_result}")
    p2_result = part2()
    print(f"Part 2: {p2_result}")
