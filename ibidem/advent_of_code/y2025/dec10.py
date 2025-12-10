#!/usr/bin/env python
import dataclasses
import itertools
import math
from typing import List

import bitstruct
from icecream import ic

from ibidem.advent_of_code.util import get_input_name, gen_list


# From itertools documentation
def powerset(iterable):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


@dataclasses.dataclass
class Machine:
    target: int
    buttons: List[int]
    bit_length: int

    def toggle_button(self, id):
        self.target = self.target ^ self.buttons[id]

    def __repr__(self):
        target_lights = "".join("." if b == 0 else "#" for b in bitstruct.unpack("u1" * self.bit_length, self.target.to_bytes(length=math.ceil(self.bit_length/8))))
        return f"Machine({target_lights=}, {self.bit_length=})"


def parse_lights(lights):
    bits = []
    for c in lights:
        if c in "[]":
            continue
        bits.append(0 if c == "." else 1)
    bit_length = len(bits)
    return int.from_bytes(bitstruct.pack("u1" * bit_length, *bits)), bit_length


def parse_button(button, bit_length):
    bits = [0] * bit_length
    button = button[1:-1] # Remove () from ends
    bit_ids = (int(b) for b in button.split(","))
    for id in bit_ids:
        bits[id] = 1
    return int.from_bytes(bitstruct.pack("u1" * bit_length, *bits))


@gen_list
def load(fobj):
    for line in fobj:
        parts = iter(line.strip().split())
        lights, bit_length = parse_lights(next(parts))
        buttons = []
        for button in parts:
            if button[0] == "{":
                break
            buttons.append(parse_button(button, bit_length))
        yield Machine(lights, buttons, bit_length)


def part1(machines):
    results = []
    for machine in machines:
        ic(machine)
        for presses in powerset(machine.buttons):
            lights = 0
            for press in presses:
                lights = lights ^ press
            if lights == machine.target:
                print(f"Found sequence {presses} for {machine=}")
                results.append(len(presses))
                break
    return sum(results)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(10, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
