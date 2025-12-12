#!/usr/bin/env python
# -*- coding: utf-8
from queue import Queue

from .intcode import load_program, IntCode


class Solver(object):
    def __init__(self):
        program = load_program("dec21")
        self.intcode = IntCode(program)
        self._input_queue = Queue()
        self._acc = []
        self.result = None

    def run(self, instructions):
        for line in instructions:
            for c in line.strip():
                self._input_queue.put(ord(c))
            self._input_queue.put(10)
        self.intcode.execute(self._input_queue.get, self.output)

    def output(self, v):
        if v > 128:
            self.result = v
            return
        self._acc.append(v)
        if v == 10:
            line = "".join(chr(v) for v in self._acc)
            print(line.strip())
            self._acc = []


def part1():
    instructions = [
        "NOT A T",
        "NOT T T",
        "AND B T",
        "AND C T",
        "NOT T J",
        "AND D J",
        "WALK",
    ]
    run(instructions)


def part2():
    instructions = [
        "NOT F J",
        "NOT E T",
        "OR J T",
        "NOT B T",
        "AND T J",
        "NOT C T",
        "OR T J",
        "NOT H T",
        "NOT T T",
        "AND T J",
        "NOT A T",
        "OR T J",
        "AND D J",
        "RUN",
    ]
    run(instructions)


def run(instructions):
    solver = Solver()
    solver.run(instructions)
    print("The total damage to the hull is {}".format(solver.result))


if __name__ == "__main__":
    part1()
    part2()
