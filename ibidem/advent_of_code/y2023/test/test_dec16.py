import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2023.dec16 import load, part1, part2, handle_point, Beam, Direction

TestData = namedtuple('TestData', 'part1 part2 input')

TEST_INPUTS = [
    TestData(46, 51, io.StringIO(textwrap.dedent("""\
        .|...\\....
        |.-.\\.....
        .....|-...
        ........|.
        ..........
        .........\\
        ..../.\\\\..
        .-.-/..|..
        .|....-|.\\
        ..//.|....
    """))),
]


class TestDec16():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Board)

    @pytest.mark.parametrize('beam,char,expected', [
        (Beam(5, 5, Direction.UP), '|', [Beam(5, 4, Direction.UP)]),
        (Beam(5, 5, Direction.UP), '.', [Beam(5, 4, Direction.UP)]),
        (Beam(5, 5, Direction.UP), '-', [Beam(4, 5, Direction.LEFT), Beam(6, 5, Direction.RIGHT)]),
        (Beam(5, 5, Direction.UP), '/', [Beam(6, 5, Direction.RIGHT)]),
        (Beam(5, 5, Direction.UP), '\\', [Beam(4, 5, Direction.LEFT)]),
        (Beam(5, 5, Direction.LEFT), '|', [Beam(5, 4, Direction.UP), Beam(5, 6, Direction.DOWN)]),
    ])
    def test_handle_point(self, beam, char, expected):
        assert handle_point(beam, char) == expected

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
