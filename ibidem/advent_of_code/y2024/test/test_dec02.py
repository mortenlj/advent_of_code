import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec02 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(2, 4, io.StringIO(textwrap.dedent("""\
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """))),
]


class TestDec02():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 6
        assert all(isinstance(l, list) for l in loaded)
        assert all(all(isinstance(i, int) for i in l) for l in loaded)
        assert all(len(l) == 5 for l in loaded)
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
