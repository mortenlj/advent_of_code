#!/usr/bin/env python
import numpy as np

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return np.fromstring(fobj.read(), dtype=int, sep=",")


def part1(input):
    residuals = np.arange(np.min(input), np.max(input) + 1)
    work = np.rot90(
        np.broadcast_to(residuals, (input.shape[0], residuals.shape[0])), -1
    )
    res = work - input
    return np.min(np.sum(np.abs(res), axis=1))


def part2(input):
    residuals = np.arange(np.min(input), np.max(input) + 1)
    work = np.rot90(
        np.broadcast_to(residuals, (input.shape[0], residuals.shape[0])), -1
    )
    res = work - input
    simple_cost = np.abs(res)
    cost = (simple_cost * (simple_cost + 1)) / 2
    return np.min(np.sum(cost, axis=1))


if __name__ == "__main__":
    with open(get_input_name(7, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
