import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec01 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(11, 31, io.StringIO(textwrap.dedent("""\
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """))),
]


class TestDec01():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        loaded = list(loaded)
        assert len(loaded) == 2
        assert all(len(p) == 6 for p in loaded)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
