#!/usr/bin/env python
# -*- coding: utf-8

from .instructions import Instruction
from .parameter import Parameter


class IntCode(object):
    def __init__(self, memory):
        self.memory = memory.copy()
        self.memory.extend([0] * (32 * 1024 - len(self.memory)))
        self.rb = 0
        self._ip = 0

    def execute(self, input_func=None, output_func=None):
        keep_running = None
        while keep_running is None:
            instruction = self._next(input_func, output_func)
            keep_running = instruction.execute()
            self._ip = instruction.ip_adjust(self._ip)
            self.rb = instruction.rb_adjust(self.rb)

    def _next(self, input_func, output_func):
        instruction_code = self.memory[self._ip]
        opcode = instruction_code % 100
        instruction = Instruction.from_opcode(opcode)
        params = []
        if instruction.size > 1:
            modes = reversed("{:0{width}}".format(instruction_code // 100, width=instruction.size - 1))
            for i, mode in enumerate(modes):
                params.append(Parameter.from_mode(int(mode))(self.memory[self._ip + i + 1], self))
        return instruction(params, input_func=input_func, output_func=output_func)
