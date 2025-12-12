import io

import numpy as np
import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec13 import load, part1, part2, find_mirror

TEST_INPUT = io.StringIO("""\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""")

PART1_RESULT = 405
PART2_RESULT = 400


class TestDec13:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 2
        assert all(isinstance(x, Board) for x in loaded)

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.parametrize(
        "grid,expected",
        [
            ([["#", ".", ".", "#"]], 2),
            (
                [
                    ["#", ".", ".", "#"],
                    ["#", ".", ".", "#"],
                ],
                2,
            ),
            (
                [
                    ["#", ".", ".", "#"],
                    [".", "#", "#", "."],
                    ["#", ".", ".", "#"],
                ],
                2,
            ),
            (
                [
                    ["#", ".", "#", "#", ".", ".", "#", "#", "."],
                    [".", ".", "#", ".", "#", "#", ".", "#", "."],
                    ["#", "#", ".", ".", ".", ".", ".", ".", "#"],
                    ["#", "#", ".", ".", ".", ".", ".", ".", "#"],
                    [".", ".", "#", ".", "#", "#", ".", "#", "."],
                    [".", ".", "#", "#", ".", ".", "#", "#", "."],
                    ["#", ".", "#", ".", "#", "#", ".", "#", "."],
                ],
                5,
            ),
        ],
    )
    def test_find_mirror(self, grid, expected):
        grid = np.array(grid)
        assert find_mirror(grid) == expected

    @pytest.mark.skip(reason="Not implemented")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
