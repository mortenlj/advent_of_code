import io

import pytest

from ibidem.advent_of_code.y2021.dec24 import load, part1

TEST_INPUT = io.StringIO("""\
inp w
add x w
mul w 0
mod x 2
inp w
add y w
mul w 0
mod y 3
add z x
mul x 0
add z y
mul y 0
""")

PART1_RESULT = 89


class TestDec24():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return list(load(input))

    def test_load(self, loaded):
        assert len(loaded) == 12

    def test_part1(self, loaded):
        actual = part1(loaded)
        assert actual == PART1_RESULT
