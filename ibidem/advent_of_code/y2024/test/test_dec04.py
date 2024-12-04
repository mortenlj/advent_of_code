import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec04 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(18, 9, io.StringIO(textwrap.dedent("""\
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
    """))),
]


class TestDec04():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert loaded
        assert loaded.size_y == 10
        assert loaded.size_y == 10

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
