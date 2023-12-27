import io
import textwrap
from collections import namedtuple

import pytest
from Geometry3D import Point

from ibidem.advent_of_code.y2023.dec22 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(5, NotImplemented, io.StringIO(textwrap.dedent("""\
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
    """))),
]


class TestDec22():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 7
        first_brick = loaded[0]
        assert first_brick.start == Point(1, 0, 1)
        assert first_brick.end == Point(1, 2, 1)
        assert first_brick.length == 2

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip(reason="Not implemented")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
