#!/usr/bin/env python
# -*- coding: utf-8

from ibidem.advent_of_code.board import Board
from .intcode import load_program, IntCode


class Scanner(object):
    def __init__(self, size):
        self._board = Board(size, size, do_translate=False)
        self._program = load_program("dec19")
        self._x_given = False
        self._current_pos = None
        self._positions = [(x, y) for x in range(size) for y in range(size)]

    def _input(self):
        if self._current_pos is None:
            self._current_pos = self._positions.pop(0)
        if self._x_given:
            result = self._current_pos[1]
            self._x_given = False
            return result
        else:
            result = self._current_pos[0]
            self._x_given = True
            return result

    def _output(self, value):
        if value == 0:
            self._board.set(self._current_pos[0], self._current_pos[1], ".")
        elif value == 1:
            self._board.set(self._current_pos[0], self._current_pos[1], "#")
        else:
            raise ValueError("Invalid output value")
        self._current_pos = None

    def scan(self):
        while self._positions:
            intcode = IntCode(self._program)
            intcode.execute(self._input, self._output)
        self._board.print()
        return self._board.count("#")


def part1():
    scanner = Scanner(50)
    result = scanner.scan()
    print("The tractor beam affects {} points".format(result))


if __name__ == "__main__":
    part1()
