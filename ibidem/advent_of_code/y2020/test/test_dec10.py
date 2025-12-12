import pytest

from ibidem.advent_of_code.y2020.dec10 import *

TEST1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
TEST2 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
]

RESULT1 = 7 * 5
RESULT2 = 22 * 10

ARR1 = 8
ARR2 = 19208


class TestDec10:
    @pytest.mark.parametrize("input, expected", ((TEST1, RESULT1), (TEST2, RESULT2)))
    def test_part1(self, input, expected):
        actual = part1(input)
        assert actual == expected

    @pytest.mark.parametrize("input, expected", ((TEST1, ARR1), (TEST2, ARR2)))
    def test_part2(self, input, expected):
        actual = part2(input)
        assert actual == expected
