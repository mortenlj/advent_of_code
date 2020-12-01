#!/usr/bin/env python
# -*- coding: utf-8
import os

try:
    from .machine import IntCode
    from .disassembler import Disassembler
except ModuleNotFoundError:
    from machine import IntCode
    from disassembler import Disassembler


def load_program(day):
    fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "{}.txt".format(day))
    with open(fpath) as fobj:
        data = fobj.read().strip()
        program = [int(i) for i in data.split(",")]
        return program
