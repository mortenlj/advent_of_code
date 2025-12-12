#!/usr/bin/env python
from rich.progress import track

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    towels = fobj.readline().strip().split(", ")
    designs = [line.strip() for line in fobj if line.strip()]
    return towels, designs


def design_is_possible(towels: list[str], design: str) -> bool:
    if not design:
        return True
    for towel in towels:
        if design.startswith(towel):
            if design_is_possible(towels, design[len(towel) :]):
                return True
    return False


def part1(input):
    towels, designs = input
    possible = 0
    for design in designs:
        if design_is_possible(towels, design):
            possible += 1
    return possible


def find_designs(
    cache: dict[str, list[list[str]]], towels: list[str], design: str
) -> list[list[str]]:
    if design in cache:
        return cache[design]
    results = []
    for towel in towels:
        if design.startswith(towel):
            remaining = design[len(towel) :]
            if not remaining:
                results.append([towel])
                continue
            possible_patterns = find_designs(cache, towels, remaining)
            results.extend([towel] + pattern for pattern in possible_patterns)
    cache[design] = results
    return results


def part2(input):
    towels, designs = input
    count = 0
    cache = {}
    for design in track(designs):
        possible_towels = [t for t in towels if t in design]
        results = find_designs(cache, possible_towels, design)
        count += len(results)
    return count


if __name__ == "__main__":
    with open(get_input_name(19, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(19, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
