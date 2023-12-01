import io

import pytest
from ibidem.advent_of_code.y2023.dec01 import load, part1, part2

TEST_INPUT1 = io.StringIO("""\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""")

TEST_INPUT2 = io.StringIO("""\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""")

PART1_RESULT = 142
PART2_RESULT = 281


class TestDec01:
    @pytest.fixture
    def input1(self):
        TEST_INPUT1.seek(0)
        return TEST_INPUT1

    @pytest.fixture
    def loaded1(self, input1):
        return load(input1)

    @pytest.fixture
    def input2(self):
        TEST_INPUT2.seek(0)
        return TEST_INPUT2

    @pytest.fixture
    def loaded2(self, input2):
        return load(input2)

    def test_part1(self, loaded1):
        result = part1(loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = part2(loaded2)
        assert result == PART2_RESULT
