import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec07 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        3749,
        11387,
        io.StringIO(
            textwrap.dedent("""\
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
    """)
        ),
    ),
]


class TestDec07:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 9
        assert len(loaded[0]) == 2
        assert len(loaded[0][1]) == 2
        assert len(loaded[1][1]) == 3

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
