#!/usr/bin/env python
# -*- coding: utf-8
import io
import textwrap

import pytest

from ibidem.advent_of_code.board import Board

ADJACENCY_BOARD = Board.from_string(textwrap.dedent("""\
    abcd
    efgh
    ijkl
    mnop
    qrst
    """))


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


def test_count():
    b = Board.from_string(".#.\n#.#\n###")
    assert b.count(".") == 3


@pytest.mark.parametrize("x, y, expected", (
        (1, 1, list("abcegijk")),
        (0, 0, list("bef")),
        (3, 3, list("klost")),
))
def test_adjacent(x, y, expected):
    actual = ADJACENCY_BOARD.adjacent(x, y)
    assert actual == expected
