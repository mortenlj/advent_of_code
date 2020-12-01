#!/usr/bin/env python
# -*- coding: utf-8

import pytest

from ..intcode import IntCode


@pytest.mark.parametrize("program, memory", (
        ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ([1102, 4, 3, 0, 99], [12, 4, 3, 0, 99]),
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99]),
))
def test_intcode(program, memory):
    intcode = IntCode(program)
    intcode.execute()
    assert intcode.memory[:len(program)] == memory


def test_input():
    program = [3, 0, 99]
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: 42)
    assert intcode.memory[:len(program)] == [42, 0, 99]


def test_output():
    out = []
    intcode = IntCode([4, 2, 99])
    intcode.execute(output_func=out.append)
    assert out == [99]


LARGE_PROGRAM = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
REPLICATING_PROGRAM = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
LONG_NUMBER = 1219070632396864
LONG_NUMBER_PROGRAM = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
BIG_NUMBER = 1125899906842624
BIG_NUMBER_PROGRAM = [104, BIG_NUMBER, 99]


@pytest.mark.parametrize("program, input, result", (
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1, 0),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], -1, 0),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], -8, 0),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 199, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], -8, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], -1, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 1, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 199, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
        (LARGE_PROGRAM, 1, 999),
        (LARGE_PROGRAM, 7, 999),
        (LARGE_PROGRAM, 8, 1000),
        (LARGE_PROGRAM, 9, 1001),
        (LARGE_PROGRAM, 99, 1001),
))
def test_comparisons(program, input, result):
    out = []
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: input, output_func=out.append)
    assert out == [result]


@pytest.mark.parametrize("program, input, result", (
        (REPLICATING_PROGRAM, None, REPLICATING_PROGRAM),
        (LONG_NUMBER_PROGRAM, None, [LONG_NUMBER]),
        (BIG_NUMBER_PROGRAM, None, [BIG_NUMBER]),
))
def test_relative_base(program, input, result):
    out = []
    intcode = IntCode(program)
    intcode.execute(input_func=lambda: input, output_func=out.append)
    assert out == result
