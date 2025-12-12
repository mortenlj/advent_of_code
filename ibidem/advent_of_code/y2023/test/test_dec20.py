import collections
import io
import textwrap
from collections import namedtuple
from queue import Queue

import pytest

from ibidem.advent_of_code.y2023.dec20 import load, part1, part2

Case = namedtuple("Case", "part1 part2 modules_length input")

TEST_INPUTS = [
    Case(
        32000000,
        NotImplemented,
        5,
        io.StringIO(
            textwrap.dedent("""\
        broadcaster -> a, b, c
        %a -> b
        %b -> c
        %c -> inv
        &inv -> a
    """)
        ),
    ),
    Case(
        11687500,
        NotImplemented,
        6,
        io.StringIO(
            textwrap.dedent("""\
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
    """)
        ),
    ),
    Case(
        1250000,
        2,
        3,
        io.StringIO(
            textwrap.dedent("""\
        broadcaster -> a
        %a -> rx
    """)
        ),
    ),
]


class TestDec20:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded, case):
        deque, modules = loaded
        assert isinstance(deque, collections.deque)
        assert len(modules) == case.modules_length

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        if case.part2 != NotImplemented:
            result = part2(loaded)
            assert result == case.part2
