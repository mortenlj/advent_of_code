#!/usr/bin/env python
from collections import deque, Counter

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return fobj.read().strip()


def count_unique(window):
    counter = Counter(window)
    return len(counter.keys())


def part1(input):
    return search_buffer(input, 4)


def search_buffer(buffer, window_length):
    window = deque()
    for i, c in enumerate(buffer):
        window.append(c)
        if len(window) > window_length:
            window.popleft()
        if count_unique(window) == window_length:
            return i + 1
    return 0


def part2(input):
    return search_buffer(input, 14)


if __name__ == "__main__":
    with open(get_input_name(6, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
