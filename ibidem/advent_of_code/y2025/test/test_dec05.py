import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2025.dec05 import load, part1, part2, Fresh

Case = namedtuple('Case', 'part1 part2 input')

TEST_INPUTS = [
    Case(3, 14, io.StringIO(textwrap.dedent("""\
        3-5
        10-14
        16-20
        12-18

        1
        5
        8
        11
        17
        32
    """))),
    Case(0, 16, io.StringIO(textwrap.dedent("""\
        3-5
        2-6
        10-14
        16-20
        12-18
    """))),
    Case(0, 15, io.StringIO(textwrap.dedent("""\
        3-5
        2-5
        10-14
        16-20
        12-18
    """))),
    Case(0, 15, io.StringIO(textwrap.dedent("""\
        3-5
        3-6
        10-14
        16-20
        12-18
    """))),
    Case(0, 18, io.StringIO(textwrap.dedent("""\
        1-9
        5-9
        1-5
        2-8
        2-9
        1-8
        11-19
        15-19
        11-15
        12-18
        12-19
        11-18
    """))),
    Case(0, 18, io.StringIO(textwrap.dedent("""\
        1-5
        1-8
        1-9
        11-15
        11-18
        11-19
        12-18
        12-19
        15-19
        2-8
        2-9
        5-9
    """))),
    Case(0, 19, io.StringIO(textwrap.dedent("""\
        1-5
        1-8
        1-9
        11-15
        11-18
        11-19
        12-18
        12-19
        15-19
        2-8
        2-9
        5-9
        1-19
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

    def test_load(self, loaded, case):
        if case.part1 == 0:
            return
        fresh, ingredients = loaded
        assert len(ingredients) == 6
        assert len(fresh) == 4
        assert all(isinstance(v, Fresh) for v in fresh)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
