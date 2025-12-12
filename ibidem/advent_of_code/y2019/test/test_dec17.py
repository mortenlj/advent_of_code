import textwrap

import pytest

from ibidem.advent_of_code.board import Board
from ..dec17 import get_intersections, calculate_alignments

SMALL_MAP = textwrap.dedent("""\
    ..#..........
    ..#..........
    #######...###
    #.#...#...#.#
    #############
    ..#...#...#..
    ..#####...^..    
    """)


@pytest.mark.parametrize(
    "board, intersections",
    ((Board.from_string(SMALL_MAP), {(2, 2), (2, 4), (6, 4), (10, 4)}),),
)
def test_get_intersections(board, intersections):
    actual = set(get_intersections(board))
    assert actual == intersections


@pytest.mark.parametrize(
    "intersections, result", (({(2, 2), (2, 4), (6, 4), (10, 4)}, 76),)
)
def test_aligments(intersections, result):
    actual = calculate_alignments(intersections)
    assert actual == result
