import io
from collections import deque

import pytest

from ibidem.advent_of_code.y2021.dec10 import (
    load,
    part1,
    part2,
    completion_score,
    Pairs,
)

TEST_INPUT = io.StringIO("""\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""")

PART1_RESULT = 26397
PART2_RESULT = 288957


class TestDec10:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 10

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT

    @pytest.mark.parametrize(
        "line, expected",
        (
            ("}}]])})]", 288957),
            (")}>]})", 5566),
            ("}}>}>))))", 1480781),
            ("]]}}]}]}>", 995444),
            ("])}>", 294),
        ),
    )
    def test_completion_score(self, line, expected):
        my_line = (Pairs.get(c).open for c in reversed(line))
        stack = deque(Pairs.get(c) for c in my_line)
        actual = completion_score(stack)
        assert actual == expected
