import io

import pytest

from ibidem.advent_of_code.y2022.dec08 import load, part1, part2

TEST_INPUT = io.StringIO("""\
30373
25512
65332
33549
35390
""")

PART1_RESULT = 21
PART2_RESULT = 8


class TestDec08():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded
        assert loaded.size_x == 5
        assert loaded.size_y == 5

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
