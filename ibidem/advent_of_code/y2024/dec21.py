#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


class Numeric:
    _press_map = {
        "A": {"A": "A", "0": "<A", "1": "^<<A", "2": "^<A", "3": "^A", "4": "^^<<A", "5": "^^<A", "6": "^^A",
              "7": "^^^<<A", "8": "^^^<A", "9": "^^^A"},
        "0": {"A": ">A", "0": "A", "1": "^<A", "2": "^A", "3": "^>A", "4": "^^<A", "5": "^^A", "6": "^^>A",
              "7": "^^^<A", "8": "^^^A", "9": "^^^>A"},
        "1": {"A": ">>vA", "0": ">vA", "1": "A", "2": ">A", "3": ">>A", "4": "^A", "5": "^>A", "6": "^>>A", "7": "^^A",
              "8": "^^>A", "9": "^^>>A"},
        "2": {"A": ">vA", "0": "vA", "1": "<A", "2": "A", "3": ">A", "4": "^<A", "5": "^A", "6": "^>A", "7": "^^<A",
              "8": "^^A", "9": ">^^A"},
        "3": {"A": "vA", "0": "v<A", "1": "<<A", "2": "<A", "3": "A", "4": "^<<A", "5": "^<A", "6": "^A", "7": "^^<<A",
              "8": "^^<A", "9": "^^A"},
        "4": {"A": ">>vvA", "0": ">vvA", "1": "vA", "2": "v>A", "3": "v>>A", "4": "A", "5": ">A", "6": ">>A", "7": "^A",
              "8": "^>A", "9": "^>>A"},
        "5": {"A": ">vvA", "0": "vvA", "1": "v<A", "2": "vA", "3": "v>A", "4": "<A", "5": "A", "6": ">A", "7": "^<A",
              "8": "^A", "9": "^>A"},
        "6": {"A": "vvA", "0": "vv<A", "1": "v<<A", "2": "v<A", "3": "vA", "4": "<<A", "5": "<A", "6": "A", "7": "^<<A",
              "8": "^<A", "9": "^A"},
        "7": {"A": ">>vvvA", "0": ">vvvA", "1": "vvA", "2": "vv>A", "3": "vv>>A", "4": "vA", "5": "v>A", "6": "v>>A",
              "7": "A", "8": ">A", "9": ">>A"},
        "8": {"A": ">vvvA", "0": "vvvA", "1": "vv<A", "2": "vvA", "3": "vv>A", "4": "v<A", "5": "vA", "6": "v>A",
              "7": "<A", "8": "A", "9": ">A"},
        "9": {"A": "vvvA", "0": "vvv<A", "1": "vv<<A", "2": "vv<A", "3": "vvA", "4": "v<<A", "5": "v<A", "6": "vA",
              "7": "<<A", "8": "<A", "9": "A"},
    }

    def __init__(self):
        self._position = "A"

    def next_press(self, value):
        press = self._press_map[self._position][value]
        self._position = value
        return press


class Directional:
    _press_map = {
        "A": {"A": "A", "^": "<A", "<": "<v<A", ">": "vA", "v": "<vA"},
        "^": {"A": ">A", "^": "A", "<": "v<A", ">": ">vA", "v": "vA"},
        "<": {"A": ">>^A", "^": ">^A", "<": "A", ">": ">>A", "v": ">A"},
        ">": {"A": "^A", "^": "<^A", "<": "<<A", ">": "A", "v": "<A"},
        "v": {"A": ">^A", "^": "^A", "<": "<A", ">": ">A", "v": "A"},
    }

    def __init__(self):
        self._position = "A"

    def next_press(self, value):
        press = self._press_map[self._position][value]
        self._position = value
        return press


def load(fobj):
    return [l.strip() for l in fobj]


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
