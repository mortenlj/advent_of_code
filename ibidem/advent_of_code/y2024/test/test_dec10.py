import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec10 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        36,
        81,
        io.StringIO(
            textwrap.dedent("""\
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
    """)
        ),
    ),
]


class TestDec10:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)
        assert loaded.size_y == 8
        assert loaded.size_x == 8
        assert loaded.get(1, 1) == 8

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
