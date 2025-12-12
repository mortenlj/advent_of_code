from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2020.dec19 import *

Case = namedtuple("TestCase", ["rules", "messages", "matches"])

CASE1 = Case(
    {
        r.name: r
        for r in (
            Rule("0", "((1) (2))"),
            Rule("1", "a"),
            Rule("2", "((1 3) | (3 1))"),
            Rule("3", "b"),
        )
    },
    ["aab", "aba", "aabb", "baa"],
    ["aab", "aba"],
)
CASE2 = Case(
    {
        r.name: r
        for r in (
            Rule("0", "(4 1 5)"),
            Rule("1", "((2 3) | (3 2))"),
            Rule("2", "((4 4) | (5 5))"),
            Rule("3", "((4 5) | (5 4))"),
            Rule("4", "a"),
            Rule("5", "b"),
        )
    },
    ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"],
    ["ababbb", "abbbab"],
)
CASE3 = Case(
    {
        r.name: r
        for r in (Rule("0", "1 15"), Rule("1", "a"), Rule("15", "b"), Rule("5", "x"))
    },
    ["ab", "aab", "abb", "aabb"],
    ["ab"],
)


class TestDec19:
    @pytest.mark.parametrize(
        "case",
        (
            CASE1,
            CASE2,
            CASE3,
        ),
    )
    def test_part1(self, case):
        actual = part1(case.rules, case.messages)
        assert actual == len(case.matches)

    @pytest.mark.parametrize(
        "input, pattern",
        (
            ("0: 1", "1"),
            ("0: 1 1", "(1 1)"),
            ("0: 12", "12"),
            ("0: 12 34", "(12 34)"),
            ("0: 12 | 34", "(12 | 34)"),
            ("0: 1 3 | 3 1", "((1 3) | (3 1))"),
        ),
    )
    def test_load_rule(self, input, pattern):
        rules = {}
        load_rule(input, rules, None)
        assert rules["0"].pattern == pattern

    @pytest.mark.parametrize(
        "line, pattern",
        (
            ("1", "1"),
            ("1 1", "(1 1)"),
            ("1 2 3", "(1 2 3)"),
            ("12", "12"),
            ("12 34", "(12 34)"),
        ),
    )
    def test_parse_plain_rule(self, line, pattern):
        actual = parse_plain_rule(line)
        assert actual == pattern

    @pytest.mark.parametrize(
        "line, pattern",
        (
            ("1 | 1", "(1 | 1)"),
            ("1 2 | 3 4", "((1 2) | (3 4))"),
            ("12 | 3 4", "(12 | (3 4))"),
        ),
    )
    def test_parse_split_rule(self, line, pattern):
        actual = parse_split_rule(line)
        assert actual == pattern
