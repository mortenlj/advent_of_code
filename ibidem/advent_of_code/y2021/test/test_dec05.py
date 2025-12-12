import io

import pytest

from ibidem.advent_of_code.y2021.dec05 import *
from ibidem.advent_of_code.y2021.dec05 import _load_input

TEST_INPUT = io.StringIO("""\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""")

PART1_RESULT = 5
PART2_RESULT = 12


class TestDec05:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def without_diagonal_lines(self, input):
        lines = _load_input(input, with_diagonal=False)
        return lines

    @pytest.fixture
    def with_diagonal_lines(self, input):
        lines = _load_input(input, with_diagonal=True)
        return lines

    def test_load_input_without_diagonal(self, input):
        lines = list(_load_input(input, with_diagonal=False))
        assert len(lines) == 6
        assert lines[0].start == Pos(0, 9)
        assert lines[0].end == Pos(5, 9)
        assert lines[-1].start == Pos(3, 4)
        assert lines[-1].end == Pos(1, 4)

    def test_load_input_with_diagonal(self, input):
        lines = list(_load_input(input, with_diagonal=True))
        assert len(lines) == 10
        assert lines[0].start == Pos(0, 9)
        assert lines[0].end == Pos(5, 9)
        assert lines[-1].start == Pos(5, 5)
        assert lines[-1].end == Pos(8, 2)

    def test_part1(self, without_diagonal_lines):
        result = part1(list(without_diagonal_lines))
        assert result == PART1_RESULT

    def test_part2(self, with_diagonal_lines):
        result = part1(list(with_diagonal_lines))
        assert result == PART2_RESULT


class TestLine:
    def test_hor_line(self):
        line = Line("0,0 -> 2,0")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 0), Pos(1, 0), Pos(2, 0)}

    def test_ver_line(self):
        line = Line("0,0 -> 0,2")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 0), Pos(0, 1), Pos(0, 2)}

    def test_reversed_line(self):
        line = Line("0,2 -> 0,0")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 2), Pos(0, 1), Pos(0, 0)}


class TestDiagonalLine:
    def test_down_right(self):
        line = DiagonalLine("0,0 -> 2,2")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 0), Pos(1, 1), Pos(2, 2)}

    def test_down_left(self):
        line = DiagonalLine("2,0 -> 0,2")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 2), Pos(1, 1), Pos(2, 0)}

    def test_up_right(self):
        line = DiagonalLine("0,2 -> 2,0")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 2), Pos(1, 1), Pos(2, 0)}

    def test_up_left(self):
        line = DiagonalLine("2,2 -> 0,0")
        actual_points = set(line.points())
        assert actual_points == {Pos(0, 0), Pos(1, 1), Pos(2, 2)}
