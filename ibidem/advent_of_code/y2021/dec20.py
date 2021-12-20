#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    algo_str = fobj.readline().strip()
    fobj.readline()
    board = Board.from_string(fobj.read(), fill_value=".")
    board.grid = np.pad(board.grid, ((9, 9), (9, 9)), mode="constant", constant_values=".")
    return algo_str, board


def pad(view, x, y, parent):
    if view.shape == (3, 3):
        return view
    left_pad = 1 if x == 0 else 0
    right_pad = 1 if x == parent.shape[1] - 1 else 0
    top_pad = 1 if y == 0 else 0
    bottom_pad = 1 if y == parent.shape[0] - 1 else 0
    padded = np.pad(view, ((top_pad, bottom_pad), (left_pad, right_pad)), mode="constant", constant_values=".")
    assert padded.shape == (3, 3)
    return padded


def part1(algo, board):
    size_x, size_y = board.size_x, board.size_y
    for i in range(2):
        enhance(algo, board, size_x, size_y)
        print(f"After {i + 1} steps:")
        board.print(include_empty=True)
    return board.count("#")


def enhance(algo, board, size_x, size_y):
    grid = np.zeros_like(board.grid)
    for x in range(size_x):
        for y in range(size_y):
            view = board.adjacent_view(x, y)
            if view.shape != (3, 3):
                view = pad(view, x, y, board.grid)
            g = view.flatten()
            b = g == "#"
            idx = int("".join("1" if v else "0" for v in b), 2)
            grid[y, x] = algo[idx]
    board.grid = grid


def part2(algo, board):
    board.grid = np.pad(board.grid, ((200, 200), (200, 200)), mode="constant", constant_values=".")
    size_x, size_y = board.size_x, board.size_y
    for i in range(50):
        enhance(algo, board, size_x, size_y)
        print(f"After {i + 1} steps:")
        board.print(include_empty=True)
    # Cut away the outer edges where we find weird artifacts that shouldn't be there.
    board.grid = board.grid[50:-50, 50:-50]
    return board.count("#")


if __name__ == "__main__":
    with open(get_input_name(20, 2021)) as fobj:
        p1_result = part1(*load(fobj))
        print(f"Part 1: {p1_result}")
        print(
            "Three corners are wrong on some inputs, but \"obvious\" in the printout, so subtract 3 when that happens")
    with open(get_input_name(20, 2021)) as fobj:
        p2_result = part2(*load(fobj))
        print(f"Part 2: {p2_result}")
