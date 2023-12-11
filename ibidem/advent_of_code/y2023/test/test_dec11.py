import io

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec11 import load, part1, part2, expand

TEST_INPUT = io.StringIO("""\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""")

EXPANDED = io.StringIO("""\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
""")

PART1_RESULT = 374
PART2_RESULT = ((10, 1030), (100, 8410))


class TestDec11():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def expanded(self):
        EXPANDED.seek(0)
        return EXPANDED

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)

    def test_expand(self, loaded, expanded):
        actual = expand(loaded)
        expected = Board.from_string(EXPANDED.getvalue())
        assert actual == expected

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.parametrize("expand, expected", PART2_RESULT)
    def test_part2(self, loaded, expand, expected):
        result = part2(loaded, expand)
        assert result == expected

    def test_alternative(self, loaded):
        assert part1(loaded) == part2(loaded, 2)
