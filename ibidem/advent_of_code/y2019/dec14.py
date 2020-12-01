#!/usr/bin/env python
# -*- coding: utf-8
from collections import defaultdict
from functools import total_ordering
from queue import PriorityQueue

import math

from .util import get_input_name

TRILLION = 1000000000000
CHEMICALS = {}


@total_ordering
class Chemical(object):
    @classmethod
    def from_name(cls, name):
        if name in CHEMICALS:
            return CHEMICALS[name]
        return cls(name)

    def __init__(self, name):
        self.name = name
        self.requires = []
        CHEMICALS[name] = self

    @property
    def priority(self):
        sub_prio = sum(r.priority for r in self.requires) * 10
        final_prio = sub_prio + len(self.requires)
        return final_prio

    def __eq__(self, other):
        return self is other

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Chemical({})".format(self.name)


class Ingredient(object):
    def __init__(self, quantity, chemical):
        self.quantity = quantity
        self.chemical = chemical

    @classmethod
    def from_str(cls, s):
        q, n = s.split()
        return cls(int(q), Chemical.from_name(n))

    def __repr__(self):
        return "Ingredient({}, {})".format(self.quantity, self.chemical)


class Reaction(object):
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output
        self.output.chemical.requires = [i.chemical for i in inputs]

    def __repr__(self):
        return "Reaction({} => {})".format(", ".join(self.inputs), self.output)


def calculate_ore(lines):
    return calculate(lines, round_up)


def calculate_fuel(lines):
    return TRILLION // calculate(lines, lambda a, b: a / b)


def round_up(needed, quantity):
    return math.ceil(needed / quantity)


def calculate(lines, operation):
    needs = defaultdict(int)
    needs["FUEL"] = 1
    reactions = _load_reactions(lines)
    queue = _prep_queue()
    while not queue.empty():
        _, chemical = queue.get()
        needed = needs[chemical.name]
        if chemical.name == "ORE":
            return needed
        if needed > 0:
            reaction = reactions[chemical]
            multiplier = operation(needed, reaction.output.quantity)
            for input in reaction.inputs:
                needs[input.chemical.name] += input.quantity * multiplier
    raise RuntimeError("This probably shouldn't happen")


def _prep_queue():
    queue = PriorityQueue()
    for chemical in CHEMICALS.values():
        queue.put((-1 * chemical.priority, chemical))
    return queue


def _load_reactions(lines):
    reactions = {}
    for line in lines:
        input_str, output_str = line.split("=>")
        inputs = [Ingredient.from_str(s.strip()) for s in input_str.split(",")]
        output = Ingredient.from_str(output_str)
        reactions[output.chemical] = Reaction(inputs, output)
    return reactions


def part1():
    with open(get_input_name("dec14")) as fobj:
        ore_needed = calculate_ore(fobj)
    print("You need {} units of ORE".format(ore_needed))


def part2():
    with open(get_input_name("dec14")) as fobj:
        fuel_produced = calculate_fuel(fobj)
    print("With {} ORE you could produce {} fuel".format(TRILLION, fuel_produced))


if __name__ == "__main__":
    part1()
    part2()
