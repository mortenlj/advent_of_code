import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec18 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(NotImplemented, NotImplemented, io.StringIO(textwrap.dedent("""\
        5,4
        4,2
        4,5
        3,0
        2,1
        6,3
        2,4
        1,5
        0,6
        3,3
        2,6
        5,1
        1,2
        5,5
        2,5
        6,5
        1,4
        0,4
        6,4
        1,1
        6,1
        1,0
        0,5
        1,6
        2,0
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
        assert len(loaded) == 25
        assert len(loaded[0]) == 2
        assert loaded[0] == (5, 4)

    @pytest.mark.skip(reason="TODO")
    def test_part1(self, loaded, case):
        result = part1(loaded, (7,7), 12)
        assert result == case.part1

    @pytest.mark.skip(reason="TODO")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
