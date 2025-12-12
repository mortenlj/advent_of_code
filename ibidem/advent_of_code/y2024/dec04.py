#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

PART1_NEEDLE = list("XMAS")
PART2_NEEDLE = np.array([["M", "*", "M"], ["*", "A", "*"], ["S", "*", "S"]])
PART2_MATCH_IDX = [(0, 0, 1, 2, 2), (0, 2, 1, 0, 2)]


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def part1(input):
    count = 0
    values = input.grid
    for _ in range(4):
        count = count_one_dir(count, values)
        count = count_diag(count, values)
        values = np.rot90(values)
    return count


def count_one_dir(count, values):
    for i in range(len(values)):
        for k in range(len(values[i]) - len(PART1_NEEDLE) + 1):
            if np.all(values[i][k : k + len(PART1_NEEDLE)] == PART1_NEEDLE):
                count += 1
    return count


def count_diag(count, values):
    for i in range(
        -len(values) + len(PART1_NEEDLE), len(values) - len(PART1_NEEDLE) + 1
    ):
        d = np.diag(values, k=i)
        count = count_one_diag(count, d)
    return count


def count_one_diag(count, diag):
    for k in range(len(diag) - len(PART1_NEEDLE) + 1):
        if np.all(diag[k : k + len(PART1_NEEDLE)] == PART1_NEEDLE):
            count += 1
    return count


def part2(input):
    count = 0
    values = input.grid
    for _ in range(4):
        count = count_one_dir_part2(count, values)
        values = np.rot90(values)
    return count


def count_one_dir_part2(count, values):
    for i in range(len(values) - len(PART2_NEEDLE) + 1):
        for k in range(len(values[i]) - len(PART2_NEEDLE[0]) + 1):
            grid = values[i : i + len(PART2_NEEDLE), k : k + len(PART2_NEEDLE[0])]
            match = [tuple(v) for v in np.where(grid == PART2_NEEDLE)]
            if match == PART2_MATCH_IDX:
                count += 1
    return count


if __name__ == "__main__":
    with open(get_input_name(4, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(4, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
