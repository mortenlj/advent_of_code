#!/usr/bin/env python
import itertools
import re
from collections import namedtuple

from tqdm import tqdm

from ibidem.advent_of_code.util import get_input_name

Registers = namedtuple("Registers", ("w", "x", "y", "z"))


class Alu(object):
    def __init__(self, program, inputs):
        self.w = self.x = self.y = self.z = 0
        self.inputs = iter(inputs)
        self._program = program

    def run(self):
        for inst in self._program:
            inst(self)

    @property
    def registers(self):
        return Registers(self.w, self.x, self.y, self.z)


class Instruction(object):
    pass


class Inp(Instruction):
    PATTERN = re.compile(r"inp ([wxyz])")

    def __init__(self, target):
        self._target = target

    def __call__(self, alu):
        value = next(alu.inputs)
        setattr(alu, self._target, value)


class Add(Instruction):
    PATTERN = re.compile(r"add ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, alu):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(alu, self._value)
        left = getattr(alu, self._target)
        setattr(alu, self._target, left + right)


class Mul(Instruction):
    PATTERN = re.compile(r"mul ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, alu):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(alu, self._value)
        left = getattr(alu, self._target)
        setattr(alu, self._target, left * right)


class Div(Instruction):
    PATTERN = re.compile(r"div ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, alu):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(alu, self._value)
        left = getattr(alu, self._target)
        setattr(alu, self._target, int(left / right))


class Mod(Instruction):
    PATTERN = re.compile(r"mod ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, alu):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(alu, self._value)
        left = getattr(alu, self._target)
        setattr(alu, self._target, left % right)


class Eql(Instruction):
    PATTERN = re.compile(r"eql ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, alu):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(alu, self._value)
        left = getattr(alu, self._target)
        setattr(alu, self._target, 1 if left == right else 0)


def load(fobj):
    fobj.seek(0)
    for line in fobj:
        for inst in Instruction.__subclasses__():
            m = inst.PATTERN.match(line.strip())
            if m:
                yield inst(*m.groups())
                break


def run_program(program, inputs):
    alu = Alu(program, inputs)
    alu.run()
    return alu.registers


def part1(program):
    program = list(program)
    for candidate in tqdm(itertools.product(range(9, 0, -1), repeat=14)):
        result = run_program(program, candidate)
        if result.z == 0:
            return "".join(str(d) for d in candidate)
    return None


def part2(program):
    return None


if __name__ == "__main__":
    with open(get_input_name(24, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(24, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
