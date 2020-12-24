#!/usr/bin/env python
# -*- coding: utf-8

import enum

import numpy as np
from colorama import init, Fore, Back

from ibidem.advent_of_code.board import Board
from .intcode import load_program, IntCode

SIZE = 100


class Directions(enum.IntEnum):
    NORTH = (1, "^")
    SOUTH = (2, "v")
    WEST = (3, "<")
    EAST = (4, ">")

    def __new__(cls, value, char):
        instance = int.__new__(cls, value)
        instance._value_ = value
        instance.char = char
        return instance

    def right(self):
        order = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)
        idx = order.index(self)
        next = idx + 1
        if next >= len(order):
            next = 0
        return order[next]

    def left(self):
        order = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)
        idx = order.index(self)
        next = idx - 1
        if next < 0:
            next = len(order) - 1
        return order[next]

    def move(self, x, y):
        if self == Directions.NORTH:
            return x, y + 1
        if self == Directions.SOUTH:
            return x, y - 1
        if self == Directions.WEST:
            return x - 1, y
        if self == Directions.EAST:
            return x + 1, y
        raise ValueError("Invalid direction")


class Status(enum.IntEnum):
    WALL = 0
    OPEN = 1
    GOAL = 2


class NodeType(enum.Enum):
    START = "O"
    WALL = "#"
    OPEN = "."
    GOAL = "X"
    UNKNOWN = " "


class Node(object):
    def __init__(self, visits, type, parent, distance, x=None, y=None):
        self.visits = visits
        self.type = type
        self.parent = parent
        self.distance = distance
        self.x = x
        self.y = y


class Complete(Exception):
    pass


class Mapper(object):
    def __init__(self, intcode):
        self._board = Board(SIZE, SIZE)
        self._nodes = Board(SIZE, SIZE, fill_value=Node(0, NodeType.UNKNOWN, None, 9999), dtype=np.object_)
        for y in range(SIZE):
            for x in range(SIZE):
                self._nodes.grid[y][x] = Node(0, NodeType.UNKNOWN, None, 9999)
        self._x = self._y = 0
        start_node = Node(1, NodeType.START, None, 0)
        self._nodes.set(self._x, self._y, start_node)
        self._board.set(self._x, self._y, self._nodes.get(self._x, self._y).type.value)
        self._current_direction = Directions.NORTH
        self._current_node = start_node
        self._intcode = intcode
        self._counter = 0
        self._goal = None

    def map(self):
        try:
            self._intcode.execute(self._input, self._output)
        except Complete:
            self._draw_solved_map()
            return self._goal, self._nodes

    def _draw_solved_map(self):
        current = self._goal
        while current.type is not NodeType.START:
            c = self._board.get(current.x, current.y)
            self._board.set(current.x, current.y, Back.GREEN + c + Back.RESET)
            current = current.parent
        self._board.print()
        print("Distance to goal: {}".format(self._goal.distance))

    def is_map_complete(self):
        if self._goal is None:
            return False
        for row in self._nodes.grid:
            if all(node.type is NodeType.UNKNOWN for node in row):
                continue
            if any(0 < node.visits < 4 for node in row):
                return False
        return True

    def _input(self):
        best = None
        for direction in Directions:
            x, y = direction.axial(self._x, self._y)
            candidate = self._nodes.get(x, y)
            if best is None or candidate.visits < best[0].visits:
                best = (candidate, direction)
        self._current_direction = best[1]
        return self._current_direction

    def _output(self, v):
        if v == Status.WALL:
            x, y = self._current_direction.move(self._x, self._y)
            node = Node(9999, NodeType.WALL, self._current_node, 9999, x=x, y=y)
            self._nodes.set(x, y, node)
            self._board.set(x, y, node.type.value)
        else:
            self._x, self._y = self._current_direction.move(self._x, self._y)
            prev_node, node = self._current_node, self._nodes.get(self._x, self._y)
            self._current_node = node
            node.x = self._x
            node.y = self._y
            node.visits += 1
            if node.distance > prev_node.distance:
                node.distance = prev_node.distance + 1
                node.parent = prev_node
            if v == Status.GOAL:
                node.type = NodeType.GOAL
                self._goal = node
            elif node.type != NodeType.START:
                node.type = NodeType.OPEN
            self._board.set(self._x, self._y, node.type.value)
        self._counter += 1
        if self._counter % 5 == 0:
            prev = self._board.set(self._x, self._y, Fore.RED + self._current_direction.char + Fore.RESET)
            self._board.print()
            self._board.set(self._x, self._y, prev)
        if self.is_map_complete():
            raise Complete()


def part1():
    intcode = IntCode(load_program("dec15"))
    mapper = Mapper(intcode)
    mapper.map()
    # TODO: Once map is generated, find shortest path


if __name__ == "__main__":
    init()
    part1()
