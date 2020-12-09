#!/usr/bin/env python
import itertools

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(9, 2020)) as fobj:
        return [int(l) for l in fobj]


def find_invalid(input, preamble):
    search = input[0:preamble]
    for current in input[preamble:]:
        for x, y in itertools.combinations(search, 2):
            if x + y == current:
                search.pop(0)
                search.append(current)
                break
        else:
            return current
    raise ValueError("Found no invalid numbers in sequence")


def find_weakness(input, target):
    i, j = find_weakness_range(input, target)
    smallest = min(input[i:j])
    largest = max(input[i:j])
    return smallest + largest


def find_weakness_range(input, target):
    for i, start in enumerate(input):
        sum = start
        for j, end in enumerate(input[i + 1:]):
            sum += end
            if sum == target:
                return i, i + 1 + j
            elif sum > target:
                break
    raise ValueError("Found no weakness in sequence")


def part1():
    invalid = find_invalid(load(), 25)
    print(f"The first invalid number in sequence is {invalid}")
    return invalid


def part2(invalid):
    weakness = find_weakness(load(), invalid)
    print(f"Weakness found: {weakness}")


if __name__ == "__main__":
    invalid = part1()
    part2(invalid)
