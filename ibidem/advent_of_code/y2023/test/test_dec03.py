import io

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec03 import load, part1, part2

TEST_INPUT = io.StringIO("""\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""")

SPECIAL_CASE = io.StringIO("""\
.......
123.876
...#...
.......
""")

PART1_RESULT = 4361
PART2_RESULT = 467835


class TestDec03:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def special(self):
        SPECIAL_CASE.seek(0)
        return SPECIAL_CASE

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded: Board):
        assert loaded.size_x == 10
        assert loaded.size_y == 10

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_special(self, special):
        input = load(special)
        result = part1(input)
        assert result == 999

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
