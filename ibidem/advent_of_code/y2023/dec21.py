#!/usr/bin/env python
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read())


def part1(board: Board, steps):
    visit = board.find('S')
    for i in range(steps):
        new_visit = set()
        for x, y in visit:
            for nx, ny in board.adjacent_indexes(x, y, False):
                if board.get(nx, ny) in 'S.':
                    new_visit.add((nx, ny))
        visit = new_visit
    return len(visit)


def part2(board, steps):
    return None


if __name__ == "__main__":
    with open(get_input_name(21, 2023)) as fobj:
        p1_result = part1(load(fobj), 64)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(21, 2023)) as fobj:
        p2_result = part2(load(fobj), 26501365)
        print(f"Part 2: {p2_result}")
