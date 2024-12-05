import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec05 import load, part1, part2, sort_update, Rule, Page, Update

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(143, 123, io.StringIO(textwrap.dedent("""\
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13
        
        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """))),
]


class TestDec05():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        rules, updates = loaded
        assert len(rules) == 21
        assert len(updates) == 6
        assert rules[0].first.number == 47
        assert rules[0].second.number == 53
        assert updates[0].page_numbers == [75, 47, 61, 53, 29]
        assert updates[0].middle_page == 61

    @pytest.mark.parametrize("update,expected", [
        (Update([75, 97, 47, 61, 53]), Update([97, 75, 47, 61, 53])),
        (Update([61, 13, 29]), Update([61, 29, 13])),
        (Update([97, 13, 75, 29, 47]), Update([97, 75, 47, 29, 13])),
    ])
    def test_sort_update(self, loaded, update, expected):
        rules, _ = loaded
        actual = sort_update(update, rules)
        assert actual == expected

    @pytest.mark.parametrize("rule,update,expected", [
        (Rule(Page(97), Page(75)), [75, 97, 47, 61, 53], [97, 75, 47, 61, 53]),
        (Rule(Page(29), Page(13)), [61, 13, 29], [61, 29, 13]),
        (Rule(Page(47), Page(53)), [61, 13, 29], [61, 13, 29]),
        (Rule(Page(97), Page(13)), [61, 13, 29], [61, 13, 29]),
        (Rule(Page(75), Page(29)), [61, 13, 29], [61, 13, 29]),
        (Rule(Page(61), Page(13)), [97, 13, 75, 29, 47], [97, 13, 75, 29, 47]),
        (Rule(Page(53), Page(29)), [97, 13, 75, 29, 47], [97, 13, 75, 29, 47]),
    ])
    def test_sort_rule_update(self, rule, update, expected):
        actual = rule.sort_update(update)
        assert actual == expected

    def test_part1(self, loaded, case):
        result, _ = part1(loaded)
        assert result == case.part1

    @pytest.fixture
    def invalid(self, loaded, case):
        _, i = part1(loaded)
        return i

    def test_part2(self, loaded, case, invalid):
        result = part2(loaded, invalid)
        assert result == case.part2
