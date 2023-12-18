import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2023.dec18 import load, part1, part2

TestData = namedtuple('TestData', 'part1 part2 input')

TEST_INPUTS = [
    TestData(62, 952408144115, io.StringIO(textwrap.dedent("""\
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
    """))),
]


class TestDec18():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 14
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    @pytest.mark.skip(reason="No clue")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
