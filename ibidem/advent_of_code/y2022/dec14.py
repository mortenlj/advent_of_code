#!/usr/bin/env python
import enum
from itertools import pairwise

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

ENTRYPOINT = (500, 0)


class Location(enum.Enum):
    Occupied = enum.auto()
    Taken = enum.auto()
    Abyss = enum.auto()


def load(fobj):
    structures = []
    for line in fobj:
        structure = []
        for data in line.split(" -> "):
            coord = tuple(int(x) for x in data.split(","))
            structure.append(coord)
        structures.append(structure)
    return structures


def place_at(x, y, board, max_y):
    if y > max_y + 10:
        return Location.Abyss
    if board.get(x, y) == " ":
        if (location := place_at(x, y + 1, board, max_y)) != Location.Occupied:
            return location
        if (location := place_at(x - 1, y + 1, board, max_y)) != Location.Occupied:
            return location
        if (location := place_at(x + 1, y + 1, board, max_y)) != Location.Occupied:
            return location
        board.set(x, y, "o")
        return Location.Taken
    return Location.Occupied


def add_sand(board, max_y):
    x, y = ENTRYPOINT
    return place_at(x, y, board, max_y)


def setup_board(structures):
    board = Board(do_translate=False)
    max_y = 0
    # Draw structures on map
    for struct in structures:
        for pair in pairwise(struct):
            start, end = sorted(pair)
            for x in range(start[0], end[0] + 1):
                for y in range(start[1], end[1] + 1):
                    max_y = max(max_y, y)
                    board.set(x, y, "#")
    return board, max_y


def part1(structures):
    board, max_y = setup_board(structures)
    while add_sand(board, max_y) == Location.Taken:
        pass
    count = board.count("o")
    # For visualization
    board.set(500, 0, "+")
    for x in range(480, 520):
        board.set(x, max_y + 2, "~")
    print("=" * 60)
    board.print(include_empty=True, crop_to_bounds=True)
    print("=" * 60)
    return count


def part2(structures):
    board, max_y = setup_board(structures)

    def new_get(self, x, y):
        if y == max_y + 2:
            return "#"
        return self.old_get(x, y)

    Board.old_get = Board.get
    Board.get = new_get

    while add_sand(board, max_y) == Location.Taken:
        pass
    count = board.count("o")
    # For visualization
    board.set(500, 0, "+")
    for x in range(480, 520):
        board.set(x, max_y + 2, "~")
    print("=" * 60)
    board.print(include_empty=True, crop_to_bounds=True)
    print("=" * 60)
    return count


if __name__ == "__main__":
    with open(get_input_name(14, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
