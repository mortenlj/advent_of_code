#!/usr/bin/env python
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read())


def part1(board):
    beams = set()
    for x in range(board.size_x):
        if board.get(x, 0) == "S":
            beams.add(x)
            break
    splits = 0
    for y in range(1, board.size_y):
        new_beams = set()
        for beam in beams:
            if board.get(beam, y) == "^":
                splits += 1
                if beam > 0:
                    new_beams.add(beam - 1)
                if beam < board.size_x-1:
                    new_beams.add(beam + 1)
            else:
                new_beams.add(beam)
        beams = new_beams
    return splits


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(7, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
