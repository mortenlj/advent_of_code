#!/usr/bin/env python
import networkx
import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, time_this


def make_graph(board):
    g = networkx.DiGraph()
    for x in range(board.size_x):
        for y in range(board.size_y):
            for p in board.adjacent_indexes(x, y, include_diagonal=False):
                g.add_edge(p, (x, y), risk=board.get(x, y))
    return g, (board.size_x - 1, board.size_y - 1)


def load1(fobj):
    board = Board.from_string(fobj.read(), fill_value=0, dtype=int, growable=False)
    return make_graph(board)


def load2(fobj):
    board = Board.from_string(fobj.read(), fill_value=0, dtype=int, growable=False)
    g = board.grid
    g = np.tile(g, (5, 5))
    overlay = np.repeat(np.arange(5), board.size_x)
    overlay = overlay + overlay.reshape((overlay.shape[0], 1))
    m = np.ma.asarray(g + overlay)
    m.mask = m <= 9
    m = m - 9
    board.grid = m.data
    return make_graph(board)


@time_this
def part1(graph, lr):
    return networkx.shortest_path_length(graph, (0, 0), lr, "risk")


@time_this
def part2(graph, lr):
    return networkx.shortest_path_length(graph, (0, 0), lr, "risk")


if __name__ == "__main__":
    with open(get_input_name(15, 2021)) as fobj:
        p1_result = part1(*load1(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2021)) as fobj:
        p2_result = part2(*load2(fobj))
        print(f"Part 2: {p2_result}")
