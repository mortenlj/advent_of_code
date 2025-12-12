#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), fill_value=0, dtype=int, growable=False)


def adjacent_view(grid, x, y):
    x_min = max(x - 1, 0)
    y_min = max(y - 1, 0)
    x_max = min(x + 2, grid.shape[1])
    y_max = min(y + 2, grid.shape[0])
    return grid[(slice(y_min, y_max), slice(x_min, x_max))]


def simulate_step(board):
    board.grid += 1
    work = np.ma.asarray(board.grid)
    while (work > 9).any():
        should_flash = np.transpose(np.nonzero(work > 9))
        for y, x in should_flash:
            to_flash = adjacent_view(work, x, y)
            to_flash += 1
            work[y, x] = np.ma.masked
    board.grid[work.mask] = 0
    return board.count(0)


def part1(board):
    total_flashes = 0
    for step in range(100):
        total_flashes += simulate_step(board)
    return total_flashes


def part2(board):
    step = 0
    while board.count(0) < 100:
        step += 1
        simulate_step(board)
    return step


if __name__ == "__main__":
    with open(get_input_name(11, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
