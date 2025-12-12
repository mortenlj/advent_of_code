import io

import pytest

from ibidem.advent_of_code.y2022.dec14 import load, part1, part2

TEST_INPUT = io.StringIO("""\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""")

PART1_RESULT = 24
PART2_RESULT = 93


class TestDec14:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 2
        assert len(loaded[0]) == 3
        assert len(loaded[1]) == 4

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
