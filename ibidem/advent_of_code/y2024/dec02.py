#!/usr/bin/env python
import itertools

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    reports = []
    for line in fobj:
        reports.append(list(map(int, line.strip().split())))
    return reports


def report_is_safe(report):
    return all(a > b and 1 <= a - b <= 3 for a, b in itertools.pairwise(report))


def part1(input):
    count = 0
    for report in input:
        if report_is_safe(report) or report_is_safe(reversed(report)):
            count += 1
    return count


def part2(input):
    count = 0
    for report in input:
        if report_is_safe(report) or report_is_safe(reversed(report)):
            count += 1
            continue
        for i in range(len(report)):
            copy = report[:]
            del copy[i]
            if report_is_safe(copy) or report_is_safe(reversed(copy)):
                count += 1
                break
    return count


if __name__ == "__main__":
    with open(get_input_name(2, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(2, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
