import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec22 import (
    load,
    part1,
    part2,
    next_secret_number,
    mix,
    prune,
)

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        37327623,
        23,
        io.StringIO(
            textwrap.dedent("""\
        1
        10
        100
        2024
    """)
        ),
    ),
]


class TestDec22:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 4
        assert loaded[0] == 1
        assert loaded[1] == 10
        assert loaded[2] == 100
        assert loaded[3] == 2024

    @pytest.mark.parametrize(
        "num, expected",
        [
            (123, 15887950),
            (15887950, 16495136),
            (16495136, 527345),
            (527345, 704524),
            (704524, 1553684),
            (1553684, 12683156),
            (12683156, 11100544),
            (11100544, 12249484),
            (12249484, 7753432),
            (7753432, 5908254),
        ],
    )
    def test_next_secret_number(self, num, expected):
        result = next_secret_number(num)
        assert result == expected

    @pytest.mark.parametrize(
        "num, mixval, expected",
        [
            (42, 15, 37),
        ],
    )
    def test_mix(self, num, mixval, expected):
        result = mix(num, mixval)
        assert result == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            (100000000, 16113920),
        ],
    )
    def test_prune(self, value, expected):
        result = prune(value)
        assert result == expected

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip("Not implemented")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
