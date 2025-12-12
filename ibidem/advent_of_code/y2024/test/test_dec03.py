import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec03 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input1 input2")

TEST_INPUTS = [
    Case(
        161,
        48,
        io.StringIO(
            textwrap.dedent(
                "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
            )
        ),
        io.StringIO(
            textwrap.dedent(
                "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
            )
        ),
    ),
]


class TestDec03:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input1.seek(0)
        request.param.input2.seek(0)
        return request.param

    @pytest.fixture
    def loaded1(self, case):
        return load(case.input1)

    @pytest.fixture
    def loaded2(self, case):
        return load(case.input2)

    def test_load(self, loaded1):
        assert isinstance(loaded1, str)

    def test_part1(self, loaded1, case):
        result = part1(loaded1)
        assert result == case.part1

    def test_part2(self, loaded2, case):
        result = part2(loaded2)
        assert result == case.part2
