#!/usr/bin/env python
import itertools
import re

import numpy as np

from ibidem.advent_of_code.util import get_input_name

MEM_PATTERN = re.compile(r"mem\[(\d+)\] = (\d+)")


class Program1:
    def __init__(self):
        self.memory = {}
        self.where = None
        self.mask_value = None

    def process(self, instructions):
        for inst in instructions:
            if inst.startswith("mask"):
                self.where, self.mask_value = self.mask(inst[7:])
            elif inst.startswith("mem"):
                m = MEM_PATTERN.match(inst)
                addr = int(m.group(1))
                value = int(m.group(2))
                self.set(addr, value)

    def set(self, addr, value):
        bin_value = tobinarray(value)
        result = np.where(self.where, self.mask_value, bin_value)
        self.memory[addr] = result

    @staticmethod
    def mask(m):
        mask_value = np.array(list(m.replace("X", "0")), dtype=np.uint8)
        where = np.array(list(m)) != "X"
        return where, mask_value

    def calculate_sum(self):
        return sum(toint(v) for v in self.memory.values())


class Program2:
    def __init__(self):
        self.memory = {}
        self.floating_idx = None
        self.fixed_idx = None

    def process(self, instructions):
        for inst in instructions:
            if inst.startswith("mask"):
                mask_values = np.array(list(inst[7:]))
                self.floating_idx = np.where(mask_values == "X")[0]
                self.fixed_idx = np.where(mask_values == "1")[0]
            elif inst.startswith("mem"):
                m = MEM_PATTERN.match(inst)
                addr = int(m.group(1))
                value = int(m.group(2))
                self.set(addr, value)

    def set(self, addr, value):
        for mem in self.generate_addr(addr):
            self.memory[mem] = value

    def generate_addr(self, addr):
        bin_addr = tobinarray(addr)
        np.put(bin_addr, self.fixed_idx, 1)
        for combo in itertools.product((0, 1), repeat=len(self.floating_idx)):
            np.put(bin_addr, self.floating_idx, combo)
            yield toint(bin_addr)

    def calculate_sum(self):
        return sum(self.memory.values())


def load():
    with open(get_input_name(14, 2020)) as fobj:
        return fobj.read().splitlines(keepends=False)


def tobinarray(value):
    return np.array(list(np.binary_repr(value, width=36)), dtype=np.uint8)


def toint(value):
    return sum(1 << i for i, b in enumerate(reversed(value)) if b)


def part1(instructions):
    program = Program1()
    program.process(instructions)
    result = program.calculate_sum()
    print(f"The result of the initialisation process v1 is {result}")
    return result


def part2(instructions):
    program = Program2()
    program.process(instructions)
    result = program.calculate_sum()
    print(f"The result of the initialisation process v2 is {result}")
    return result


if __name__ == "__main__":
    instructions = load()
    part1(instructions)
    part2(instructions)
