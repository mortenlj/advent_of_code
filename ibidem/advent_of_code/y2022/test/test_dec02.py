import io

import pytest

from ibidem.advent_of_code.y2022.dec02 import load1, part1, part2, Play, load2, Outcome

TEST_INPUT = io.StringIO("""\
A Y
B X
C Z
""")

PART1_RESULT = 15
PART2_RESULT = 12


class TestDec02():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded1(self, input):
        return load1(input)

    @pytest.fixture
    def loaded2(self, input):
        return load2(input)

    def test_load1(self, loaded1):
        assert len(loaded1) == 3  # NOQA
        assert loaded1[0][0] == Play.Rock
        assert loaded1[0][1] == Play.Paper
        assert loaded1[1][0] == Play.Paper
        assert loaded1[1][1] == Play.Rock
        assert loaded1[2][0] == Play.Scissors
        assert loaded1[2][1] == Play.Scissors

    def test_load2(self, loaded2):
        assert len(loaded2) == 3  # NOQA
        assert loaded2[0][0] == Play.Rock
        assert loaded2[0][1] == Outcome.Draw
        assert loaded2[1][0] == Play.Paper
        assert loaded2[1][1] == Outcome.Loss
        assert loaded2[2][0] == Play.Scissors
        assert loaded2[2][1] == Outcome.Win

    def test_part1(self, loaded1):
        result = part1(loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = part2(loaded2)
        assert result == PART2_RESULT
