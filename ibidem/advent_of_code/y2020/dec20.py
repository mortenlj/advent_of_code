#!/usr/bin/env python
import operator
from collections import deque
from functools import reduce

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Tile:
    def __init__(self, title, edges, flipped):
        self.id = int(title[5:9])
        self.edges = edges
        self.flipped = flipped


def load():
    tiles = []
    with open(get_input_name(20, 2020)) as fobj:
        lines = deque(fobj.read().splitlines(keepends=False))
        while lines:
            title = lines.popleft()
            input = []
            for _ in range(10):
                input.append(lines.popleft())
            board = Board.from_string("\n".join(input))
            grid = board.grid
            edges, grid = collect_edges(grid)
            grid = np.flipud(grid)
            flipped, grid = collect_edges(grid)
            tiles.append(Tile(title, edges, flipped))
            lines.popleft()
    return tiles


def collect_edges(grid):
    edges = []
    for _ in range(4):
        edges.append(tuple(grid[0]))
        grid = np.rot90(grid)
    return edges, grid


def count_edges(edges, other_edges):
    count = 0
    for edge in edges:
        if edge not in other_edges:
            count += 1
    return count


def part1(tiles):
    corners = []
    for tile in tiles:
        other_edges = set()
        for other in tiles:
            if tile.id == other.id:
                continue
            other_edges.update(other.edges)
            other_edges.update(other.flipped)
        count = count_edges(tile.edges, other_edges)
        if count == 2:
            corners.append(tile)
            continue
        count = count_edges(tile.flipped, other_edges)
        if count == 2:
            corners.append(tile)
    print(f"Found {len(corners)} corners! Their IDs are:")
    corner_ids = [c.id for c in corners]
    print(corner_ids)
    result = reduce(operator.mul, corner_ids)
    print(f"That makes the result: {result}")


def part2():
    pass


if __name__ == "__main__":
    tiles = load()
    part1(tiles)
    part2()
