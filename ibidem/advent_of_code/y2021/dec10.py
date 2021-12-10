#!/usr/bin/env python

import enum
from collections import defaultdict, deque

from ibidem.advent_of_code.util import get_input_name


class Pairs(enum.Enum):
    NORMAL = ("(", ")", 3)
    SQUARE = ("[", "]", 57)
    CURLY = ("{", "}", 1197)
    ANGLED = ("<", ">", 25137)

    def __init__(self, open, close, corruption_score):
        self.characters = (open, close)
        self.open = open
        self.close = close
        self.corruption_score = corruption_score

    @classmethod
    def get(cls, c):
        for i in cls:
            if c in i.characters:
                return i


def load(fobj):
    return fobj.read().splitlines(keepends=False)


def part1(input):
    stack = deque()
    score = 0
    for line in input:
        for c in line:
            cur = Pairs.get(c)
            if c == cur.close:
                other = stack.pop()
                if not other == cur:
                    score += cur.corruption_score
                    break
            if c == cur.open:
                stack.append(cur)
    return score


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(10, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
