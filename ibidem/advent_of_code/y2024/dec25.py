#!/usr/bin/env python
import enum
from collections import defaultdict

from ibidem.advent_of_code.util import get_input_name


class SchematicKind(enum.Enum):
    Undefined = 0
    Lock = 1
    Key = 2


def load(fobj):
    schematics = defaultdict(set)
    kind = SchematicKind.Undefined
    heights = [0] * 5
    linecount = 0
    for line in fobj:
        line = line.strip()
        if not line:
            schematics[kind].add(tuple(heights))
            heights = [0] * 5
            kind = SchematicKind.Undefined
            linecount = 0
            continue
        if linecount == 0:
            if line == "#####":
                kind = SchematicKind.Lock
            else:
                kind = SchematicKind.Key
        elif linecount <= 5:
            for i, c in enumerate(line):
                if c == "#":
                    heights[i] += 1
        linecount += 1
    if linecount > 0:
        schematics[kind].add(tuple(heights))
    return schematics[SchematicKind.Key], schematics[SchematicKind.Lock]


def part1(input):
    keys, locks = input
    matches = set()
    for lock in locks:
        for key in keys:
            if all(k + l <= 5 for k, l in zip(key, lock)):  # noqa
                matches.add((key, lock))
    return len(matches)


if __name__ == "__main__":
    with open(get_input_name(25, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
