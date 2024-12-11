#!/usr/bin/env python
from functools import lru_cache

from rich.progress import track

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return [int(v) for v in fobj.read().strip().split()]


@lru_cache(maxsize=None)
def blink_stone(stone) -> list[int]:
    engraved = str(stone)
    if stone == 0:
        return [1]
    elif len(engraved) % 2 == 0:
        left, right = engraved[:len(engraved) // 2], engraved[len(engraved) // 2:]
        return [int(left), int(right)]
    return [stone * 2024]


def blink(stones, iteration):
    new_stones = []
    for stone in stones:
        new_stones.extend(blink_stone(stone))
    return new_stones


def part1(stones: list[int]):
    for i in track(range(25)):
        stones = blink(stones, i + 1)
    return len(stones)


def part2(stones: list[int]):
    for i in range(75):
        stones = blink(stones, i + 1)
    return len(stones)


if __name__ == "__main__":
    with open(get_input_name(11, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
