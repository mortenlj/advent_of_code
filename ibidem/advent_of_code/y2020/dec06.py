#!/usr/bin/env python
import string

from ibidem.advent_of_code.y2020.util import get_input_name

ALL_ANSWERS = set(string.ascii_lowercase)


def load(update):
    with open(get_input_name("dec06")) as fobj:
        groups = []
        group = set()
        for line in fobj:
            if line.strip():
                answers = set(line.strip())
                update(group, answers)
            else:
                groups.append(group)
                group = set()
        if group:
            groups.append(group)
        return groups


def load2():
    return load(lambda g, a: g.update(ALL_ANSWERS - a))


def load1():
    return load(lambda g, a: g.update(a))


def part1():
    groups = load1()
    result = sum(len(g) for g in groups)
    print(f"Result 1: {result}")
    return result


def part2():
    groups = load2()
    result = sum(len(ALL_ANSWERS - g) for g in groups)
    print(f"Result 2 {result}")
    return result


if __name__ == "__main__":
    part1()
    part2()
