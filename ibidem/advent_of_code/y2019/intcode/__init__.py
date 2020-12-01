#!/usr/bin/env python
# -*- coding: utf-8
import os

from .disassembler import Disassembler
from .machine import IntCode


def load_program(day):
    fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "{}.txt".format(day))
    with open(fpath) as fobj:
        data = fobj.read().strip()
        program = [int(i) for i in data.split(",")]
        return program
