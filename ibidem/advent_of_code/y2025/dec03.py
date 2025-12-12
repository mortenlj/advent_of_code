#!/usr/bin/env python
from typing import List

from ibidem.advent_of_code.util import get_input_name, gen_list


@gen_list
def load(fobj):
    for line in fobj:
        yield [int(c) for c in line.strip()]


def find_second_largest(bank, largest):
    result = 0
    idx = -1
    for i, d in enumerate(bank):
        if result < d < largest:
            result = d
            idx = i
    return result, idx


def part1_solve_bank(bank: List[int]):
    first = max(bank)
    first_idx = bank.index(first)
    if first_idx == len(bank) - 1:
        first, first_idx = find_second_largest(bank, first)
    second = max(bank[first_idx + 1 :])
    return second + first * 10


def part1(banks):
    results = []
    for bank in banks:
        results.append(part1_solve_bank(bank))
    return sum(results)


def part2_solve_bank(bank: List[int], wanted_length):
    if wanted_length == 0:
        return 0
    if wanted_length == len(bank):
        return sum([d * (10**i) for i, d in enumerate(reversed(bank))])
    if wanted_length == 1:
        searched = bank
    else:
        searched = bank[: -(wanted_length - 1)]
    result = max(searched)
    result_idx = bank.index(result)
    sub_result = part2_solve_bank(bank[result_idx + 1 :], wanted_length - 1)
    mul_result = result * 10 ** (wanted_length - 1)
    return mul_result + sub_result


def part2(banks):
    results = []
    for bank in banks:
        results.append(part2_solve_bank(bank, 12))
    return sum(results)


if __name__ == "__main__":
    with open(get_input_name(3, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(3, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
