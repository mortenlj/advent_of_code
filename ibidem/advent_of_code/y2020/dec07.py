#!/usr/bin/env python

import re

import networkx as nx

from ibidem.advent_of_code.y2020.util import get_input_name

BAG_PATTERN = re.compile(r"(\d*) ?(\w+ \w+) bags?")
TARGET = "shiny gold"


def load():
    with open(get_input_name("dec07")) as fobj:
        return fobj.read().splitlines(keepends=False)


def parse_color(spec):
    m = BAG_PATTERN.match(spec)
    if m:
        return m.group(1), m.group(2)
    raise ValueError(f"Found no color in {spec}")


def parse_network(rules):
    g = nx.DiGraph()
    for rule in rules:
        left, right = rule.split("contain")
        _, parent = parse_color(left.strip())
        for spec in right.split(","):
            count, child = parse_color(spec.strip())
            if not count:
                continue
            g.add_edge(parent, child, weight=int(count))
    return g


def part1():
    containers = find_containers(load(), TARGET)
    print(f"{len(containers)} bags can carry a {TARGET} bag")


def find_containers(rules, target):
    g = parse_network(rules)
    containers = nx.algorithms.dag.ancestors(g, target)
    return containers


def count_children(g, target):
    count = 1
    for child in g.successors(target):
        count += count_children(g, child) * g.out_edges[target, child]["weight"]
    return count


def part2():
    g = parse_network(load())
    count = count_children(g, TARGET) - 1
    print(f"One {TARGET} bag must contain {count} other bags")


if __name__ == "__main__":
    part1()
    part2()
