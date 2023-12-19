import io
import operator
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2023.dec19 import load, part1, part2, parse_step, Step, true_func, parse_part, Part

TestData = namedtuple('TestData', 'part1 part2 input')

TEST_INPUTS = [
    TestData(19114, NotImplemented, io.StringIO(textwrap.dedent("""\
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}
        
        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
    """))),
]


class TestDec19():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        workflows, parts = loaded
        assert len(workflows) == 11
        assert len(parts) == 5

    @pytest.mark.parametrize("step,expected", [
        ("s>2770:qs", Step("s", operator.gt, 2770, "qs")),
        ("m<1801:hdj", Step("m", operator.lt, 1801, "hdj")),
        ("R", Step("x", true_func, 0, "R")),
    ])
    def test_parse_step(self, step, expected):
        assert parse_step(step) == expected

    @pytest.mark.parametrize("part,expected,rating", [
        ("{x=787,m=2655,a=1222,s=2876}", Part(x=787, m=2655, a=1222, s=2876), 7540),
        ("{x=2036,m=264,a=79,s=2244}", Part(x=2036, m=264, a=79, s=2244), 4623),
        ("{x=2127,m=1623,a=2188,s=1013}", Part(x=2127, m=1623, a=2188, s=1013), 6951),
    ])
    def test_parse_part(self, part, expected, rating):
        actual = parse_part(part)
        assert actual == expected
        assert actual.rating() == rating

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1
        
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
