import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2023.dec15 import load, part1, part2, hash, focusing_power

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(1320, 145, io.StringIO(textwrap.dedent("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"))),
]


class TestDec15():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 11

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2

    @pytest.mark.parametrize("step,expected", [
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),

    ])
    def test_hash(self, step, expected):
        actual = hash(step)
        assert actual == expected

    @pytest.mark.parametrize("box_num,slot,focal_length,expected", [
        (1, 1, 1, 1),
        (1, 2, 2, 4),
        (4, 1, 7, 28),
        (4, 2, 5, 40),
        (4, 3, 6, 72),
    ])
    def test_focusing_power(self, box_num, slot, focal_length, expected):
        assert focusing_power(box_num, slot, focal_length) == expected
