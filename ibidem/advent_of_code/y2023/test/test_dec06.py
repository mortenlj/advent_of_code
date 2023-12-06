import io

import pytest
from ibidem.advent_of_code.y2023.dec06 import load1, part1, part2, load2

TEST_INPUT = io.StringIO("""\
Time:      7  15   30
Distance:  9  40  200
""")

PART1_RESULT = 288
PART2_RESULT = 71503


class TestDec06():
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
        assert len(loaded1) == 3
        assert loaded1[0] == (7, 9)
        assert loaded1[1] == (15, 40)
        assert loaded1[2] == (30, 200)

    def test_load2(self, loaded2):
        assert len(loaded2) == 2
        assert loaded2[0] == 71530
        assert loaded2[1] == 940200

    def test_part1(self, loaded1):
        result = part1(loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = part2(loaded2)
        assert result == PART2_RESULT
