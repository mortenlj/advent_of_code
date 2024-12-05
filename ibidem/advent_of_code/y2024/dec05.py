#!/usr/bin/env python
import copy
import functools
from dataclasses import dataclass

from ibidem.advent_of_code.util import get_input_name


@dataclass
class Rule:
    first: int
    second: int

    @classmethod
    def parse(cls, line):
        first, second = line.split("|")
        return cls(int(first), int(second))


@dataclass
class Update:
    page_numbers: list[int]

    @property
    def middle_page(self):
        return self.page_numbers[len(self.page_numbers) // 2]

    @classmethod
    def parse(cls, line):
        return cls([int(p) for p in line.split(",")])

    def sort(self, rules):
        def cmp(a, b):
            for rule in rules:
                if a == rule.first and b == rule.second:
                    return -1
                if a == rule.second and b == rule.first:
                    return 1
            return 0

        self.page_numbers.sort(key=functools.cmp_to_key(cmp))


def load(fobj):
    rules = []
    updates = []
    doing_rules = True
    for line in fobj:
        if not line.strip():
            doing_rules = False
            continue
        if doing_rules:
            rules.append(Rule.parse(line.strip()))
        else:
            updates.append(Update.parse(line.strip()))
    return rules, updates


def part1(input):
    middle_numbers = []
    rules, updates = input
    invalid_updates = []
    for update in updates:
        original_update = copy.deepcopy(update)
        update.sort(rules)
        if update == original_update:
            middle_numbers.append(update.middle_page)
        else:
            invalid_updates.append(update)
    return sum(middle_numbers), invalid_updates


def part2(input, invalid_updates):
    original_rules, _ = input
    middle_numbers = []
    for update in invalid_updates:
        update.sort(original_rules)
        middle_numbers.append(update.middle_page)
    return sum(middle_numbers)


if __name__ == "__main__":
    with open(get_input_name(5, 2024)) as fobj:
        p1_result, invalid = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(5, 2024)) as fobj:
        p2_result = part2(load(fobj), invalid)
        print(f"Part 2: {p2_result}")
