import io
import pytest

from ibidem.advent_of_code.y2023.dec07 import load, part1, part2, HandType

TEST_INPUT = io.StringIO("""\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""")

PART1_RESULT = 6440
PART2_RESULT = NotImplemented


class TestDec07():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 5
        assert loaded[0].bid == 765
        assert loaded[0].type == HandType.ONE_PAIR
        assert loaded[0].cards == [3, 2, 10, 3, 13]
        assert loaded[-1].type == HandType.THREE_OF_A_KIND

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT
        
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
