#!/usr/bin/env python

from ibidem.advent_of_code.y2020.util import get_input_name

ALL_ANSWERS = set("abcdefghijklmnopqrstuvwxyz")


def load2():
    with open(get_input_name("dec06")) as fobj:
        groups = []
        group = set()
        for line in fobj:
            if line.strip():
                answers = set(line.strip())
                nos = ALL_ANSWERS - answers
                group.update(nos)
            else:
                groups.append(group)
                group = set()
        if group:
            groups.append(group)
        return groups


def load1():
    with open(get_input_name("dec06")) as fobj:
        groups = []
        group = set()
        for line in fobj:
            if line.strip():
                group.update(line.strip())
            else:
                groups.append(group)
                group = set()
        if group:
            groups.append(group)
        return groups


def part1():
    groups = load1()
    result = sum(len(g) for g in groups)
    print(f"Result 1: {result}")


def part2():
    groups = load2()
    result = sum(len(ALL_ANSWERS - g) for g in groups)
    print(f"Result 2 {result}")


if __name__ == "__main__":
    part1()
    part2()
