
import pytest

from ibidem.advent_of_code.y2021.dec03 import *

TEST_INPUT = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

PART1_RESULT = 198


class TestDec03():
    def test_part1(self):
        board = Board.from_string(TEST_INPUT, fill_value=0, dtype=np.int_)
        result = part1(board)
        assert result == PART1_RESULT
        
    def test_part2(self):
        pass
