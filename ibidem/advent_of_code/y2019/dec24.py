#!/usr/bin/env python
# -*- coding: utf-8

import numpy as np

from ibidem.advent_of_code.board import Board
from .util import get_input_name

BOARD_SIZE = 5


class GoL(object):
    def __init__(self, board):
        self._board = board
        self._seen = set()

    def _board_value(self, i, j):
        if i == -1 or i == BOARD_SIZE or j == -1 or j == BOARD_SIZE:
            return False
        return self._board[i][j]

    def step(self):
        self._seen.add(self._hashable_board())
        new_grid = self._board.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                total = 0
                for ni, nj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    total += int(self._board_value(i+ni, j+nj))
                if self._board[i][j]:
                    if total != 1:
                        new_grid[i][j] = False
                else:
                    if total == 1 or total == 2:
                        new_grid[i][j] = True

        self._board = new_grid

    def _hashable_board(self):
        return np.packbits(self._board).tobytes()

    def duplicate(self):
        return self._hashable_board() in self._seen


def part1():
    with open(get_input_name("dec24")) as fobj:
        char_board = Board.from_string(fobj.read().strip())
        board = char_board.grid == "#"
        gol = GoL(board)
        while not gol.duplicate():
            gol.step()
        bd_points = (2 ** np.arange(25))
        points = bd_points * gol._board.flatten()
        print("This board has a biodiversity of {}".format(np.sum(points)))


if __name__ == "__main__":
    part1()
