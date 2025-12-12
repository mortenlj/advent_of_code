import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec21 import load, part1, part2

Case = namedtuple("Case", "steps result input")

TEST_INPUTS = [
    Case(
        6,
        16,
        io.StringIO(
            textwrap.dedent("""\
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
    """)
        ),
    ),
]


class TestDec21:
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
        result = part1(loaded, case.steps)
        assert result == case.result

    @pytest.mark.skip(reason="Not implemented")
    def test_part2(self, loaded, case):
        result = part2(loaded, case.steps)
        assert result == case.result
