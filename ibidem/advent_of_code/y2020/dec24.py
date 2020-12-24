#!/usr/bin/env python
from enum import auto, Enum

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def coord(self):
        return self.r, self.q

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r)


class Tile(Enum):
    WHITE = auto()
    BLACK = auto()


class Direction(Enum):
    def __new__(cls, value, axial):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.axial = axial
        return obj

    EAST = ("e", Hex(+1, 0))
    SOUTHEAST = ("se", Hex(0, +1))
    SOUTHWEST = ("sw", Hex(-1, +1))
    WEST = ("w", Hex(-1, 0))
    NORTHWEST = ("nw", Hex(0, -1))
    NORTHEAST = ("ne", Hex(1, -1))


def parse_line(line):
    i = iter(line)
    for c in i:
        if c == "e":
            yield Direction.EAST
        elif c == "w":
            yield Direction.WEST
        else:
            c += next(i)
            yield Direction(c)


def load():
    with open(get_input_name(24, 2020)) as fobj:
        for line in fobj:
            yield list(parse_line(line.strip()))


def part1(tile_flips):
    room = Board(fill_value=Tile.WHITE, dtype=Tile)
    for flip_seq in tile_flips:
        t = Hex(0, 0)
        for m in flip_seq:
            t += m.axial
        room[t.coord] = Tile.WHITE if room[t.coord] == Tile.BLACK else Tile.BLACK
    idx = np.where(room.grid == Tile.BLACK)
    result = len(room.grid[idx])
    print(f"There are {result} black tiles in the room")
    return result


def part2(tile_flips):
    pass


if __name__ == "__main__":
    tile_flips = list(load())
    part1(tile_flips)
    part2(tile_flips)
