#!/usr/bin/env python
from collections import defaultdict

from ibidem.advent_of_code.util import get_input_name


class Case:
    def __init__(self, line):
        signal_patterns, digit_outputs = line.split("|")
        self.signal_patterns = [frozenset(s) for s in signal_patterns.strip().split()]
        self.digit_outputs = [frozenset(s) for s in digit_outputs.strip().split()]


CANDIDATES = {2: {1}, 3: {7}, 4: {4}, 5: {2, 3, 5}, 6: {0, 6, 9}, 7: {8}}


def load(fobj):
    for line in fobj:
        yield Case(line)


def part1(input):
    counts = 0
    for case in input:
        for output in case.digit_outputs:
            if len(output) in {2, 3, 4, 7}:
                counts += 1
    return counts


def solve_three(search, solution):
    patterns = search[3]
    for pattern in patterns:
        if solution[1].issubset(pattern):
            solution[3] = pattern
            search[3].remove(pattern)
            return


def solve_six(search, solution):
    patterns = search[6]
    for pattern in patterns:
        if not solution[1].issubset(pattern):
            solution[6] = pattern
            search[6].remove(pattern)
            return


def solve_nine(search, solution):
    patterns = search[9]
    for pattern in patterns:
        if solution[4].issubset(pattern):
            solution[9] = pattern
            search[9].remove(pattern)
            return


def solve_five(search, solution):
    patterns = search[5]
    for pattern in patterns:
        if pattern.issubset(solution[6]):
            solution[5] = pattern
            search[5].remove(pattern)
            return


def solve_zero(search, solution):
    solution[0] = search[0].pop()


def solve_two(search, solution):
    solution[2] = search[2].pop()


def solve_output(solution, digit_outputs):
    pattern_to_digit = {pattern: digit for digit, pattern in solution.items()}
    result = 0
    for i, digit_pattern in enumerate(reversed(digit_outputs)):
        digit = pattern_to_digit[digit_pattern]
        result += 10**i * digit
    return result


def solve_case(case):
    patterns_to_candidates = {
        p: CANDIDATES[len(p)].copy() for p in case.signal_patterns
    }
    candidates_to_patterns = defaultdict(set)
    search = {}
    for pattern, candidates in patterns_to_candidates.items():
        candidates_to_patterns[frozenset(candidates)].add(pattern)
        for candidate in candidates:
            search[candidate] = candidates_to_patterns[frozenset(candidates)]
    solution = {
        candidates.pop(): pattern
        for pattern, candidates in patterns_to_candidates.items()
        if len(candidates) == 1
    }
    solve_three(search, solution)
    solve_six(search, solution)
    solve_nine(search, solution)
    solve_five(search, solution)
    solve_zero(search, solution)
    solve_two(search, solution)
    return solve_output(solution, case.digit_outputs)


def part2(input):
    sum = 0
    for case in input:
        sum += solve_case(case)
    return sum


if __name__ == "__main__":
    with open(get_input_name(8, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
