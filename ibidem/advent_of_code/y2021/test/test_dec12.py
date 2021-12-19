import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2021.dec12 import load, part1, part2

Case = namedtuple("Case", ("p1_result", "p2_result", "input"))

TESTS = [
    Case(10, 36, io.StringIO(textwrap.dedent("""\
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
        """))),
    Case(19, 103, io.StringIO(textwrap.dedent("""\
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
    Case(226, 3509, io.StringIO(textwrap.dedent("""\
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


class TestDec12():
    @pytest.mark.parametrize("case", TESTS)
    def test_part1(self, case):
        case.input.seek(0)
        result = part1(load(case.input))
        assert result == case.p1_result

    @pytest.mark.parametrize("case", TESTS)
    def test_part2(self, case):
        case.input.seek(0)
        result = part2(load(case.input))
        assert result == case.p2_result
