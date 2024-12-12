import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec12 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(140, NotImplemented, io.StringIO(textwrap.dedent("""\
        AAAA
        BBCD
        BBCC
        EEEC
    """))),
    Case(772, NotImplemented, io.StringIO(textwrap.dedent("""\
        OOOOO
        OXOXO
        OOOOO
        OXOXO
        OOOOO
    """))),
    Case(1930, NotImplemented, io.StringIO(textwrap.dedent("""\
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
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
