#!/usr/bin/env python
# -*- coding: utf-8

from intcode import IntCode, load_program


def part1():
    program = load_program("dec05")
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: input("Enter value => "))


if __name__ == "__main__":
    part1()
