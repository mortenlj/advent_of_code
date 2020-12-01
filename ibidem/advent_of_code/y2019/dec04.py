#!/usr/bin/env python
# -*- coding: utf-8
from collections import defaultdict


def decreasing(s):
    prev = 0
    for c in s:
        i = int(c)
        if i < prev:
            return True
        prev = i
    return False


def no_double(s):
    prev = ""
    for c in s:
        if c == prev:
            return False
        prev = c
    return True


def just_double(s):
    if no_double(s):
        return False
    series = defaultdict(list)
    prev = ""
    for c in s:
        if c == prev:
            series[c].append(c)
        prev = c
    return any(len(s) == 1 for s in series.values())


def part1():
    count = 0
    for i in range(206938, 679128):
        s = str(i)
        if decreasing(s):
            continue
        if no_double(s):
            continue
        if len(s) != 6:
            continue
        count += 1
    print(count)


def part2():
    count = 0
    for i in range(206938, 679128):
        s = str(i)
        if len(s) != 6:
            continue
        if decreasing(s):
            continue
        if just_double(s):
            count += 1
    print(count)


if __name__ == "__main__":
    part1()
    part2()
