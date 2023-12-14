#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read())


def tilt_column(column):
    insert_at = 0
    for i, c in enumerate(column):
        if c == ".":
            continue
        if c == "#":
            insert_at = i + 1
        if c == "O":
            column[i] = "."
            column[insert_at] = "O"
            insert_at += 1
    return column


def calculate_load(column):
    total_load = 0
    for i, c in enumerate(reversed(column)):
        if c == "O":
            total_load += i + 1
    return total_load


def part1(input: Board):
    result = 0
    for x in range(input.size_x):
        column = input.grid[:, x]
        new_column = tilt_column(column)
        total_load = calculate_load(new_column)
        result += total_load
    return result


def run_cycle(grid):
    for direction in ("N", "W", "S", "E"):
        new_grid = grid.copy()
        for x in range(grid.shape[1]):
            column = grid[:, x]
            new_column = tilt_column(column)
            new_grid[:, x] = new_column
        grid = np.rot90(new_grid, k=-1, axes=(0, 1))
    return grid


def part2(board):
    grid = board.grid
    configurations = {}
    for i in range(1, 1_000_000_001):
        grid = run_cycle(grid)
        last_seen = configurations.get(grid.tobytes())
        if last_seen is not None:
            if (1_000_000_000 - i) % (i - last_seen) == 0:
                break
        configurations[grid.tobytes()] = i
    result = 0
    for x in range(grid.shape[1]):
        column = grid[:, x]
        total_load = calculate_load(column)
        result += total_load
    return result


if __name__ == "__main__":
    with open(get_input_name(14, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
