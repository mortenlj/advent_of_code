#!/usr/bin/env python
from collections import Counter
from enum import IntEnum
from functools import total_ordering

from ibidem.advent_of_code.util import get_input_name


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    FIVE_OF_A_KIND = 8


@total_ordering
class Hand:
    def __init__(self, line, joker_mode):
        cards, bid = line.split()
        self.bid = int(bid.strip())
        self.cards = [self._card_value(c, joker_mode) for c in cards.strip()]
        self.type = self._hand_type(self.cards, joker_mode)

    def __eq__(self, other):
        return self.type == other.type and self.cards == other.cards

    def __lt__(self, other):
        if self.type == other.type:
            return self.cards < other.cards
        return self.type < other.type

    @staticmethod
    def _card_value(c, joker_mode):
        if joker_mode and c == "J":
            return 1
        value_map = {
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if c in value_map:
            return value_map[c]
        else:
            return int(c)

    @staticmethod
    def _hand_type(cards, joker_mode):
        c = Counter(cards)
        current_type = HandType.HIGH_CARD
        if joker_mode:
            joker_count = c[1]
            del c[1]
        else:
            joker_count = 0
        if joker_count == 5:
            return HandType.FIVE_OF_A_KIND
        for _, count in c.most_common():
            if count == 5:
                return HandType.FIVE_OF_A_KIND
            if count == 4:
                if joker_count == 1:
                    return HandType.FIVE_OF_A_KIND
                return HandType.FOUR_OF_A_KIND
            if count == 3:
                if joker_count == 2:
                    return HandType.FIVE_OF_A_KIND
                if joker_count == 1:
                    return HandType.FOUR_OF_A_KIND
                current_type = HandType.THREE_OF_A_KIND
                continue
            if count == 2:
                if joker_count == 3:
                    return HandType.FIVE_OF_A_KIND
                if joker_count == 2:
                    return HandType.FOUR_OF_A_KIND
                if joker_count == 1:
                    current_type = HandType.THREE_OF_A_KIND
                    joker_count = 0
                    continue
                if current_type == HandType.THREE_OF_A_KIND:
                    return HandType.FULL_HOUSE
                if current_type == HandType.ONE_PAIR:
                    return HandType.TWO_PAIRS
                current_type = HandType.ONE_PAIR
                continue
            if count == 1:
                if joker_count == 4:
                    return HandType.FIVE_OF_A_KIND
                if joker_count == 3:
                    return HandType.FOUR_OF_A_KIND
                if joker_count == 2:
                    return HandType.THREE_OF_A_KIND
                if joker_count == 1:
                    if current_type == HandType.ONE_PAIR:
                        return HandType.TWO_PAIRS
                    current_type = HandType.ONE_PAIR
                    joker_count = 0
                    continue
        return current_type


def load(fobj, joker_mode):
    return [Hand(line, joker_mode) for line in fobj]


def solve(input):
    payouts = []
    for i, hand in enumerate(sorted(input)):
        payouts.append(hand.bid * (i + 1))
    return sum(payouts)


if __name__ == "__main__":
    with open(get_input_name(7, 2023)) as fobj:
        p1_result = solve(load(fobj, False))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2023)) as fobj:
        p2_result = solve(load(fobj, True))
        print(f"Part 2: {p2_result}")
