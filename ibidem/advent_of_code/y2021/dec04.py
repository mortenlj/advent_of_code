#!/usr/bin/env python
import re
import textwrap

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class BingoBoard(Board):
    _SPACE = re.compile(r" +")

    @classmethod
    def from_space_separated_strings(cls, lines):
        size_y = len(lines)
        size_x = len(cls._SPACE.split(lines[0].strip()))
        board = cls(size_x, size_y, do_translate=False, flip=False, fill_value=-1, dtype=np.int_)
        for y, row in enumerate(lines):
            for x, value in enumerate(cls._SPACE.split(row.strip())):
                board.set(x, y, int(value))
        board.grid = np.ma.asarray(board.grid)
        return board

    def mark(self, value):
        where = self.grid == value
        self.grid[where] = np.ma.masked

    def won(self):
        return np.any(np.all(self.grid.mask, axis=0)) or np.any(np.all(self.grid.mask, axis=1))

    def score(self):
        return np.sum(self.grid)

    def print(self, buf=None):
        lines = []
        rows = reversed(self.grid) if self._flip else self.grid
        for row in rows:
            if not all(c == self._fill_value for c in row):
                lines.append(" ".join(str(v) for v in row).rstrip())
        output = "\n".join(lines)
        text = textwrap.dedent(output)
        print(text, file=buf)


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
