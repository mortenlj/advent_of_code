import io

import pytest

from ibidem.advent_of_code.y2022.dec01 import load, part1, part2

TEST_INPUT = io.StringIO("""\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""")

PART1_RESULT = 24000
PART2_RESULT = 45000


class TestDec01:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
