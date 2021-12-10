#!/usr/bin/env python

import enum
from collections import deque

from ibidem.advent_of_code.util import get_input_name


class Pairs(enum.Enum):
    NORMAL = ("(", ")", 3, 1)
    SQUARE = ("[", "]", 57, 2)
    CURLY = ("{", "}", 1197, 3)
    ANGLED = ("<", ">", 25137, 4)

    def __init__(self, open, close, corruption_score, completion_score):
        self.characters = (open, close)
        self.open = open
        self.close = close
        self.corruption_score = corruption_score
        self.completion_score = completion_score

    @classmethod
    def get(cls, c):
        for i in cls:
            if c in i.characters:
                return i


def load(fobj):
    return fobj.read().splitlines(keepends=False)


def part1(input):
    score = 0
    for line in input:
        stack = deque()
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


def completion_score(stack):
    score = 0
    for cur in reversed(stack):
        score *= 5
        score += cur.completion_score
    return score


def part2(input):
    scores = []
    for line in input:
        stack = deque()
        for c in line:
            cur = Pairs.get(c)
            if c == cur.close:
                other = stack.pop()
                if not other == cur:
                    stack = None
                    break
            if c == cur.open:
                stack.append(cur)
        if stack:
            scores.append(completion_score(stack))
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    with open(get_input_name(10, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
