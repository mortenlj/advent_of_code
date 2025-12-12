#!/usr/bin/env python
# -*- coding: utf-8

from ibidem.advent_of_code.util import get_input_name
from .disassembler import Disassembler as Disassembler
from .machine import IntCode as IntCode


def load_program(day):
    fpath = get_input_name(day, 2019)
    with open(fpath) as fobj:
        data = fobj.read().strip()
        program = [int(i) for i in data.split(",")]
        return program
