#!/usr/bin/env python
from collections import deque, defaultdict

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.length = 0 if parent is None else parent.length + 1

    @property
    def coords(self):
        return self.x, self.y

    def visited(self, coords):
        node = self
        while node is not None:
            if node.coords == coords:
                return True
            node = node.parent
        return False

    def __repr__(self):
        return f"Node(x: {self.x}, y: {self.y})"


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def find_start_and_end(board: Board) -> ((int, int), (int, int)):
    where = board.find(".")
    return tuple(reversed(where[0])), tuple(reversed(where[-1]))


def part1(board):
    start, end = find_start_and_end(board)
    working = deque([Node(*start)])
    nodes = {}
    while working:
        node = working.popleft()
        if node.coords in nodes:
            contender = nodes[node.coords]
            if node.length <= contender.length:
                continue
        nodes[node.coords] = node
        value = board.get(*node.coords)
        match value:
            case ">":
                working.append(Node(node.x + 1, node.y, node))
            case "<":
                working.append(Node(node.x - 1, node.y, node))
            case "^":
                working.append(Node(node.x, node.y - 1, node))
            case "v":
                working.append(Node(node.x, node.y + 1, node))
            case _:
                for x, y in board.adjacent_indexes(node.x, node.y, include_diagonal=False):
                    if node.parent and node.parent.coords == (x, y):
                        continue
                    value = board.get(x, y)
                    if value == "#":
                        continue
                    if value == ">" and x < node.x:
                        continue
                    if value == "<" and x > node.x:
                        continue
                    if value == "^" and y > node.y:
                        continue
                    if value == "v" and y < node.y:
                        continue
                    working.append(Node(x, y, node))
    return nodes[end].length


def show_path(board, node):
    while node:
        board.set(*node.coords, "O")
        node = node.parent
    board.print()


def part2(board):
    start, end = find_start_and_end(board)
    working = deque([Node(*start)])
    nodes = defaultdict(list)
    while working:
        node = working.popleft()
        nodes[node.coords].append(node)
        if node.coords == end:
            continue
        for x, y in board.adjacent_indexes(node.x, node.y, include_diagonal=False):
            if node.visited((x, y)):
                continue
            value = board.get(x, y)
            if value == "#":
                continue
            working.append(Node(x, y, node))
    # show_path(board, nodes[end])
    return max(n.length for n in nodes[end])


if __name__ == "__main__":
    with open(get_input_name(23, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(23, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
