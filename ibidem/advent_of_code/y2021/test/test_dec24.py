import io

import pytest

from ibidem.advent_of_code.y2021.dec24 import load, Alu, Registers

TEST_INPUT1 = io.StringIO("""\
inp z
inp x
mul z 3
eql z x
""")

TEST_INPUT2 = io.StringIO("""\
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
""")


class TestDec24():
    @pytest.fixture
    def input(self):
        TEST_INPUT1.seek(0)
        return TEST_INPUT1

    @pytest.fixture
    def loaded(self, input):
        return list(load(input))

    def test_load(self, loaded):
        assert len(loaded) == 4

    @pytest.mark.parametrize("inputs, expected", (
            ([1, 2], 0),
            ([1, 3], 1),
            ([2, 6], 1),
            ([2, 9], 0),
    ))
    def test_run1(self, inputs, expected):
        loaded = load(TEST_INPUT1)
        alu = Alu(loaded, inputs)
        alu.run()
        assert alu.z == expected

    @pytest.mark.parametrize("inputs, expected", (
            ([2], Registers(0, 0, 1, 0)),
            ([3], Registers(0, 0, 1, 1)),
            ([6], Registers(0, 1, 1, 0)),
            ([9], Registers(1, 0, 0, 1)),
    ))
    def test_run2(self, inputs, expected):
        loaded = load(TEST_INPUT2)
        alu = Alu(loaded, inputs)
        alu.run()
        assert alu.registers == expected
