import io
import textwrap
from collections import namedtuple

import networkx as nx
import pytest

from ibidem.advent_of_code.y2025.dec11 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(5, None, io.StringIO(textwrap.dedent("""\
        aaa: you hhh
        you: bbb ccc
        bbb: ddd eee
        ccc: ddd eee fff
        ddd: ggg
        eee: out
        fff: out
        ggg: out
        hhh: ccc fff iii
        iii: out
    """))),
    Case(None, 2, io.StringIO(textwrap.dedent("""\
        svr: aaa bbb
        aaa: fft
        fft: ccc
        bbb: tty
        tty: ccc
        ccc: ddd eee
        ddd: hub
        hub: fff
        eee: dac
        dac: fff
        fff: ggg hhh
        ggg: out
        hhh: out
    """))),
]


class TestDec11():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, nx.Graph)

    def test_part1(self, loaded, case):
        if case.part1 is None:
            return
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        if case.part2 is None:
            return
        result = part2(loaded)
        assert result == case.part2
