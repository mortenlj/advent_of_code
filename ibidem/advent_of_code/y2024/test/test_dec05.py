import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec05 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(143, NotImplemented, io.StringIO(textwrap.dedent("""\
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
        
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
