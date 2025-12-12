import io

import pytest

from ibidem.advent_of_code.y2021.dec17 import load, part1, part2

TEST_INPUT = io.StringIO("""target area: x=20..30, y=-10..-5""")

PART1_RESULT = 45
PART2_RESULT = 112


class TestDec17:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded.upper_left.x == 20
        assert loaded.upper_left.y == -5
        assert loaded.lower_right.x == 30
        assert loaded.lower_right.y == -10

    def test_part1_testdata(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.parametrize(
        "input, expected", ((io.StringIO("target area: x=269..292, y=-68..-44"), 2278),)
    )
    def test_part1_realdata(self, input, expected):
        loaded = load(input)
        result = part1(loaded)
        assert result == expected

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
