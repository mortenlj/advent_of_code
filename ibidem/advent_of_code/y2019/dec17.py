#!/usr/bin/env python
# -*- coding: utf-8

try:
    from .board import Board
    from .intcode import load_program, IntCode, Disassembler
except ModuleNotFoundError:
    from board import Board
    from intcode import load_program, IntCode, Disassembler


def capture_camera(intcode):
    chars = []
    intcode.execute(output_func=chars.append)
    board = Board.from_string("".join(chr(c) for c in chars))
    return board


def _get_neighbours(x, y, board):
    result = []
    for dx in (-1, 1):
        try:
            result.append(board.get(x + dx, y))
        except IndexError:
            pass
    for dy in (-1, 1):
        try:
            result.append(board.get(x, y + dy))
        except IndexError:
            pass
    return result


def get_intersections(board):
    for y, row in enumerate(board.grid):
        for x, c in enumerate(row):
            if c == "#":
                neighbours = _get_neighbours(x, y, board)
                if neighbours.count("#") > 2:
                    yield x, y


def calculate_alignments(intersections):
    return sum(x*y for x, y in intersections)


def part1():
    program = load_program("dec17")
    intcode = IntCode(program)
    board = capture_camera(intcode)
    board.print()
    intersections = get_intersections(board)
    alignments = calculate_alignments(intersections)
    print("The sum of alignments is {}".format(alignments))


if __name__ == "__main__":
    part1()
