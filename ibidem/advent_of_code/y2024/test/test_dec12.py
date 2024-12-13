import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec12 import load, solve

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(140, 80, io.StringIO(textwrap.dedent("""\
        AAAA
        BBCD
        BBCC
        EEEC
    """))),
    Case(772, 436, io.StringIO(textwrap.dedent("""\
        OOOOO
        OXOXO
        OOOOO
        OXOXO
        OOOOO
    """))),
    Case(1930, 1206, io.StringIO(textwrap.dedent("""\
        RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE
    """))),
    Case(NotImplemented, 236, io.StringIO(textwrap.dedent("""\
        EEEEE
        EXXXX
        EEEEE
        EXXXX
        EEEEE
    """))),
    Case(NotImplemented, 368, io.StringIO(textwrap.dedent("""\
        AAAAAA
        AAABBA
        AAABBA
        ABBAAA
        ABBAAA
        AAAAAA
    """))),
]


class TestDec12():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)

    def test_solve1(self, loaded, case):
        if case.part1 == NotImplemented:
            pytest.skip()
        p1_result, _ = solve(loaded)
        assert p1_result == case.part1

    def test_solve2(self, loaded, case):
        _, p2_result = solve(loaded)
        assert p2_result == case.part2
