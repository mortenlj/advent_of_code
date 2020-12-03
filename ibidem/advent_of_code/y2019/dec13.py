#!/usr/bin/env python
# -*- coding: utf-8

from collections import namedtuple

from ibidem.advent_of_code.board import Board
from .intcode import load_program, IntCode

Tile = namedtuple("Tile", ["value", "char"])


class Tiles(object):
    EMPTY = Tile(0, " ")
    WALL = Tile(1, "#")
    BLOCK = Tile(2, "X")
    PADDLE = Tile(3, "-")
    BALL = Tile(4, "O")

    @classmethod
    def from_value(cls, value):
        for attr in dir(cls):
            if attr.isupper() and getattr(cls, attr).value == value:
                return getattr(cls, attr)


class Arcade(object):
    def __init__(self, program):
        self._board = Board(100, 100, flip=True)
        self._machine = IntCode(program)
        self._acc = []
        self._score = 0
        self._direction = 0
        self._ball_x = None
        self._paddle_x = None

    def play(self):
        self._machine.execute(input_func=self._joystick, output_func=self._draw)
        self._board.print()
        return self._count(), self._score

    def _joystick(self):
        if self._ball_x and self._paddle_x:
            self._direction = self._ball_x - self._paddle_x
        return self._direction

    def _draw(self, value):
        self._acc.append(value)
        if len(self._acc) == 3:
            x, y, tile_value = self._acc
            if x == -1 and y == 0:
                self._score = tile_value
                print("New score: {}".format(self._score))
                self._board.print()
                print()
            else:
                tile = Tiles.from_value(tile_value)
                if tile == Tiles.BALL:
                    self._ball_x = x
                elif tile == Tiles.PADDLE:
                    self._paddle_x = x
                self._board.set(x, y, tile.char)
            self._acc = []

    def _count(self):
        return self._board.count(Tiles.BLOCK.char)


def part1():
    program = load_program("dec13")
    play(program)


def part2():
    program = load_program("dec13")
    program[0] = 2
    play(program)


def play(program):
    arcade = Arcade(program)
    count, score = arcade.play()
    print("There are {} blocks left in play, score is {}".format(count, score))


if __name__ == "__main__":
    part2()
