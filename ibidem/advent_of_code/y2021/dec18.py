#!/usr/bin/env python
import copy
import functools
import itertools
import math
from collections import abc

from ibidem.advent_of_code.util import get_input_name


class ExitRecursive(Exception):
    pass


class ExplodeValues(Exception):
    def __init__(self, left, right):
        self.left = left
        self.right = right


def load(fobj):
    numbers = []
    for line in fobj:
        numbers.append(eval(line.strip()))
    return numbers


def snailadd_pair(left, right):
    number = [left, right]
    reduce(number)
    return number


def snailadd(numbers):
    return functools.reduce(snailadd_pair, numbers)


def explode(number, _depth=0):
    try:
        for i, v in enumerate(number):
            if isinstance(v, abc.MutableSequence):
                if _depth == 3:
                    left, right = v
                    left, right = place_value(number, i, left, right)
                    number[i] = 0
                    if left is None and right is None:
                        raise ExitRecursive
                    raise ExplodeValues(left, right)
                else:
                    try:
                        explode(v, _depth=_depth + 1)
                    except ExplodeValues as e:
                        left, right = place_value(number, i, e.left, e.right)
                        if left is None and right is None:
                            raise ExitRecursive
                        raise ExplodeValues(left, right)
    except (ExitRecursive, ExplodeValues):
        if _depth > 0:
            raise
        return True
    return False


def place_value(number, i, left, right):
    if not isinstance(number, abc.MutableSequence):
        return left, right
    if left is not None and i > 0:
        insert_value(number, i - 1, -1, left)
        left = None
    if right is not None and i < len(number) - 1:
        insert_value(number, i + 1, 0, right)
        right = None
    return left, right


def insert_value(number, idx, end, value):
    if isinstance(number[idx], abc.MutableSequence):
        insert_value(number[idx], end, end, value)
    else:
        number[idx] += value


def split(number, _inner=False):
    try:
        for i, v in enumerate(number):
            if isinstance(v, abc.MutableSequence):
                split(v, _inner=True)
            elif v >= 10:
                left = v // 2
                right = math.ceil(v / 2)
                number[i] = [left, right]
                raise ExitRecursive
    except ExitRecursive:
        if _inner:
            raise
        return True
    return False


def reduce(number):
    while True:
        if explode(number):
            continue
        if not split(number):
            return


def magnitude(number):
    if not isinstance(number, abc.MutableSequence):
        return number
    return magnitude(number[0]) * 3 + magnitude(number[1]) * 2


def part1(numbers):
    result = snailadd(numbers)
    return magnitude(result)


def part2(numbers):
    best = 0
    for pair in itertools.permutations(numbers, 2):
        mag = magnitude(snailadd(copy.deepcopy(pair)))
        if mag > best:
            best = mag
    return best


if __name__ == "__main__":
    with open(get_input_name(18, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
