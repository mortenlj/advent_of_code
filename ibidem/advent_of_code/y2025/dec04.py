#!/usr/bin/env python

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def part1(board: Board):
    return solve(board, 1)


def solve(board: Board, max_iterations: int):
    movable = []
    for _ in range(max_iterations):
        for x in range(board.size_x):
            for y in range(board.size_y):
                if board.get(x, y) == "@":
                    neighbors = board.adjacent(x, y)
                    if neighbors.count("@") < 4:
                        movable.append((x, y))
        if len(movable) == 0:
            break
        for x,y in movable:
            board.set(x, y, "x")
        print(f"Moved {len(movable)} rolls")
        movable = []
    if movable:
        print("!!!!!!!!!!! NOT DONE, INCREASE MAX ITERATIONS !!!!!!!!!!!!!!!")
    return board.count("x")


def part2(board):
    return solve(board, 1000)


if __name__ == "__main__":
    with open(get_input_name(4, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(4, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
