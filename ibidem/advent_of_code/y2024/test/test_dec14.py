import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec14 import load, part1, part2, Vector

Case = namedtuple("Case", "part1 part2 input, board_x, board_y")

TEST_INPUTS = [
    Case(
        12,
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        p=0,4 v=3,-3
        p=6,3 v=-1,-3
        p=10,3 v=-1,2
        p=2,0 v=2,-1
        p=0,0 v=1,3
        p=3,0 v=-2,-2
        p=7,6 v=-1,-3
        p=3,0 v=-1,-2
        p=9,3 v=2,3
        p=7,3 v=-1,2
        p=2,4 v=2,-3
        p=9,5 v=-3,-3
    """)
        ),
        11,
        7,
    ),
]


class TestDec14:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input, case.board_x, case.board_y)

    def test_load(self, loaded, case):
        robots, board = loaded
        assert len(robots) == 12
        assert robots[4].position == Vector(0, 0)
        assert robots[4].velocity == Vector(1, 3)
        assert robots[-1].position == Vector(9, 5)
        assert robots[-1].velocity == Vector(-3, -3)
        assert isinstance(board, Board)
        assert board.size_x == case.board_x
        assert board.size_y == case.board_y

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip(reason="Test case has no christmas tree")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
