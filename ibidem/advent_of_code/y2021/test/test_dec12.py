import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2021.dec12 import load, part1, part2

Case = namedtuple("Case", ("result", "input"))

PART1_TESTS = [
    Case(10, io.StringIO(textwrap.dedent("""\
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
        """))),
    Case(19, io.StringIO(textwrap.dedent("""\
        dc-end
        HN-start
        start-kj
        dc-start
        dc-HN
        LN-dc
        HN-end
        kj-sa
        kj-HN
        kj-dc
        """))),
    Case(226, io.StringIO(textwrap.dedent("""\
        fs-end
        he-DX
        fs-he
        start-DX
        pj-DX
        end-zg
        zg-sl
        zg-pj
        pj-he
        RW-he
        fs-DX
        pj-RW
        zg-RW
        start-pj
        he-WI
        zg-he
        pj-fs
        start-RW
        """))),
]

PART2_RESULT = NotImplemented


class TestDec12():
    @pytest.mark.parametrize("case", PART1_TESTS)
    def test_part1(self, case):
        result = part1(load(case.input))
        assert result == case.result

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
