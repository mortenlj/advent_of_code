#!/usr/bin/env python
# -*- coding: utf-8

import itertools
from queue import Queue
from threading import Thread

try:
    from intcode import IntCode, load_program
except ModuleNotFoundError:
    from .intcode import IntCode, load_program

NAMES = ["A", "B", "C", "D", "E"]


class Amp(object):
    def __init__(self, name, program, input_func, output_func):
        self.name = name
        self._input_func = input_func
        self._output_func = output_func
        self._intcode = IntCode(program)
        self._thread = Thread(target=self._execute)

    def run(self):
        self._thread.start()

    def _execute(self):
        self._intcode.execute(input_func=self._input_func, output_func=self._output_func)

    def join(self):
        self._thread.join()

    def __repr__(self):
        return "Amp(name={})".format(self.name)


def run_phases(program, phases):
    channels = [Queue(), Queue(), Queue(), Queue(), Queue()]
    amps = []
    for i in range(5):
        amps.append(Amp(NAMES[i], program, channels[i - 1].get, channels[i].put))
    for i, phase in enumerate(phases):
        chan = channels[i - 1]
        chan.put(phase)
    channels[-1].put(0)
    for amp in amps:
        amp.run()
    for amp in amps:
        amp.join()
    return channels[-1].get()


def perform(phases):
    program = load_program("dec07")
    best_value = 0
    for candidate in itertools.permutations(phases, len(phases)):
        result = run_phases(program, candidate)
        if result > best_value:
            best_value = result
    print(best_value)


def part1():
    phases = [0, 1, 2, 3, 4]
    perform(phases)


def part2():
    phases = [5, 6, 7, 8, 9]
    perform(phases)


if __name__ == "__main__":
    part1()
    part2()
