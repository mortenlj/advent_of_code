#!/usr/bin/env python
# -*- coding: utf-8
import io
import re
import textwrap

import numpy as np

GROW_SIZE = 200


class TooSmall(Exception):
    """The current grid is too small for the wanted operation"""
    pass


class Board(object):
    def __init__(self, size_x=None, size_y=None, do_translate=True, flip=False, fill_value=" ", dtype="<U15",
                 growable=True):
        size_x = 10 if size_x is None else size_x
        size_y = 10 if size_y is None else size_y
        self.grid = np.full((size_y, size_x), fill_value, dtype)
        self._fill_value = fill_value
        self._do_translate = do_translate
        self._flip = flip
        self._growable = growable

    @property
    def size_x(self):
        return self.grid.shape[1]

    @property
    def size_y(self):
        return self.grid.shape[0]

    @classmethod
    def from_string(cls, string, fill_value=" ", dtype="<U15", growable=True):
        lines = string.strip().splitlines()
        size_y = len(lines)
        size_x = len(lines[0].strip())
        board = cls(size_x, size_y, do_translate=False, flip=False, fill_value=fill_value, dtype=dtype,
                    growable=growable)
        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                board.set(x, y, char)
        return board

    def set(self, x, y, c):
        gx, gy = self._translate(x, y)
        try:
            self._index_check(gx, gy)
        except TooSmall as e:
            self._grow(e.args[-1])
            return self.set(x, y, c)
        old = self.grid[gy][gx]
        self.grid[gy][gx] = c
        return old

    def get(self, x, y):
        gx, gy = self._translate(x, y)
        try:
            self._index_check(gx, gy)
        except TooSmall as e:
            self._grow(e.args[-1])
            return self.get(x, y)
        return self.grid[gy][gx]

    def __getitem__(self, item):
        return self.get(*item)

    def __setitem__(self, key, value):
        return self.set(key[0], key[1], value)

    def _grow(self, axis):
        if not self._growable:
            raise IndexError(f"{axis.upper()} coordinate out of bounds")
        if self._do_translate:
            if axis == "x":
                pad = ((0, 0), (GROW_SIZE // 2, GROW_SIZE // 2))
            else:
                pad = ((GROW_SIZE // 2, GROW_SIZE // 2), (0, 0))
        else:
            if axis == "x":
                pad = ((0, 0), (0, GROW_SIZE))
            else:
                pad = ((0, GROW_SIZE), (0, 0))
        self.grid = np.pad(self.grid, pad, mode="constant", constant_values=self._fill_value)

    def _translate(self, x, y):
        if not self._do_translate:
            return x, y
        gx = x + self.size_x // 2
        gy = -1 * y + self.size_y // 2
        return gx, gy

    def _index_check(self, gx, gy):
        if not self._do_translate:
            if gx < 0:
                raise IndexError("X coordinate ({}) out of bounds".format(gx), "x")
            if gy < 0:
                raise IndexError("Y coordinate ({}) out of bounds".format(gy), "y")
        if not 0 <= gx < self.size_x:
            raise TooSmall("X coordinate ({}) out of bounds".format(gx), "x")
        if not 0 <= gy < self.size_y:
            raise TooSmall("Y coordinate ({}) out of bounds".format(gy), "y")

    def count(self, v):
        return sum((row == v).sum() for row in self.grid)

    def copy(self):
        b = Board(size_x=self.size_x, size_y=self.size_y, do_translate=self._do_translate,
                  flip=self._flip, fill_value=self._fill_value, dtype=self.grid.dtype)
        b.grid = self.grid.copy()
        return b

    def adjacent(self, x, y, include_diagonal=True):
        values = []
        for nx, ny in self.adjacent_indexes(x, y, include_diagonal):
            values.append(self.get(nx, ny))
        return values

    def adjacent_indexes(self, x, y, include_diagonal):
        for j in (-1, 0, 1):
            for i in (-1, 0, 1):
                if i == j == 0:
                    continue
                if not include_diagonal and (i != 0 and j != 0):
                    continue
                try:
                    nx, ny = x + i, y + j
                    self._index_check(nx, ny)
                    yield (nx, ny)
                except (IndexError, TooSmall):
                    pass

    def adjacent_view(self, x, y):
        x_min = max(x - 1, 0)
        y_min = max(y - 1, 0)
        x_max = min(x + 2, self.grid.shape[1])
        y_max = min(y + 2, self.grid.shape[0])
        return self.grid[(slice(y_min, y_max), slice(x_min, x_max))]

    def print(self, buf=None, include_empty=False, crop_to_bounds=False):
        lines = []
        rows = reversed(self.grid) if self._flip else self.grid
        min_row = 0
        max_row = self.size_y
        if crop_to_bounds:
            min_row, max_row = max_row, min_row
        for row in rows:
            if (tainted := not all(c == self._fill_value for c in row)) or include_empty:
                if tainted and crop_to_bounds:
                    min_row = min(min_row, len(lines))
                    max_row = max(max_row, len(lines) + 1)
                lines.append("".join(str(v) for v in row).rstrip())
        output = "\n".join(lines[min_row:max_row])
        if not include_empty or crop_to_bounds:
            text = textwrap.dedent(output)
        else:
            text = output
        print(text, file=buf)

    def __repr__(self):
        buf = io.StringIO()
        self.print(buf)
        return buf.getvalue()

    def __eq__(self, other):
        return other is not None and \
               (self.grid == other.grid).all() and \
               self._flip == other._flip and self._do_translate == other._do_translate


class BingoBoard(Board):
    _SPACE = re.compile(r" +")

    @classmethod
    def from_space_separated_strings(cls, lines):
        size_y = len(lines)
        size_x = len(cls._SPACE.split(lines[0].strip()))
        board = cls(size_x, size_y, do_translate=False, flip=False, fill_value=-1, dtype=np.int_)
        for y, row in enumerate(lines):
            for x, value in enumerate(cls._SPACE.split(row.strip())):
                board.set(x, y, int(value))
        board.grid = np.ma.asarray(board.grid)
        return board

    def mark(self, value):
        where = self.grid == value
        self.grid[where] = np.ma.masked

    def won(self):
        return np.any(np.all(self.grid.mask, axis=0)) or np.any(np.all(self.grid.mask, axis=1))

    def score(self):
        return np.sum(self.grid)

    def print(self, buf=None):
        lines = []
        rows = reversed(self.grid) if self._flip else self.grid
        for row in rows:
            if not all(c == self._fill_value for c in row):
                lines.append(" ".join(str(v) for v in row).rstrip())
        output = "\n".join(lines)
        text = textwrap.dedent(output)
        print(text, file=buf)


if __name__ == "__main__":
    pass
