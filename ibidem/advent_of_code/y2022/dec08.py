#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), fill_value=0, dtype=int)


def part1(input):
    visible = Board(input.size_x, input.size_y, do_translate=False, flip=True)
    grid = input.grid
    for rotation in range(4):
        for y, row in enumerate(grid):
            max_height = -1
            for x, tree in enumerate(row):
                if tree > max_height:
                    visible.set(x, y, "X")
                    max_height = tree
        grid = np.rot90(grid)
        visible.grid = np.rot90(visible.grid)
    return visible.count("X")


def _calculate_view_distance(tree, x, y, input):
    if x == 0:
        return 0
    distance = 0
    for offset in range(1, x + 1):
        distance += 1
        other_tree = input.get(x - offset, y)
        if other_tree >= tree:
            return distance
    return distance


def part2(input):
    scenic_score = Board(
        input.size_x,
        input.size_y,
        do_translate=False,
        flip=True,
        fill_value=1,
        dtype=int,
    )
    for rotation in range(4):
        view_distance = Board(
            input.size_x,
            input.size_y,
            do_translate=False,
            flip=True,
            fill_value=0,
            dtype=int,
        )
        for y, row in enumerate(input.grid):
            for x, tree in enumerate(row):
                view = _calculate_view_distance(tree, x, y, input)
                view_distance.set(x, y, view)
        scenic_score.grid *= view_distance.grid
        input.grid = np.rot90(input.grid)
        scenic_score.grid = np.rot90(scenic_score.grid)
    return scenic_score.grid.max()


if __name__ == "__main__":
    with open(get_input_name(8, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
