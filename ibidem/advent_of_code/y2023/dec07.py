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
    def __init__(self, line):
        cards, bid = line.split()
        self.bid = int(bid.strip())
        self.cards = [self._card_value(c) for c in cards.strip()]
        self.type = self._hand_type(self.cards)

    def __eq__(self, other):
        return self.type == other.type and self.cards == other.cards

    def __lt__(self, other):
        if self.type == other.type:
            return self.cards < other.cards
        return self.type < other.type

    @staticmethod
    def _card_value(c):
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
    def _hand_type(cards):
        c = Counter(cards)
        current_type = HandType.HIGH_CARD
        for _, count in c.most_common():
            if count == 5:
                return HandType.FIVE_OF_A_KIND
            if count == 4:
                return HandType.FOUR_OF_A_KIND
            if count == 3:
                current_type = HandType.THREE_OF_A_KIND
                continue
            if count == 2:
                if current_type == HandType.THREE_OF_A_KIND:
                    return HandType.FULL_HOUSE
                if current_type == HandType.ONE_PAIR:
                    return HandType.TWO_PAIRS
                current_type = HandType.ONE_PAIR
                continue
        return current_type


def load(fobj):
    return [Hand(line) for line in fobj]


def part1(input):
    payouts = []
    for i, hand in enumerate(sorted(input)):
        payouts.append(hand.bid * (i + 1))
    return sum(payouts)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(7, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
