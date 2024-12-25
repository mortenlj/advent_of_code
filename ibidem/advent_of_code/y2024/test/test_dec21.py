import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec21 import load, part1, part2, make_sequence, Numeric, Directional

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

    def test_numeric(self):
        n = Numeric()
        output = [n.next_press(c) for c in "029A"]
        assert "".join(output) == "<A^A>^^AvvvA"

    @pytest.mark.parametrize("input, expected", [
        ("<A^A>^^AvvvA", "<v<A>>^A<A>AvA<^AA>A<vAAA>^A"),
        ("v<<A>>^A<A>AvA<^AA>A<vAAA>^A", "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),
    ])
    def test_directional(self, input, expected):
        d = Directional()
        output = [d.next_press(c) for c in input]
        assert "".join(output) == expected

    @pytest.mark.skip("Entierly wrong approach")
    @pytest.mark.parametrize("input, expected", [
        ("029A", "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),
        ("980A", "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
        ("179A", "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
        ("456A", "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
        ("379A", "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
    ])
    def test_make_sequence(self, input, expected):
        output = make_sequence(input)
        assert output == expected
        length = len(output)
        numeric = int(input[:-1])
        assert length == numeric * len(input)

    @pytest.mark.skip("Entierly wrong approach")
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip("Not started")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
