import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec19 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(6, 16, io.StringIO(textwrap.dedent("""\
        r, wr, b, g, bwu, rb, gb, br
        
        brwrr
        bggr
        gbbr
        rrbgbr
        ubwu
        bwurrg
        brgr
        bbrgwb
    """))),
]


class TestDec19():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 2
        towels, designs = loaded
        assert len(towels) == 8
        assert len(designs) == 8
        assert towels[0] == "r"
        assert towels[-1] == "br"
        assert designs[0] == "brwrr"
        assert designs[-1] == "bbrgwb"
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
