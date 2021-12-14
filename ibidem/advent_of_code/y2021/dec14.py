#!/usr/bin/env python
import itertools
from collections import Counter, defaultdict

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
    return itertools.zip_longest(a, b)


def part1(start, rules):
    return solve(start, rules, 10)


def seed(iterable):
    result = defaultdict(int)
    for pair in pairwise(iterable):
        if None in pair:
            idx = 0 if pair[1] is None else 1
            result[pair[idx]] += 1
        else:
            result[pair] += 1
    return result


def solve(start, rules, steps):
    result = seed(start)
    for i in range(steps):
        result = solve_step(i, result, rules)
    counts = Counter()
    for pair in result.keys():
        key = pair[0]
        counts[key] += result[pair]
    common = counts.most_common()
    most = common[0][1]
    least = common[-1][1]
    return most - least


def solve_step(i, input, rules):
    result = defaultdict(int)
    for pair in input.keys():
        if isinstance(pair, tuple):
            first, last = pair
            middle = rules[pair]
            result[(first, middle)] += input[pair]
            result[(middle, last)] += input[pair]
        else:
            result[pair] += input[pair]
    print(f"Step {i} solved")
    return result


def part2(start, rules):
    return solve(start, rules, 40)


if __name__ == "__main__":
    with open(get_input_name(14, 2021)) as fobj:
        p1_result = part1(*load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2021)) as fobj:
        p2_result = part2(*load(fobj))
        print(f"Part 2: {p2_result}")
