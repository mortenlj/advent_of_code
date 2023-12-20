import collections
import io
import textwrap
from collections import namedtuple
from queue import Queue

import pytest

from ibidem.advent_of_code.y2023.dec20 import load, part1, part2

TestData = namedtuple('TestData', 'part1 part2 modules_length input')

TEST_INPUTS = [
    TestData(32000000, NotImplemented, 5, io.StringIO(textwrap.dedent("""\
        broadcaster -> a, b, c
        %a -> b
        %b -> c
        %c -> inv
        &inv -> a
    """))),
    TestData(11687500, NotImplemented, 6, io.StringIO(textwrap.dedent("""\
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
    """))),
]


class TestDec20():
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
