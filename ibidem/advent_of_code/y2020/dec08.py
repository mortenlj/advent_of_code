#!/usr/bin/env python
from collections import namedtuple

from ibidem.advent_of_code.y2020.util import get_input_name

Instruction = namedtuple("Instruction", ("operation", "value"))


class Handheld:
    def __init__(self, programlisting):
        self.program = self._load_program(programlisting)
        self.ip = 0
        self.acc = 0

    def _load_program(self, programlisting):
        program = []
        for line in programlisting:
            op, value = line.strip().split(" ")
            program.append(Instruction(op, int(value)))
        return program

    def execute(self):
        seen_ip = set()
        while self.ip not in seen_ip:
            seen_ip.add(self.ip)
            instruction = self.program[self.ip]
            if instruction.operation == "acc":
                self.acc += instruction.value
                self.ip += 1
            elif instruction.operation == "nop":
                self.ip += 1
            elif instruction.operation == "jmp":
                self.ip += instruction.value


def load():
    with open(get_input_name("dec08")) as fobj:
        return fobj.readlines()


def part1():
    handheld = Handheld(load())
    handheld.execute()
    print(f"Stopped at {handheld.ip}, with an accumulator value of {handheld.acc}")


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
