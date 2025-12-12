import io

import pytest

from ibidem.advent_of_code.y2022.dec06 import load, part1, part2

TEST_INPUT = io.StringIO("""\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""")

PART1_RESULT = 7
PART2_RESULT = 19


class TestDec06:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 30
        assert loaded == loaded.strip()

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
