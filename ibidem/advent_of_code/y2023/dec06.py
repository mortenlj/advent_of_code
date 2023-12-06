#!/usr/bin/env python
from functools import reduce
from operator import mul

from ibidem.advent_of_code.util import get_input_name
from sympy import symbols, S, solveset


def load1(fobj):
    times = [int(t) for t in fobj.readline().split(":", 1)[1].split()]
    distances = [int(d) for d in fobj.readline().split(":", 1)[1].split()]
    return list(zip(times, distances))


def load2(fobj):
    time = int("".join(fobj.readline().split(":", 1)[1].split()))
    distance = int("".join(fobj.readline().split(":", 1)[1].split()))
    return time, distance



def part1(input):
    results = []
    for time, distance in input:
        solution = solve(time, distance)
        results.append(len(solution))
    return reduce(mul, results)


def solve(time, distance):
    hold_time = symbols("hold_time")
    equation = hold_time * (time - hold_time) > distance
    solution = solveset(equation, symbol=hold_time, domain=S.Naturals)
    return solution


def part2(input):
    time, distance = input
    solution = solve(time, distance)
    return len(solution)


if __name__ == "__main__":
    with open(get_input_name(6, 2023)) as fobj:
        p1_result = part1(load1(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2023)) as fobj:
        p2_result = part2(load2(fobj))
        print(f"Part 2: {p2_result}")
