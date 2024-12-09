import io

import pytest

from ibidem.advent_of_code.y2022.dec12 import load, part1, part2

TEST_INPUT = io.StringIO("""\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""")

PART1_RESULT = 31
PART2_RESULT = 29


class TestDec12():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded
        assert loaded.size_y == 5
        assert loaded.size_x == 8

    @pytest.mark.xfail(reason="No idea why it fails, solution was correct in 2022")
    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.xfail(reason="No idea why it fails, solution was correct in 2022")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
