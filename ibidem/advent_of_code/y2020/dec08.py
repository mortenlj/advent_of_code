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

    def execute(self, fix=False):
        self.ip = 0
        self.acc = 0
        seen_ip = set()
        while self.ip not in seen_ip:
            seen_ip.add(self.ip)
            try:
                instruction = self.program[self.ip]
            except IndexError:
                return True
            if instruction.operation == "acc":
                self.acc += instruction.value
                self.ip += 1
            elif instruction.operation == "nop":
                if fix:
                    if self.ip + instruction.value >= len(self.program):
                        return True
                self.ip += 1
            elif instruction.operation == "jmp":
                self.ip += instruction.value
        return False

    def execute_patcher(self):
        for i, instruction in enumerate(self.program):
            if instruction.operation != "jmp":
                continue
            try:
                self.program[i] = Instruction("nop", instruction.value)
                if self.execute():
                    return i
            finally:
                self.program[i] = instruction


def load():
    with open(get_input_name("dec08")) as fobj:
        return fobj.readlines()


def part1():
    handheld = Handheld(load())
    handheld.execute()
    print(f"Stopped at {handheld.ip}, with an accumulator value of {handheld.acc}")


def part2():
    handheld = Handheld(load())
    fixed = handheld.execute(fix=True)
    if fixed:
        print(
            f"Patched program stopped with an accumulator value of {handheld.acc}, after patching nop at {handheld.ip}")
        return
    patched_ip = handheld.execute_patcher()
    print(f"Patched program stopped with an accumulator value of {handheld.acc}, after patching jmp at {patched_ip}")


if __name__ == "__main__":
    part1()
    part2()
