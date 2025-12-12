#!/usr/bin/env python

import re
from collections import namedtuple

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

FOLD_PATTERN = re.compile(r"fold along ([xy])=(\d+)")

Fold = namedtuple("Fold", ("axis", "idx"))
Point = namedtuple("Point", ("x", "y"))


def fold(line):
    m = FOLD_PATTERN.match(line.strip())
    return Fold(0 if m.group(1) == "y" else 1, int(m.group(2)))


def point(line):
    return Point(*(int(v) for v in line.strip().split(",")))


def load(fobj):
    points = []
    folds = []
    x_max = y_max = 0
    board = None
    for line in fobj:
        if not line.strip():
            board = Board(
                x_max + 1,
                y_max + 1,
                do_translate=False,
                fill_value=0,
                dtype=int,
                growable=False,
            )
            continue
        if board:
            folds.append(fold(line))
        else:
            p = point(line)
            x_max = max(x_max, p.x)
            y_max = max(y_max, p.y)
            points.append(p)
    for p in points:
        board.set(p.x, p.y, 1)
    return board, folds


def part1(board, folds):
    grid = board.grid
    fold = folds[0]
    a, _, b = np.split(grid, [fold.idx, fold.idx + 1], axis=fold.axis)
    grid = a + np.flip(b, axis=fold.axis)
    return (grid > 0).sum()


def part2(board, folds):
    grid = board.grid
    for fold in folds:
        a, _, b = np.split(grid, [fold.idx, fold.idx + 1], axis=fold.axis)
        grid = a + np.flip(b, axis=fold.axis)
    lines = []
    for row in grid:
        lines.append("".join(" " if v == 0 else "#" for v in row))
    output = "\n".join(lines)
    return output


if __name__ == "__main__":
    with open(get_input_name(13, 2021)) as fobj:
        p1_result = part1(*load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(13, 2021)) as fobj:
        p2_result = part2(*load(fobj))
        print(f"Part 2: \n{p2_result}")
