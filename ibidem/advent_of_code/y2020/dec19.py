#!/usr/bin/env python
import re

from ibidem.advent_of_code.util import get_input_name


class Rule:
    NUM = re.compile(r"\d+")

    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern

    def resolve(self, rules):
        self.rules = rules
        self.pattern, changes = self.NUM.subn(self.replace, self.pattern)
        while changes > 0:
            self.pattern, changes = self.NUM.subn(self.replace, self.pattern)
        return self.pattern.replace(" ", "")

    def replace(self, m):
        rule = self.rules[m.group()]
        return rule.resolve(self.rules)

    def __repr__(self):
        return f"Rule({self.name}, {self.pattern})"


def parse_split_rule(line):
    left, right = line.split("|")
    left = parse_plain_rule(left)
    right = parse_plain_rule(right)
    return f"({left} | {right})"


def parse_plain_rule(line):
    parts = line.split()
    if len(parts) == 1:
        return line.strip()
    return f"({line.strip()})"


def load_rule(line, rules, _):
    name, pattern = line.split(":")
    pattern = pattern.strip()
    if "|" in pattern:
        pattern = parse_split_rule(pattern)
    else:
        pattern = parse_plain_rule(pattern)
    rules[name] = Rule(name, pattern)


def load_message(line, _, messages):
    messages.append(line)


def load():
    rules = {}
    messages = []
    line_parser = load_rule
    with open(get_input_name(19, 2020)) as fobj:
        for line in fobj:
            line = line.strip()
            line = line.replace('"', "")
            if not line:
                line_parser = load_message
                continue
            line_parser(line, rules, messages)
    return rules, messages


def part1(rules, messages):
    start = rules["0"]
    pattern = re.compile(start.resolve(rules))
    count = 0
    for message in messages:
        if pattern.fullmatch(message):
            count += 1
    print(f"{count} messages matches rule 0")
    return count


def part2(rules, messages):
    pass


if __name__ == "__main__":
    rules, messages = load()
    part1(rules, messages)
    part2(rules, messages)
