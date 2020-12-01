#!/usr/bin/env python
# -*- coding: utf-8

from .intcode import IntCode, load_program


def part1():
    program = load_program("dec09")
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: 1)


def part2():
    program = load_program("dec09")
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: 2)


if __name__ == "__main__":
    part1()
    part2()
