import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec03 import load, part1, part2, part1_solve_bank, part2_solve_bank

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(357, 3121910778619, io.StringIO(textwrap.dedent("""\
        987654321111111
        811111111111119
        234234234234278
        818181911112111
    """))),
]


class TestDec03():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 4
        assert len(loaded[0]) == 15

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.parametrize(["bank", "expected"], (
        ([9,8,7,6,5,4,3,2,1,1,1,1,1,1,1], 98),
        ([8,1,1,1,1,1,1,1,1,1,1,1,1,1,9], 89),
        ([2,3,4,2,3,4,2,3,4,2,3,4,2,7,8], 78),
        ([8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], 92),
    ))
    def test_part1_solve_bank(self, bank, expected):
        actual = part1_solve_bank(bank)
        assert actual == expected

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2

    @pytest.mark.parametrize(["bank", "expected"], (
            ([9,8,7,6,5,4,3,2,1,1,1,1,1,1,1], 987654321111),
            ([8,1,1,1,1,1,1,1,1,1,1,1,1,1,9], 811111111119),
            ([2,3,4,2,3,4,2,3,4,2,3,4,2,7,8], 434234234278),
            ([8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], 888911112111),
    ))
    def test_part2_solve_bank(self, bank, expected):
        actual = part2_solve_bank(bank, 12)
        assert actual == expected
