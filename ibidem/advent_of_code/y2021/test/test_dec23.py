import io

import pytest

from ibidem.advent_of_code.y2021.dec23 import load, part1, part2

TEST_INPUT = io.StringIO("""\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""")

PART1_RESULT = 12521
PART2_RESULT = 44169


class TestDec23:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded

    @pytest.mark.xfail(reason="Solved on paper :D")
    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.xfail(reason="No clue for algorithm")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
