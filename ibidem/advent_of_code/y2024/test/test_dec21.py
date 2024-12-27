import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec21 import load, part1, part2, make_sequence

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(126384, NotImplemented, io.StringIO(textwrap.dedent("""\
        029A
        980A
        179A
        456A
        379A
    """))),
]


class TestDec21():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 5
        assert loaded[0] == "029A"

    @pytest.mark.parametrize("input, expected_complexity", [
        ("029A", 68 * 29),
        ("980A", 60 * 980),
        ("179A", 68 * 179),
        ("456A", 64 * 456),
        ("379A", 64 * 379),
    ])
    def test_make_sequence(self, input, expected_complexity):
        output = make_sequence(input)
        length = len(output)
        numeric = int(input[:-1])
        assert expected_complexity == length * numeric

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip("Not started")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
