import pytest

from ibidem.advent_of_code.y2020.dec14 import Program2

PART2_PROGRAM = [
    "mask = 000000000000000000000000000000X1001X",
    "mem[42] = 100",
    "mask = 00000000000000000000000000000000X0XX",
    "mem[26] = 1",
]
PAR2_EXPECTED = 208


class TestDec14:
    @pytest.mark.parametrize(
        "instructions, expected", ((PART2_PROGRAM, PAR2_EXPECTED),)
    )
    def test_program2(self, instructions, expected):
        program = Program2()
        program.process(instructions)
        actual = program.calculate_sum()
        assert actual == expected
