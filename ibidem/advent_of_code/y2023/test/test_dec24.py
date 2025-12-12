import io
import textwrap
from collections import namedtuple

import pytest
from Geometry3D import HalfLine

from ibidem.advent_of_code.y2023.dec24 import load, part1, part2

Case = namedtuple("Case", "part1 limit part2 input")

TEST_INPUTS = [
    Case(
        2,
        (7, 27),
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        19, 13, 30 @ -2,  1, -2
        18, 19, 22 @ -1, -1, -2
        20, 25, 34 @ -2, -2, -4
        12, 31, 28 @ -1, -2, -1
        20, 19, 15 @  1, -5, -3
    """)
        ),
    ),
]


class TestDec24:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 5
        assert isinstance(loaded[0], HalfLine)
        assert isinstance(loaded[-1], HalfLine)

    @pytest.mark.skip(reason="Not implemented correctly/completely")
    def test_part1(self, loaded, case):
        result = part1(loaded, case.limit)
        assert result == case.part1

    @pytest.mark.skip(reason="Not implemented")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
