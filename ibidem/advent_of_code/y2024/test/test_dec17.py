import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec17 import load, part1, part2, Machine

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case("4,6,3,5,6,3,5,2,1,0", NotImplemented, io.StringIO(textwrap.dedent("""\
        Register A: 729
        Register B: 0
        Register C: 0
        
        Program: 0,1,5,4,3,0
    """))),
    Case("0,1,2", NotImplemented, io.StringIO(textwrap.dedent("""\
        Register A: 10
        Register B: 0
        Register C: 0
        
        Program: 5,0,5,1,5,4
    """))),
    Case("4,2,5,6,7,7,7,7,3,1,0", NotImplemented, io.StringIO(textwrap.dedent("""\
        Register A: 2024
        Register B: 0
        Register C: 0
        
        Program: 0,1,5,4,3,0
    """))),
    Case("5,7,3,0", 117440, io.StringIO(textwrap.dedent("""\
        Register A: 2024
        Register B: 0
        Register C: 0
        
        Program: 0,3,5,4,3,0
    """))),
]


class TestDec17():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Machine)
        assert loaded.ip == 0

    @pytest.mark.parametrize("in_a,in_b,in_c,program,exp_a,exp_b,exp_c,exp_output", [
        #If register C contains 9, the program 2,6 would set register B to 1.
        (0, 0, 9, [2, 6], None, 1, None, None),
        #If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
        (10, 0, 0, [5, 0, 5, 1, 5, 4], None, None, None, [0,1,2]),
        #If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
        (2024, 0, 0, [0, 1, 5, 4, 3, 0], 0, None, None, [4,2,5,6,7,7,7,7,3,1,0]),
        #If register B contains 29, the program 1,7 would set register B to 26.
        (0, 29, 0, [1, 7], None, 26, None, None),
        #If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
        (0, 2024, 43690, [4, 0], None, 44354, None, None),
    ])
    def test_machine(self, in_a, in_b, in_c, program, exp_a, exp_b, exp_c, exp_output):
        machine = Machine(in_a, in_b, in_c, program)
        output = machine.run()
        if exp_output is not None:
            assert output == exp_output
        if exp_a is not None:
            assert machine.a.value == exp_a
        if exp_b is not None:
            assert machine.b.value == exp_b
        if exp_c is not None:
            assert machine.c.value == exp_c

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        if case.part2 is NotImplemented:
            pytest.skip("Part 2 not implemented for this case")
        result = part2(loaded)
        assert result == case.part2
