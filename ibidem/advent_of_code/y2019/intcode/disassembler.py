#!/usr/bin/env python
# -*- coding: utf-8

from collections import namedtuple

from .instructions import Instruction, Jump
from .parameter import Parameter, Immediate

Location = namedtuple("Location", ["address", "value"])


class AddressType(object):
    INSTRUCTION = object()
    DATA = object()


class Disassembler(object):
    def __init__(self, program):
        self.memory = program
        self._eof = len(program)
        self._dis = []
        self._address_map = {}
        self._type = [AddressType.DATA] * len(program)
        self.rb = 0

    def disassemble(self):
        self._disassemble()
        self._prepare()
        self._output()

    def _disassemble(self):
        self.parse(0)
        start_at = 0
        evaulate = self._dis[start_at:]
        while evaulate:
            start_at = len(self._dis)
            for location in evaulate:
                instruction = location.value
                if isinstance(instruction, Jump):
                    target = instruction._params[-1]
                    if isinstance(target, Immediate):
                        address = target.get()
                        if address not in self._address_map:
                            self.parse(address)
            evaulate = self._dis[start_at:]

    def parse(self, ip):
        while ip < self._eof:
            try:
                instruction = self._next(ip)
                location = Location(ip, instruction)
                self._dis.append(location)
                self._address_map[ip] = location
                old_ip = ip
                ip = instruction.ip_adjust(ip)
                self._type[old_ip:ip] = [AddressType.INSTRUCTION] * instruction.size
            except ValueError:
                break

    def _next(self, ip):
        instruction_code = self.memory[ip]
        opcode = instruction_code % 100
        instruction = Instruction.from_opcode(opcode)
        params = []
        if instruction.size > 1:
            modes = reversed("{:0{width}}".format(instruction_code // 100, width=instruction.size - 1))
            for i, mode in enumerate(modes):
                params.append(Parameter.from_mode(int(mode))(self.memory[ip + i + 1], self))
        return instruction(params)

    def _prepare(self):
        self._dis.sort(key=lambda l: l.address)

    def _output(self):
        ip = 0
        prev = AddressType.INSTRUCTION
        data_start = 0
        while ip < self._eof:
            type = self._type[ip]
            if type == AddressType.INSTRUCTION:
                if prev == AddressType.DATA:
                    self._output_data(data_start, ip)
                ip = self._output_instruction(ip)
            else:
                if prev == AddressType.INSTRUCTION:
                    data_start = ip
                ip += 1
            prev = type
        if prev == AddressType.DATA:
            self._output_data(data_start, ip)

    def _output_instruction(self, ip):
        location = self._address_map[ip]
        instruction = location.value
        print("{:05}: {!r}".format(location.address, instruction))
        ip = instruction.ip_adjust(ip)
        return ip

    def _output_data(self, data_start, data_end):
        for i, chunk in enumerate(_chunks(self.memory[data_start:data_end], 10)):
            print("{:05}: {}".format(data_start + i * 10, ", ".join("{:6}".format(v) for v in chunk)))


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
