#!/usr/bin/env python
# -*- coding: utf-8
import io
import textwrap

import pytest

from ibidem.advent_of_code.board import Board


@pytest.fixture
def adjacency_board():
    return Board.from_string(textwrap.dedent("""\
        abcd
        efgh
        ijkl
        mnop
        qrst
        """), growable=False)


def test_board():
    b = Board(11, 11)
    b.set(-5, -5, "/")
    b.set(5, 5, "7")
    b.set(0, 0, "0")
    b.set(-5, 5, "<")
    b.set(5, -5, ">")

    assert (b.grid == [
        ["<", " ", " ", " ", " ", " ", " ", " ", " ", " ", "7"],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", "0", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ["/", " ", " ", " ", " ", " ", " ", " ", " ", " ", ">"],
    ]).all()
    b.print()


def test_from_string():
    b = Board.from_string(textwrap.dedent("""\
        0.#.#########.1
        ..#...#...#....
        ..#.#.#4..#....
        ..#...#...#....
        3.#.#.#...####2
    """))
    assert b.get(0, 0) == "0"
    assert b.get(2, 0) == "#"
    assert b.get(14, 0) == "1"
    assert b.get(0, 4) == "3"
    assert b.get(2, 4) == "#"
    assert b.get(14, 4) == "2"
    assert b.get(14, 2) == "."
    assert b.get(7, 2) == "4"


def test_print():
    text = textwrap.dedent("""\
        0.#.#########.1
        ..#...#...#....
        ..#.#.#4..#....
        ..#...#...#....
        3.#.#.#...####2
    """)
    b = Board.from_string(text)
    buf = io.StringIO()
    b.print(buf)
    assert buf.getvalue() == text


def test_print_cropped():
    b = Board(size_x=100, size_y=100)
    b.set(10, 10, "X")
    b.set(12, 12, "X")
    buf = io.StringIO()
    b.print(buf, include_empty=True, crop_to_bounds=True)
    assert buf.getvalue() == "  X\n\nX\n"


def test_count():
    b = Board.from_string(".#.\n#.#\n###")
    assert b.count(".") == 3


@pytest.mark.parametrize("x, y, expected", (
        (1, 1, list("abcegijk")),
        (0, 0, list("bef")),
        (3, 3, list("klost")),
))
def test_adjacent(x, y, expected, adjacency_board):
    actual = adjacency_board.adjacent(x, y)
    assert actual == expected


@pytest.mark.parametrize("x, y, expected", (
        (1, 1, list("begj")),
        (0, 0, list("be")),
        (3, 3, list("lot")),
))
def test_adjacent_without_diagonal(x, y, expected, adjacency_board):
    actual = adjacency_board.adjacent(x, y, include_diagonal=False)
    assert actual == expected


def test_get_coord(adjacency_board):
    assert adjacency_board[1, 1] == "f"


def test_set_coord(adjacency_board):
    adjacency_board[1, 1] = "X"
    assert adjacency_board.get(1, 1) == "X"
