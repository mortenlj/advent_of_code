import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec13 import load, part1, part2, Vector, Coordinate, ClawMachine

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    # Part 2 answer from own testing
    Case(480, 875318608908, io.StringIO(textwrap.dedent("""\
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        
        Button A: X+26, Y+66
        Button B: X+67, Y+21
        Prize: X=12748, Y=12176
        
        Button A: X+17, Y+86
        Button B: X+84, Y+37
        Prize: X=7870, Y=6450
        
        Button A: X+69, Y+23
        Button B: X+27, Y+71
        Prize: X=18641, Y=10279
    """))),
]


class TestDec13():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    @pytest.fixture
    def adjusted(self, case):
        return load(case.input, adjust=True)

    def test_load(self, loaded):
        assert len(loaded) == 4
        assert loaded[1].button_a == Vector(26, 66)
        assert loaded[1].button_b == Vector(67, 21)
        assert loaded[1].prize == Coordinate(12748, 12176)
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, adjusted, case):
        result = part2(adjusted)
        assert result == case.part2

    def test_solve(self):
        machine = ClawMachine(Vector(2, 0), Vector(3, 0), Coordinate(11, 0), {})
        result = machine.solve()
        assert result == 6
