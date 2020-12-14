#!/usr/bin/env python
import re

import numpy as np

from ibidem.advent_of_code.util import get_input_name


class Program():
    MEM_PATTERN = re.compile(r"mem\[(\d+)\] = (\d+)")

    def __init__(self):
        self.memory = {}
        self.where = None
        self.mask_value = None

    def process(self, instructions):
        for inst in instructions:
            if inst.startswith("mask"):
                self.where, self.mask_value = mask(inst[7:])
            elif inst.startswith("mem"):
                m = self.MEM_PATTERN.match(inst)
                addr = int(m.group(1))
                value = int(m.group(2))
                self.set(addr, value)

    def set(self, addr, value):
        bin_value = tobinarray(value)
        result = np.where(self.where, self.mask_value, bin_value)
        self.memory[addr] = result

    def calculate_sum(self):
        return sum(toint(v) for v in self.memory.values())


def load():
    with open(get_input_name(14, 2020)) as fobj:
        return fobj.read().splitlines(keepends=False)


def tobinarray(value):
    return np.array(list(np.binary_repr(value, width=36)), dtype=np.uint8)


def toint(value):
    return sum(1 << i for i, b in enumerate(reversed(value)) if b)


def mask(mask):
    mask_value = np.array(list(mask.replace("X", "0")), dtype=np.uint8)
    where = np.array(list(mask)) != "X"
    return where, mask_value


def part1(instructions):
    program = Program()
    program.process(instructions)
    result = program.calculate_sum()
    print(f"The result of the initialisation process is {result}")
    return result


def part2():
    pass


if __name__ == "__main__":
    instructions = load()
    part1(instructions)
    part2()
