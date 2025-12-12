import io

import pytest

from ibidem.advent_of_code.y2023.dec07 import load, solve, HandType, Hand

TEST_INPUT = io.StringIO("""\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""")

PART1_RESULT = 6440
PART2_RESULT = 5905


class TestDec07:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded1(self, input):
        return load(input, False)

    def test_load1(self, loaded1):
        assert len(loaded1) == 5
        assert loaded1[0].bid == 765
        assert loaded1[0].type == HandType.ONE_PAIR
        assert loaded1[0].cards == [3, 2, 10, 3, 13]
        assert loaded1[-1].type == HandType.THREE_OF_A_KIND

    @pytest.fixture
    def loaded2(self, input):
        return load(input, True)

    def test_load2(self, loaded2):
        assert len(loaded2) == 5
        assert loaded2[0].bid == 765
        assert loaded2[0].type == HandType.ONE_PAIR
        assert loaded2[0].cards == [3, 2, 10, 3, 13]
        assert loaded2[1].type == HandType.FOUR_OF_A_KIND
        assert loaded2[1].cards == [10, 5, 5, 1, 5]

    def test_part1(self, loaded1):
        result = solve(loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = solve(loaded2)
        assert result == PART2_RESULT

    @pytest.mark.parametrize(
        "line,hand_type",
        [
            ("JJJJJ 1", HandType.FIVE_OF_A_KIND),
            ("TJJJJ 1", HandType.FIVE_OF_A_KIND),
            ("KKJJJ 1", HandType.FIVE_OF_A_KIND),
            ("KJKJK 1", HandType.FIVE_OF_A_KIND),
            ("QQQQJ 1", HandType.FIVE_OF_A_KIND),
            ("KQJJJ 1", HandType.FOUR_OF_A_KIND),
            ("KQQJJ 1", HandType.FOUR_OF_A_KIND),
            ("KQQQJ 1", HandType.FOUR_OF_A_KIND),
            ("KQQQQ 1", HandType.FOUR_OF_A_KIND),
            ("KQTJJ 1", HandType.THREE_OF_A_KIND),
            ("KQTTJ 1", HandType.THREE_OF_A_KIND),
            ("QQTTJ 1", HandType.FULL_HOUSE),
            ("2345J 1", HandType.ONE_PAIR),
        ],
    )
    def test_hand_type_joker(self, line, hand_type):
        hand = Hand(line, True)
        assert hand.type == hand_type
