import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec11 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(55312, NotImplemented, io.StringIO(textwrap.dedent("125 17"))),
]


class TestDec11():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 2
        assert all(isinstance(v, int) for v in loaded)
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip("Takes forever, no target to compare to")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
