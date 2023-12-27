import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec23 import load, part1, part2, find_start_and_end, Node

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(94, 154, io.StringIO(textwrap.dedent("""\
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
    """))),
]


class TestDec23():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)

    def test_find_position(self, loaded):
        expected_start = (1, 0)
        expected_end = (21, 22)
        actual_start, actual_end = find_start_and_end(loaded)
        assert actual_start == expected_start
        assert actual_end == expected_end

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2

    def test_node_visited(self):
        node = Node(0, 0)
        assert not node.visited((1, 0))
        assert not node.visited((0, 1))
        assert node.visited((0, 0))
        node = Node(0, 1, node)
        assert node.visited((0, 0))
        assert node.visited((0, 1))
        node = Node(0, 2, node)
        assert node.visited((0, 0))
        assert node.visited((0, 1))
        assert node.visited((0, 2))
