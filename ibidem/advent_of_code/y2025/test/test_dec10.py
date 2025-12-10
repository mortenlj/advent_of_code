import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec10 import load, part1, part2, Machine

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(7, 33, io.StringIO(textwrap.dedent("""\
        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    """))),
]


class TestDec10():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 3
        machine = loaded[0]
        assert isinstance(machine, Machine)
        assert machine.target == 96
        assert len(machine.buttons) == 6
        assert machine.buttons[0] == 16
        assert machine.buttons[1] == 80
        assert machine.buttons[2] == 32
        assert machine.buttons[3] == 48
        assert machine.buttons[4] == 160
        assert machine.buttons[5] == 192
        assert machine.joltage == (3, 5, 4, 7)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
