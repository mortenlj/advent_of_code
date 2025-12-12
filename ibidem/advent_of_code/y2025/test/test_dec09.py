import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.util import Vector
from ibidem.advent_of_code.y2025.dec09 import (
    load,
    part1,
    part2,
    make_poly,
    inside,
    Polygon,
    Line,
)

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        50,
        24,
        io.StringIO(
            textwrap.dedent("""\
        7,1
        11,1
        11,7
        9,7
        9,5
        2,5
        2,3
        7,3
    """)
        ),
    ),
]


class TestDec09:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert len(loaded) == 8
        assert isinstance(loaded[0], Vector)

    @pytest.fixture
    def poly(self, loaded):
        return make_poly(loaded)

    @pytest.mark.parametrize(
        "p, expected",
        (
            (Vector(1, 1), True),
            (Vector(1, 2), True),
            (Vector(1, 3), True),
            (Vector(2, 1), True),
            (Vector(2, 2), True),
            (Vector(2, 3), True),
            (Vector(3, 1), True),
            (Vector(3, 2), True),
            (Vector(3, 3), True),
            (Vector(7, 3), False),
            (Vector(9, 7), False),
            (Vector(9, 5), False),
        ),
    )
    def test_poly_contains(self, p, expected):
        top_left = Vector(1, 1)
        top_right = Vector(3, 1)
        bottom_left = Vector(1, 3)
        bottom_right = Vector(3, 3)
        lines = [
            Line(top_left, top_right),
            Line(top_right, bottom_right),
            Line(bottom_right, bottom_left),
            Line(bottom_left, top_left),
        ]
        poly = Polygon(lines)
        assert (p in poly) == expected

    @pytest.mark.parametrize(
        "v1, v2, expected",
        (
            (Vector(1, 1), Vector(2, 2), False),
            (Vector(7, 3), Vector(11, 1), True),
            (Vector(9, 7), Vector(9, 5), True),
            (Vector(9, 5), Vector(2, 3), True),
        ),
    )
    def test_inside(self, poly, v1, v2, expected):
        assert inside(poly, v1, v2) == expected

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
