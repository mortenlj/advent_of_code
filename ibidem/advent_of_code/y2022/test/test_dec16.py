import io

import pytest

from ibidem.advent_of_code.y2022.dec16 import load, part1, part2

TEST_INPUT = io.StringIO("""\
""")

PART1_RESULT = NotImplemented
PART2_RESULT = NotImplemented


class TestDec16():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
