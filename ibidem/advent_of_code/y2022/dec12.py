#!/usr/bin/env python

from networkx import DiGraph, shortest_path_length

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read())


def part1(board):
    g, start, end = build_graph(board)
    return shortest_path_length(g, start, end)


def build_graph(board):
    g = DiGraph()
    start = end = None
    for x in range(board.size_x):
        for y in range(board.size_y):
            node = (x, y)
            height = board.get(*node)
            if height == "S":
                height = "a"
                start = node
            elif height == "E":
                height = "z"
                end = node
            g.add_node(node, height=height)
            for pos in board.adjacent_indexes(x, y, False):
                other = board.get(*pos)
                if other == "S":
                    other = "a"
                elif other == "E":
                    other = "z"
                diff = ord(other) - ord(height)
                if diff <= 1:
                    g.add_edge(node, pos)
    return g, start, end


def part2(board):
    g, start, end = build_graph(board)
    results = shortest_path_length(g, target=end)
    filtered = (length for node, length in results.items() if board.get(*node) in ("a", "S"))
    return min(filtered)


if __name__ == "__main__":
    with open(get_input_name(12, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(12, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
