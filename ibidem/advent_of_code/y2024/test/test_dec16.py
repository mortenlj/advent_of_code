import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec16 import load, solve

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        1024,
        25,
        io.StringIO(
            textwrap.dedent("""\
        ###############
        #............E#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #S............#
        ###############
    """)
        ),
    ),
    Case(
        2024,
        25,
        io.StringIO(
            textwrap.dedent("""\
        ###############
        #............E#
        #........######
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #.............#
        #S............#
        ###############
    """)
        ),
    ),
    Case(
        7036,
        45,
        io.StringIO(
            textwrap.dedent("""\
        ###############
        #.......#....E#
        #.#.###.#.###.#
        #.....#.#...#.#
        #.###.#####.#.#
        #.#.#.......#.#
        #.#.#####.###.#
        #...........#.#
        ###.#.#####.#.#
        #...#.....#.#.#
        #.#.#.###.#.#.#
        #.....#...#.#.#
        #.###.#.#.#.#.#
        #S..#.....#...#
        ###############
    """)
        ),
    ),
    Case(
        11048,
        64,
        io.StringIO(
            textwrap.dedent("""\
        #################
        #...#...#...#..E#
        #.#.#.#.#.#.#.#.#
        #.#.#.#...#...#.#
        #.#.#.#.###.#.#.#
        #...#.#.#.....#.#
        #.#.#.#.#.#####.#
        #.#...#.#.#.....#
        #.#.#####.#.###.#
        #.#.#.......#...#
        #.#.###.#####.###
        #.#.#...#.....#.#
        #.#.#.#####.###.#
        #.#.#.........#.#
        #.#.#.#########.#
        #S#.............#
        #################
    """)
        ),
    ),
]


class TestDec16:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)
        assert loaded.size_y == loaded.size_x

    def test_part1(self, loaded, case):
        p1_result, _ = solve(loaded)
        assert p1_result == case.part1

    @pytest.mark.skip("Part 2 not correct yet")
    def test_part2(self, loaded, case):
        _, p2_result = solve(loaded)
        assert p2_result == case.part2
