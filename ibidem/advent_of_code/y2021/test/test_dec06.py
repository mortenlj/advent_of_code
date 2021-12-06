import io

import pytest

from ibidem.advent_of_code.y2021.dec06 import *

TEST_INPUT = io.StringIO("3,4,3,1,2")

PART1_RESULT = 5934
PART2_RESULT = 26984457539


class TestDec06():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    def test_part1(self, input):
        result = part1(input)
        assert result == PART1_RESULT
        
    def test_part2(self, input):
        result = part2(input)
        assert result == PART2_RESULT
