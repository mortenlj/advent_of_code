import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec14 import load, part1, part2, tilt_column, calculate_load

TestData = namedtuple('TestData', 'part1 part2 input')

TEST_INPUTS = [
    TestData(136, 64, io.StringIO(textwrap.dedent("""\
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
"""))),
]


class TestDec14():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2

    @pytest.mark.parametrize('column,expected', [
        ([".", ".", "O"], ["O", ".", "."]),
        (["#", ".", "O"], ["#", "O", "."]),
        ([".", "#", "O"], [".", "#", "O"]),
        ([".", ".", "O", ".", ".", "O"], ["O", "O", ".", ".", ".", "."]),
        ([".", ".", "O", "#", ".", "O"], ["O", ".", ".", "#", "O", "."]),
        ([".", "#", "O", "#", ".", "O"], [".", "#", "O", "#", "O", "."]),
    ])
    def test_tilt_column(self, column, expected):
        actual = tilt_column(column)
        assert actual == expected

    @pytest.mark.parametrize('column,expected', [
        (["O", ".", "."], 3),
        (["#", "O", "."], 2),
        ([".", "#", "O"], 1),
        (["O", "O", ".", ".", ".", "."], 11),
        (["O", ".", ".", "#", "O", "."], 8),
        ([".", "#", "O", "#", "O", "."], 6),
    ])
    def test_calculate_load(self, column, expected):
        actual = calculate_load(column)
        assert actual == expected
