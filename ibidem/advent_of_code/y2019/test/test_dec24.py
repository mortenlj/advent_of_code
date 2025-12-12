#!/usr/bin/env python
# -*- coding: utf-8

import textwrap

import pytest

from ibidem.advent_of_code.board import Board
from ..dec24 import GoL

STEPS = [
    textwrap.dedent("""\
    ....#
    #..#.
    #..##
    ..#..
    #....
    """),
    textwrap.dedent("""\
    #..#.
    ####.
    ###.#
    ##.##
    .##..
    """),
    textwrap.dedent("""\
    #####
    ....#
    ....#
    ...#.
    #.###
    """),
    textwrap.dedent("""\
    #....
    ####.
    ...##
    #.##.
    .##.#
    """),
    textwrap.dedent("""\
    ####.
    ....#
    ##..#
    .....
    ##...
    """),
]


def make_board(string):
    char_board = Board.from_string(string)
    return char_board.grid == "#"


@pytest.mark.parametrize(
    "start, end",
    (
        (STEPS[0], STEPS[1]),
        (STEPS[1], STEPS[2]),
        (STEPS[2], STEPS[3]),
        (STEPS[3], STEPS[4]),
    ),
)
def test_gol(start, end):
    board = make_board(start)
    gol = GoL(board)
    gol.step()
    expected = make_board(end)
    assert (gol._board == expected).all()
