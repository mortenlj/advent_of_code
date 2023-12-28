import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2023.dec25 import load, part1, part2

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(54, NotImplemented, io.StringIO(textwrap.dedent("""\
        jqt: rhn xhk nvd
        rsh: frs pzl lsr
        xhk: hfx
        cmg: qnr nvd lhk bvb
        rhn: xhk bvb hfx
        bvb: xhk hfx
        pzl: lsr hfx nvd
        qnr: nvd
        ntq: jqt hfx bvb xhk
        nvd: lhk
        lsr: lhk
        rzs: qnr cmg lsr rsh
        frs: qnr lhk lsr
    """))),
]


class TestDec25():
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    @pytest.mark.skip(reason="Not implemented")
    def test_load(self, loaded):
        assert loaded
        
    @pytest.mark.skip(reason="Not implemented")
    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip(reason="Not implemented")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
