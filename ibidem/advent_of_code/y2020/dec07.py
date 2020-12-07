#!/usr/bin/env python

import re

from ibidem.advent_of_code.y2020.util import get_input_name

BAG_PATTERN = re.compile(r"\d* ?(\w+ \w+) bags?")
TARGET = "shiny gold"


def load():
    with open(get_input_name("dec07")) as fobj:
        return fobj.read().splitlines(keepends=False)


def parse_color(spec):
    m = BAG_PATTERN.match(spec)
    if m:
        return m.group(1)
    raise ValueError(f"Found no color in {spec}")


def parse(rules, target):
    carriers = [target]
    containers = set()
    while carriers:
        carry = carriers.pop()
        for rule in rules:
            left, right = rule.split("contain")
            if carry in right:
                container = parse_color(left)
                carriers.append(container)
                containers.add(container)
    return containers


def part1():
    containers = parse(load(), TARGET)
    print(f"{len(containers)} bags can carry a {TARGET} bag")


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
