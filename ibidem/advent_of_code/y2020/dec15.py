#!/usr/bin/env python
from collections import defaultdict, deque

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(15, 2020)) as fobj:
        return [int(v.strip()) for v in fobj.read().split(",")]


def part1(starting):
    return search(starting, 2020)


def search(starting, end_turn):
    numbers = defaultdict(deque)
    last = None
    turn = 1
    for v in starting:
        numbers[v].append(turn)
        last = v
        turn += 1
    while turn <= end_turn:
        previous_turns = numbers[last]
        if len(previous_turns) > 1:
            number = previous_turns[-1] - previous_turns[-2]
        elif len(previous_turns) == 1:
            number = 0
        else:
            raise ValueError("This shouldn't happen")
        numbers[number].append(turn)
        if len(numbers[number]) > 2:
            numbers[number].popleft()
        last = number
        turn += 1
        if turn % 1000000 == 0:
            print(f"turn {turn} passed, with {len(numbers)} numbers seen")
    print(f"The number at turn {turn} was {last}")
    return last


def part2(starting):
    return search(starting, 30000000)


if __name__ == "__main__":
    starting = load()
    part1(starting)
    part2(starting)
