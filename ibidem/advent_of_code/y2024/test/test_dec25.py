import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec25 import load, part1

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        3,
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....
        
        #####
        ##.##
        .#.##
        ...##
        ...#.
        ...#.
        .....
        
        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####
        
        .....
        .....
        #.#..
        ###..
        ###.#
        ###.#
        #####
        
        .....
        .....
        .....
        #....
        #.#..
        #.#.#
        #####
        
        #####
        #####
        ####.
        #.#..
        .....
        .....
        .....
        
        .....
        .....
        .....
        #..#.
        #.###
        #####
        #####
    """)
        ),
    ),
]


class TestDec25:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert loaded
        keys, locks = loaded
        assert len(keys) == 4
        assert len(locks) == 3
        assert (5, 0, 2, 1, 3) in keys
        assert (3, 1, 2, 3, 2) in keys
        assert (0, 5, 3, 4, 3) in locks
        assert (3, 2, 3, 2, 1) in locks

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
