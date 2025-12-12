import io
import pytest

from ibidem.advent_of_code.y2021.dec09 import load, part1, part2, find_basin

LOW_POINTS = [(1, 0), (2, 2), (6, 4), (9, 0)]

TEST_INPUT = io.StringIO("""\
2199943210
3987894921
9856789892
8767896789
9899965678
""")

PART1_RESULT = 15
PART2_RESULT = 1134


class TestDec09:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert (loaded.size_x, loaded.size_y) == (10, 5)
        assert loaded[1, 0] == 1
        assert loaded[6, 4] == 5

    def test_part1(self, loaded):
        result, low_points = part1(loaded)
        assert result == PART1_RESULT
        assert low_points == LOW_POINTS

    def test_find_basin(self, loaded):
        result = find_basin(loaded, (1, 0))
        assert result == 3

    def test_part2(self, loaded):
        result = part2(loaded, LOW_POINTS)
        assert result == PART2_RESULT
