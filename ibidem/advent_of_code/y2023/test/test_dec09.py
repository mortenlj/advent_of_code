import io
import pytest

from ibidem.advent_of_code.y2023.dec09 import load, part1, part2


TEST_INPUT = io.StringIO("""\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""")

PART1_RESULT = 114
PART2_RESULT = 2


class TestDec09():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 3
        assert len(loaded[0]) == 6
        
    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT
        
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
