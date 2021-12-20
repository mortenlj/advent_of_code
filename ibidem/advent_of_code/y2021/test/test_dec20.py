import io

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2021.dec20 import load, part1, part2, pad

TEST_INPUT = io.StringIO("""\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""")

PART1_RESULT = 35
PART2_RESULT = 3351


class TestDec20():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        algo, board = loaded
        assert len(algo) == 512
        assert board.size_y == 5 + 9 * 2
        assert board.size_x == 5 + 9 * 2

    @pytest.mark.parametrize("x, y, expected_corners", (
            (0, 0, (".", ".", ".", "f")),
            (1, 1, ("a", "i", "c", "k")),
            (1, 0, (".", "e", ".", "g")),
            (0, 1, (".", ".", "b", "j")),
            (2, 2, ("f", "n", "h", "p")),
            (3, 3, ("k", ".", ".", ".")),
    ))
    def test_pad(self, x, y, expected_corners):
        board = Board.from_string("abcd\nefgh\nijkl\nmnop\n", fill_value=".")
        view = board.adjacent_view(x, y)
        padded = pad(view, x, y, board.grid)
        assert padded.shape == (3, 3)
        assert padded[0, 0] == expected_corners[0]
        assert padded[-1, 0] == expected_corners[1]
        assert padded[0, -1] == expected_corners[2]
        assert padded[-1, -1] == expected_corners[3]

    def test_part1(self, loaded):
        result = part1(*loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(*loaded)
        assert result == PART2_RESULT
