#!/usr/bin/env python
import copy
import functools
from collections import defaultdict
from dataclasses import dataclass

from ibidem.advent_of_code.util import get_input_name


@dataclass
class Page:
    number: int
    seen_idx: int = -1


@dataclass
class Rule:
    first: Page
    second: Page

    def see(self, idx, page):
        if self.first.number == page:
            self.first.seen_idx = idx
        elif self.second.number == page:
            self.second.seen_idx = idx

    @property
    def applies(self):
        return self.first.seen_idx >= 0 and self.second.seen_idx >= 0

    @property
    def valid(self):
        return self.first.seen_idx < self.second.seen_idx

    @classmethod
    def parse(cls, line):
        first, second = line.split("|")
        first = Page(int(first))
        second = Page(int(second))
        return cls(first, second)


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
                if a == rule.first.number and b == rule.second.number:
                    return -1
                if a == rule.second.number and b == rule.first.number:
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
    original_rules, updates = input
    invalid_updates = []
    for update in updates:
        rules = [copy.deepcopy(rule) for rule in original_rules]
        rule_mapping = defaultdict(list)
        for rule in rules:
            rule_mapping[rule.first.number].append(rule)
            rule_mapping[rule.second.number].append(rule)
        for idx, page in enumerate(update.page_numbers):
            if page not in rule_mapping:
                continue
            for rule in rule_mapping[page]:
                rule.see(idx, page)
        update_valid = all(rule.valid or not rule.applies for rule in rules)
        if update_valid:
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
