import io

import pytest

from ibidem.advent_of_code.y2022.dec21 import load, part1, part2

TEST_INPUT = io.StringIO("""\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""")

PART1_RESULT = 152
PART2_RESULT = 301


class TestDec21:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded["dbpl"].value(loaded) == 5
        assert loaded["root"].left_name == "pppw"
        assert loaded["root"].right_name == "sjmn"
        assert loaded["root"].op(1, 2) == 3

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.xfail(reason="Not implemented")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
