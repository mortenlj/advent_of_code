import io
import operator
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec01 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        3,
        6,
        io.StringIO(
            textwrap.dedent("""\
        L68
        L30
        R48
        L5
        R60
        L55
        L1
        L99
        R14
        L82
    """)
        ),
    ),
]


class TestDec01:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 10
        assert loaded[0].op == operator.sub
        assert loaded[0].value == 68
        assert loaded[2].op == operator.add
        assert loaded[2].value == 48

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
