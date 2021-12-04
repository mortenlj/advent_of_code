#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name
from ibidem.advent_of_code.board import BingoBoard


def load():
    with open(get_input_name(4, 2021)) as fobj:
        return _load_input(fobj.read())


def _load_input(string):
    numbers = None
    boards = []
    lines = []
    for line in string.splitlines(keepends=False):
        if numbers is None:
            numbers = [int(x) for x in line.split(",")]
            continue
        if line.strip():
            lines.append(line)
        elif lines:
            boards.append(BingoBoard.from_space_separated_strings(lines))
            lines = []
    if lines:
        boards.append(BingoBoard.from_space_separated_strings(lines))
    return numbers, boards


def part1(numbers, boards):
    for num in numbers:
        for board in boards:
            board.mark(num)
            if board.won():
                return num * board.score()

    
def part2(numbers, boards):
    remaining = list(range(len(boards)))
    for num in numbers:
        for i, board in enumerate(boards):
            if i not in remaining:
                continue
            board.mark(num)
            if board.won():
                remaining.remove(i)
            if not remaining:
                return num * board.score()

    
if __name__ == "__main__":
    numbers, boards = load()
    p1_result = part1(numbers, boards)
    print(f"Part 1: {p1_result}")
    p2_result = part2(numbers, boards)
    print(f"Part 2: {p2_result}")
