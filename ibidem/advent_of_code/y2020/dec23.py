#!/usr/bin/env python
from collections import deque

from ibidem.advent_of_code.util import get_input_name


class Cup:
    def __init__(self, label):
        self.label = label
        self.clockwise = None

    def tail(self, start=None):
        if self == start:
            return self
        if start is None:
            start = self
        if self.clockwise:
            return self.clockwise.tail(start)
        return self

    def inject(self, chain):
        next = self.clockwise
        self.clockwise = chain
        chain.tail().clockwise = next

    def print(self, start=None):
        if self == start:
            return deque()
        if self.clockwise is None:
            return deque((str(self.label),))
        if start is None:
            collect = self.clockwise.print(self)
            return "".join(collect)
        collect = self.clockwise.print(start)
        collect.appendleft(str(self.label))
        return collect

    def all(self, start=None):
        if self == start or self.clockwise is None:
            return deque(((self.label, self),))
        if start is None:
            collect = self.clockwise.all(self)
            return dict(collect)
        collect = self.clockwise.all(start)
        collect.appendleft((self.label, self))
        return collect

    def __repr__(self):
        return f"Cup({self.label})"


def load():
    with open(get_input_name(23, 2020)) as fobj:
        return fobj.read().strip()


def parse(input):
    cups = {}
    prev = None
    first = None
    for c in input:
        cup = Cup(int(c))
        cups[cup.label] = cup
        if not first:
            first = cup
        if prev:
            prev.clockwise = cup
        prev = cup
    prev.clockwise = first
    return first, cups


def play_round(current):
    chain = extract_three(current)
    destination = pick_destination(current)
    destination.inject(chain)
    next = current.clockwise
    return next


def extract_three(first):
    last = first
    prev = None
    chain = first.clockwise
    for _ in range(4):
        prev = last
        last = last.clockwise
    prev.clockwise = None
    first.clockwise = last
    return chain


def pick_destination(current):
    cups = current.all()
    destination_label = current.label - 1
    min_l = min(cups.keys())
    max_l = max(cups.keys())
    while destination_label != current.label:
        while destination_label >= min_l:
            try:
                return cups[destination_label]
            except KeyError:
                destination_label -= 1
        destination_label = max_l
    raise ValueError("Unable to pick valid destination!")


def play_game(rounds, first, cups):
    next = first
    for _ in range(rounds):
        next = play_round(next)
    return cups[1]


def part1(first, cups):
    result = play_game(100, first, cups)
    print(f"The end state is {result.print()}")


def part2(first, cups):
    last = first.tail()
    for i in range(max(cups.keys()), 1000000):
        cup = Cup(i)
        cups[i] = cup
        last.clockwise = cup
        last = cup
    result = play_game(10000000, first, cups)
    one = result.clockwise
    two = one.clockwise
    answer = one.label * two.label
    print(f"The answer is {answer}")
    return one, two


if __name__ == "__main__":
    first, cups = parse(load())
    part1(first, cups)
    part2(first, cups)
