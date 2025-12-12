#!/usr/bin/env python
import re
import struct
from collections import namedtuple

from alive_progress import alive_it

from ibidem.advent_of_code.util import get_input_name


class Packable(object):
    _PACK_FMT = ""

    @classmethod
    def unpack(cls, key):
        params = struct.unpack(cls._PACK_FMT, key)
        return cls(*params)

    def pack(self):
        return struct.pack(self._PACK_FMT, *self)


class State(namedtuple("State", ("w", "x", "y", "z")), Packable):
    _PACK_FMT = "iiiq"


Result = namedtuple("Result", ("generation", "inputs"))

BLANK_RESULT = Result(-1, 0)


class Instruction(object):
    _target = None
    _value = ""

    def __repr__(self):
        return f"{self.__class__.__name__.lower()} {self._target} {self._value}"


class Inp(Instruction):
    PATTERN = re.compile(r"inp ([wxyz])")

    def __init__(self, target):
        self._target = target

    def __call__(self, state, value):
        return state._replace(w=value)


class Add(Instruction):
    PATTERN = re.compile(r"add ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, state):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(state, self._value)
        left = getattr(state, self._target)
        return state._replace(**{self._target: left + right})


class Mul(Instruction):
    PATTERN = re.compile(r"mul ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, state):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(state, self._value)
        left = getattr(state, self._target)
        return state._replace(**{self._target: left * right})


class Div(Instruction):
    PATTERN = re.compile(r"div ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, state):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(state, self._value)
        left = getattr(state, self._target)
        return state._replace(**{self._target: int(left / right)})


class Mod(Instruction):
    PATTERN = re.compile(r"mod ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, state):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(state, self._value)
        left = getattr(state, self._target)
        return state._replace(**{self._target: left % right})


class Eql(Instruction):
    PATTERN = re.compile(r"eql ([wxyz]) ([wxyz]|-?\d+)")

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def __call__(self, state):
        try:
            right = int(self._value)
        except ValueError:
            right = getattr(state, self._value)
        left = getattr(state, self._target)
        return state._replace(**{self._target: 1 if left == right else 0})


def load(fobj):
    fobj.seek(0)
    for line in fobj:
        for inst in Instruction.__subclasses__():
            m = inst.PATTERN.match(line.strip())
            if m:
                yield inst(*m.groups())
                break


def run_program(program):
    states = {State(0, 0, 0, 0).pack(): BLANK_RESULT}
    for generation, inst in enumerate(program):
        new_states = {}
        if isinstance(inst, Inp):
            print(
                f"Processing instruction {generation} (which is an input instruction)"
            )
            for state_key in alive_it(states):
                state = State.unpack(state_key)
                for value in range(1, 10):
                    new_state = inst(state, value)
                    inputs = states[state_key].inputs * 10 + value
                    if new_state.pack() in states:
                        old_max = states.get(new_state.pack(), BLANK_RESULT).inputs
                        states[new_state.pack()] = Result(
                            generation, max(inputs, old_max)
                        )
                    else:
                        new_states[new_state.pack()] = Result(generation, inputs)
        else:
            for state_key in alive_it(states):
                state = State.unpack(state_key)
                new_state = inst(state)
                inputs = states[state_key].inputs
                if new_state.pack() in states:
                    old_max = states.get(new_state.pack(), BLANK_RESULT).inputs
                    states[new_state.pack()] = Result(generation, max(inputs, old_max))
                else:
                    new_states[new_state.pack()] = Result(generation, inputs)
        states = {k: v for k, v in states.items() if v.generation == generation}
        states.update(new_states)
    print(f"Searching {len(states)} states for best result")
    return max(states[s].inputs for s in states if State.unpack(s).z == 0)


def part1(program):
    program = list(program)
    return run_program(program)


def part2(program):
    return None


if __name__ == "__main__":
    with open(get_input_name(24, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(24, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
