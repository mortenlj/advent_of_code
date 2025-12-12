import io

import pytest

from ibidem.advent_of_code.y2021.dec14 import load, part1, part2, solve_step, seed

TEST_INPUT = io.StringIO("""\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""")

PART1_RESULT = 1588
PART2_RESULT = 2188189693529


class TestDec14:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        start, rules = loaded
        assert start == ["N", "N", "C", "B"]
        assert len(rules) == 16
        assert rules[("C", "N")] == "C"

    def test_part1(self, loaded):
        result = part1(*loaded)
        assert result == PART1_RESULT

    @pytest.mark.parametrize(
        "template, result",
        (
            ("NBCCNBBBCBHCB", "NBBBCNCCNBBNBNBBCHBHHBCHB"),
            (
                "NBBBCNCCNBBNBNBBCHBHHBCHB",
                "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB",
            ),
        ),
    )
    def test_solve_step(self, template, result, loaded):
        _, rules = loaded
        actual = solve_step(0, seed(template), rules)
        assert actual == seed(result)

    def test_part2(self, loaded):
        result = part2(*loaded)
        assert result == PART2_RESULT
