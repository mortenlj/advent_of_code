#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


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


def part2(board):
    # oxygen generator rating
    grid = board.grid
    candidates, bit_fields = grid.shape
    cur_field = 0
    while candidates > 1:
        summed = np.sum(grid, axis=0)
        if summed[cur_field] >= (candidates / 2):
            grid = np.delete(grid, grid[:, cur_field] == 0, axis=0)
        else:
            grid = np.delete(grid, grid[:, cur_field] == 1, axis=0)
        candidates = grid.shape[0]
        cur_field += 1
        if cur_field > bit_fields:
            raise RuntimeError("Too many candidates")
    oxy_rating = to_decimal(grid[0])
    print(oxy_rating)
    # CO2 scrubber rating
    grid = board.grid
    candidates, bit_fields = grid.shape
    cur_field = 0
    while candidates > 1:
        summed = np.sum(grid, axis=0)
        if summed[cur_field] >= (candidates / 2):
            grid = np.delete(grid, grid[:, cur_field] == 1, axis=0)
        else:
            grid = np.delete(grid, grid[:, cur_field] == 0, axis=0)
        candidates = grid.shape[0]
        cur_field += 1
        if cur_field > bit_fields:
            raise RuntimeError("Too many candidates")
    co2_rating = to_decimal(grid[0])
    print(co2_rating)
    return oxy_rating * co2_rating


if __name__ == "__main__":
    board = load()
    p1_result = part1(board)
    print(f"Part 1: {p1_result}")
    p2_result = part2(board)
    print(f"Part 2: {p2_result}")
