#!/usr/bin/env python
# -*- coding: utf-8

try:
    from .board import Board
    from .intcode import load_program, IntCode
except ModuleNotFoundError:
    from board import Board
    from intcode import load_program, IntCode

from collections import namedtuple


Color = namedtuple("Color", ("char", "value"))


class Colors(object):
    BLACK = Color(" ", 0)
    WHITE = Color("#", 1)

    _value2char = {c.value: c.char for c in (BLACK, WHITE)}
    _char2value = {c.char: c.value for c in (BLACK, WHITE)}

    @classmethod
    def value2char(cls, value):
        return cls._value2char[value]

    @classmethod
    def char2value(cls, char):
        return cls._char2value[char]


class OutputMode(object):
    COLOR = object()
    ROTATE = object()

    @classmethod
    def alternate(cls, current):
        if current == cls.COLOR:
            return cls.ROTATE
        return cls.COLOR


class Vector(namedtuple("Vector", ("x", "y"))):
    def rotate(self, direction):
        """https://stackoverflow.com/questions/4780119/2d-euclidean-vector-rotations
        (x, y) rotated 90 degrees around (0, 0) is (-y, x)
        rotate clockwise, you simply do it the other way around, getting (y, -x)."""
        if direction == 0:
            return Vector(-1*self.y, self.x)
        elif direction == 1:
            return Vector(self.y, -1*self.x)
        raise ValueError("Direction can only be 0 or 1")

    def char(self):
        if self.x == 0:
            if self.y == 1:
                return "^"
            elif self.y == -1:
                return "v"
        elif self.x == 1:
            return ">"
        elif self.x == -1:
            return "<"
        raise ValueError("Invalid direction {}".format(self))

    def __repr__(self):
        return "Vector(x={}, y={})".format(self.x, self.y)


class Position(Vector):
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    __radd__ = __add__


class Robot(object):
    def __init__(self, program):
        self._intcode = IntCode(program)
        self._position = Position(0, 0)
        self._direction = Vector(0, 1)
        self._board = Board(1000, 1000)
        self._output_mode = OutputMode.COLOR
        self._paint_counter = {}

    def set_start_white(self):
        self._board.set(0, 0, Colors.WHITE.char)

    def input(self):
        char = self._board.get(self._position.x, self._position.y)
        return Colors.char2value(char)

    def output(self, value):
        if self._output_mode == OutputMode.COLOR:
            char = Colors.value2char(value)
            self._board.set(self._position.x, self._position.y, char)
            self._paint_counter[self._position] = 1
        elif self._output_mode == OutputMode.ROTATE:
            self._direction = self._direction.rotate(value)
            self._position += self._direction
        self._output_mode = OutputMode.alternate(self._output_mode)

    def run(self):
        self._intcode.execute(self.input, self.output)
        self._board.set(self._position.x, self._position.y, self._direction.char())
        self._board.print()
        painted = sum(self._paint_counter.values())
        print("The robot painted {} panels".format(painted))


def part1():
    program = load_program("dec11")
    bot = Robot(program)
    bot.run()


def part2():
    program = load_program("dec11")
    bot = Robot(program)
    bot.set_start_white()
    bot.run()


if __name__ == "__main__":
    part1()
    part2()
