#!/usr/bin/env python
# -*- coding: utf-8

from .intcode import IntCode, load_program


def part1():
    program = load_program("dec02")
    program[1] = 12
    program[2] = 2
    intcode = IntCode(program)
    intcode.execute()
    print("Value at position 0: {}".format(intcode.memory[0]))


def part2():
    for noun in range(99):
        for verb in range(99):
            program = load_program("dec02")
            program[1] = noun
            program[2] = verb
            intcode = IntCode(program)
            intcode.execute()
            if intcode.memory[0] == 19690720:
                print("Noun: {}, Verb: {}".format(noun, verb))
                print("Result: {}".format(100 * noun + verb))
                return


if __name__ == "__main__":
    part1()
    part2()
