import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2024.dec06 import load, part1, part2, find_things, Direction, Guard, distance_to_edge, \
    find_obstacle

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(41, NotImplemented, io.StringIO(textwrap.dedent("""\
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """))),
]


class TestDec06():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    @pytest.fixture
    def things(self, loaded):
        return find_things(loaded)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)
        assert loaded.size_y == 10
        assert loaded.size_x == 10

    def test_find_things(self, loaded):
        row_obstacles, col_obstacles, guard = find_things(loaded)
        assert row_obstacles[0] == [4]
        assert row_obstacles[1] == [9]
        assert col_obstacles[0] == [8]
        assert col_obstacles[1] == [6]
        assert guard.x == 4
        assert guard.y == 6
        assert guard.direction == Direction.UP

    @pytest.mark.parametrize("guard, expected", [
        (Guard(4, 6, Direction.UP), 6),
        (Guard(4, 6, Direction.DOWN), 3),
        (Guard(4, 6, Direction.LEFT), 4),
        (Guard(4, 6, Direction.RIGHT), 5),
        (Guard(7, 7, Direction.DOWN), 2),
    ], ids=str)
    def test_distance_to_edge(self, loaded, guard, expected):
        actual = distance_to_edge(guard, loaded)
        assert actual == expected

    @pytest.mark.parametrize("guard, expected", [
        (Guard(4, 6, Direction.UP), (4, 1)),
        (Guard(4, 6, Direction.DOWN), None),
        (Guard(4, 6, Direction.LEFT), (2, 6)),
        (Guard(4, 6, Direction.RIGHT), None),
        (Guard(2, 1, Direction.UP), None),
        (Guard(2, 1, Direction.DOWN), (2, 2)),
        (Guard(2, 1, Direction.LEFT), None),
        (Guard(2, 1, Direction.RIGHT), (8, 1)),
    ], ids=str)
    def test_find_obstacle(self, things, guard, expected):
        row_obstacles, col_obstacles, _ = things
        result = find_obstacle(guard, row_obstacles, col_obstacles)
        assert result == expected

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
