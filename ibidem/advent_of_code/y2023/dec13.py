#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, gen_list


@gen_list
def load(fobj):
    current = []
    for line in fobj:
        line = line.strip()
        if line:
            current.append(line)
        else:
            yield Board.from_string("\n".join(current))
            current = []
    yield Board.from_string("\n".join(current))


def find_mirror(grid):
    """For each column, take all columns up to it and compare to flipped version of same shape on other side."""
    length = grid.shape[1]
    for c in range(1, length):
        width = c if c < length / 2 else length - c
        left = grid[:, c - width : c]
        right = grid[:, c : c + width]
        right_flipped = np.fliplr(right)
        if np.array_equal(left, right_flipped):
            return c
    return 0


def part1(input):
    result = 0
    for board in input:
        columns = find_mirror(board.grid)
        result += columns
        rows = find_mirror(np.rot90(board.grid))
        result += 100 * rows
    return result


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(13, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(13, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
