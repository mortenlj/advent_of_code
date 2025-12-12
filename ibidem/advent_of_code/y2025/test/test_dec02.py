import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec02 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        1227775554,
        4174379265,
        io.StringIO(
            textwrap.dedent(
                """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
            )
        ),
    ),
]


class TestDec02:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 11
        assert loaded[0] == (11, 23)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
