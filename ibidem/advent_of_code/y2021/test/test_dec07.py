import io
import pytest

from ibidem.advent_of_code.y2021.dec07 import load, part1, part2


TEST_INPUT = io.StringIO("16,1,2,0,4,2,7,1,2,14")

PART1_RESULT = 37
PART2_RESULT = 168


class TestDec07():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    def test_load(self, input):
        result = load(input)
        assert len(result) == 10
        
    def test_part1(self, input):
        result = part1(load(input))
        assert result == PART1_RESULT
        
    def test_part2(self, input):
        result = part2(load(input))
        assert result == PART2_RESULT
