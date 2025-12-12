import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2023.dec17 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        102,
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
    """)
        ),
    ),
]


class TestDec17:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert loaded

    @pytest.mark.skip(reason="No clue")
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip(reason="No clue")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
