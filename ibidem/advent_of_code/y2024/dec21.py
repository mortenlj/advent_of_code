#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


class Pad:
    _coords: dict
    _gap: tuple

    def __init__(self):
        self._position = "A"

    def next_press(self, value):
        r1, c1 = self._coords[self._position]
        r2, c2 = self._coords[value]
        self._position = value

        ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
        lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

        # Safe to move vertically first if heading right and corner point isn't the gap
        if c2 > c1 and (r2, c1) != self._gap:
            return f"{ud}{lr}A"

        # Safe to move horizontally first if corner point isn't the gap
        if (r1, c2) != self._gap:
            return f"{lr}{ud}A"

        # Must be safe to move vertically first because we can't be in same column as gap.
        return f"{ud}{lr}A"


class Numeric(Pad):
    _gap = (3, 0)
    _coords = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
    }


class Directional(Pad):
    _gap = (0, 0)
    _coords = {
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }


def load(fobj):
    return [line.strip() for line in fobj]


def make_sequence(input):
    n = Numeric()
    output = "".join([n.next_press(c) for c in input])
    d1 = Directional()
    output = "".join([d1.next_press(c) for c in output])
    d2 = Directional()
    output = "".join([d2.next_press(c) for c in output])
    return output


def part1(inputs):
    result = 0
    for input in inputs:
        sequence = make_sequence(input)
        complexity = len(sequence) * int(input[:-1])
        print(f"{input}: {complexity} ({sequence})")
        result += complexity
    return result


def part2(inputs):
    return None


if __name__ == "__main__":
    with open(get_input_name(21, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(21, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
