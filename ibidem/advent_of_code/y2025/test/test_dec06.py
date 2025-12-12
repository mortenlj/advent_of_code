import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec06 import load1, part1, part2, load2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        4277556,
        3263827,
        io.StringIO(
            textwrap.dedent("""\
        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   +  
    """)
        ),
    ),
]


class TestDec06:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded1(self, case):
        return load1(case.input)

    def test_load1(self, loaded1):
        assert loaded1
        assert len(loaded1) == 4
        assert len(loaded1[0]) == 4
        assert isinstance(loaded1[0][0], int)
        assert isinstance(loaded1[-1][0], str)

    def test_part1(self, loaded1, case):
        result = part1(loaded1)
        assert result == case.part1

    @pytest.fixture
    def loaded2(self, case):
        return load2(case.input)

    def test_load2(self, loaded2):
        assert loaded2
        assert len(loaded2) == 4

    def test_part2(self, loaded2, case):
        result = part2(loaded2)
        assert result == case.part2
