import io

import pytest

from ibidem.advent_of_code.y2022.dec11 import load, part1, part2, make_operation, play_monkey_round

TEST_INPUT = io.StringIO("""\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""")

PART1_RESULT = 10605
PART2_RESULT = 2713310158


class TestDec11():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded
        assert len(loaded) == 4
        assert loaded[0].items == [79, 98]
        assert loaded[2].index == 2

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.skip(reason="Too much worry")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT

    @pytest.mark.parametrize(["left", "op", "right", "doc", "result"], [
        ("old", "*", "old", "is multiplied by itself", 100),
        ("old", "*", "19", "is multiplied by 19", 190),
        ("old", "+", "6", "increases by 6", 16),
    ])
    def test_make_operation(self, left, op, right, doc, result):
        func = make_operation(left, op, right)
        actual = func(10)
        assert actual == result
        assert func.__doc__ == doc

    def test_play_monkey_round(self, loaded):
        monkeys = loaded
        play_monkey_round(monkeys, worry_level_managed=True)
        assert monkeys[0].items == [20, 23, 27, 26]
        assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]
        assert monkeys[2].items == []
        assert monkeys[3].items == []
