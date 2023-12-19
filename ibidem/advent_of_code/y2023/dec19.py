#!/usr/bin/env python
import operator
import re
from dataclasses import dataclass
from typing import Callable

from ibidem.advent_of_code.util import get_input_name

STEP_PATTERN = re.compile(r"(\w+)([<>])(\d+):(\w+)")
OPERATIONS = {
    "<": operator.lt,
    ">": operator.gt,
}


def true_func(x, y):
    return True


class Workflow:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def process(self, part):
        for step in self.steps:
            if step.operation(getattr(part, step.attr), step.value):
                return step.next
        raise RuntimeError("No matching step found")


@dataclass
class Step:
    attr: str
    operation: Callable[[int, int], bool]
    value: int
    next: str


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def rating(self):
        return self.x + self.m + self.a + self.s


def parse_step(step):
    if match := STEP_PATTERN.match(step):
        attr, op, value, next = match.groups()
        return Step(attr, OPERATIONS[op], int(value), next)
    else:
        return Step("x", true_func, 0, step)


def load(fobj):
    workflows = {}
    for line in fobj:
        line = line.strip()
        if not line:
            break
        name, steps = line.split("{")
        steps = steps[:-1].split(",")
        workflows[name] = Workflow(name, [parse_step(step) for step in steps])
    parts = []
    for line in fobj:
        line = line.strip()
        if not line:
            break
        parts.append(parse_part(line))
    return workflows, parts


def parse_part(line):
    attrs = {}
    for kv in line[1:-1].split(","):
        k, v = kv.split("=")
        attrs[k] = int(v)
    part = Part(**attrs)
    return part


def part1(input):
    workflows, parts = input
    accepted = []
    for part in parts:
        workflow = workflows["in"]
        while True:
            match workflow.process(part):
                case "A":
                    accepted.append(part)
                    break
                case "R":
                    break
                case name:
                    workflow = workflows[name]
    return sum(part.rating() for part in accepted)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(19, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(19, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
