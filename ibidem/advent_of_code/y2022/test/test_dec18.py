import io

import pytest

from ibidem.advent_of_code.y2022.dec18 import load, part1, part2

TEST_INPUT = io.StringIO("""\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""")

PART1_RESULT = 64
PART2_RESULT = 58


class TestDec18():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 13
        assert loaded[-1].x == 2
        assert loaded[-1].y == 3
        assert loaded[-1].z == 5

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.xfail(reason="Not implemented")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
