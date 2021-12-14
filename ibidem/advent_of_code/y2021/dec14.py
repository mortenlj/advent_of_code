#!/usr/bin/env python
import itertools
from collections import Counter

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    start = list(next(fobj).strip())
    next(fobj)
    rules = {}
    for line in fobj:
        k, r = line.split("->")
        key = tuple(k.strip())
        rules[key] = r.strip()
    return start, rules


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def part1(start, rules):
    return solve(start, rules, 10)


def solve(start, rules, steps):
    result = start
    for i in range(steps):
        result = solve_step(result, rules)
        print(f"Step {i} solved")
    print("Counting values ...")
    c = Counter(result)
    common = c.most_common()
    most = common[0][1]
    least = common[-1][1]
    return most - least


def solve_step(result, rules):
    last = None
    for pair in pairwise(result):
        yield pair[0]
        yield rules[pair]
        last = pair[1]
    yield last
    print("Step complete")


def part2(start, rules):
    return solve(start, rules, 40)


if __name__ == "__main__":
    with open(get_input_name(14, 2021)) as fobj:
        p1_result = part1(*load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2021)) as fobj:
        p2_result = part2(*load(fobj))
        print(f"Part 2: {p2_result}")
