import pytest

from ibidem.advent_of_code.y2020.dec15 import *


class TestDec15:
    @pytest.mark.parametrize(
        "input, expected",
        (
            ((0, 3, 6), 436),
            ((1, 3, 2), 1),
            ((2, 1, 3), 10),
            ((1, 2, 3), 27),
            ((2, 3, 1), 78),
            ((3, 2, 1), 438),
            ((3, 1, 2), 1836),
        ),
    )
    def test_part1(self, input, expected):
        actual = part1(input)
        assert actual == expected
