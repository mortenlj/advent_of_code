import io

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2021.dec13 import load, part1

TEST_INPUT = io.StringIO("""\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

INITIAL_BOARD = Board.from_string("""\
00010010010
00001000000
00000000000
10000000000
00010000101
00000000000
00000000000
00000000000
00000000000
00000000000
01000010110
00001000000
00000010001
10000000000
10100000000
""", fill_value=0, dtype=int, growable=False)

PART1_RESULT = 17


class TestDec13():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        board, folds = loaded
        assert len(folds) == 2
        assert board == INITIAL_BOARD

    def test_part1(self, loaded):
        result = part1(*loaded)
        assert result == PART1_RESULT
