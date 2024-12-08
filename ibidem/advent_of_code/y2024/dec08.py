#!/usr/bin/env python
import itertools
from collections import defaultdict
from dataclasses import dataclass

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def manhattan(self):
        return abs(self.x) + abs(self.y)

    def antinode(self, other):
        path = self - other
        return self + path


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def find_antinodes1(a, b, board):
    pos = a.antinode(b)
    if 0 <= pos.x < board.size_x and 0 <= pos.y < board.size_y:
        yield pos
    pos = b.antinode(a)
    if 0 <= pos.x < board.size_x and 0 <= pos.y < board.size_y:
        yield pos


def find_antinodes2(a, b, board):
    path = a - b
    pos = a + path
    while 0 <= pos.x < board.size_x and 0 <= pos.y < board.size_y:
        yield pos
        pos = pos + path


def part1(board: Board):
    frequencies = map_frequencies(board)
    antinodes = set()
    for freq in frequencies.keys():
        for a, b in itertools.combinations(frequencies[freq], 2):
            antinodes.update(find_antinodes1(a, b, board))
    return len(antinodes)


def map_frequencies(board):
    frequencies = defaultdict(list)
    for y in range(board.size_y):
        for x in range(board.size_x):
            v = board.get(x, y)
            if v != ".":
                frequencies[v].append(Position(x, y))
    return frequencies


def part2(board: Board):
    frequencies = map_frequencies(board)
    antinodes = set()
    for freq in frequencies.keys():
        for a, b in itertools.permutations(frequencies[freq], 2):
            antinodes.update(find_antinodes2(a, b, board))
            antinodes.add(a)
    return len(antinodes)


if __name__ == "__main__":
    with open(get_input_name(8, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
