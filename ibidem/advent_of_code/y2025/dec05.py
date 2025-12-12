#!/usr/bin/env python
from dataclasses import dataclass

from ibidem.advent_of_code.util import get_input_name


@dataclass
class Fresh:
    start: int
    end: int

    def __contains__(self, item):
        return self.start <= item < self.end

    def __len__(self):
        return self.end - self.start


def load(fobj):
    fresh = []
    ingredients = set()
    for line in fobj:
        line = line.strip()
        if not line:
            continue
        if "-" in line:
            start, end = [int(v) for v in line.split("-")]
            fresh.append(Fresh(start, end + 1))
        else:
            ingredients.add(int(line))
    return fresh, ingredients


def part1(input):
    fresh, ingredients = input
    count = 0
    for ing in ingredients:
        if any(ing in f for f in fresh):
            count += 1
    return count


def part2(input):
    fresh, _ = input
    fresh = list(fresh)
    fresh.sort(key=lambda f: (f.start, f.end))
    while True:
        fresh_len = len(fresh)
        joined = []
        f1 = fresh.pop()
        while fresh:
            f2 = fresh.pop()
            if f1.start in f2 or (f1.end - 1) in f2:
                start = min(f1.start, f2.start)
                end = max(f1.end, f2.end)
                f1 = Fresh(start, end)
            else:
                joined.append(f1)
                f1 = f2
        joined.append(f1)
        if fresh_len == len(joined):
            break
        fresh = joined
    return sum(len(f) for f in joined)


if __name__ == "__main__":
    with open(get_input_name(5, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(5, 2025)) as fobj:
        p2_result = part2(load(fobj))
        # Too high: 438538168450414
        # Too high: 344510948616107
        # Too high: 344306344403174
        print(f"Part 2: {p2_result}")
