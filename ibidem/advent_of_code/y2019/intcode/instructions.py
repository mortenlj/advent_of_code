#!/usr/bin/env python
# -*- coding: utf-8


class Instruction(object):
    opcode = None
    size = None
    _instructions = None

    def __init__(self, params, input_func=None, output_func=None):
        self._params = params

    def execute(self):
        raise NotImplementedError("Must be implemented")

    def ip_adjust(self, ip):
        return ip + self.size

    def rb_adjust(self, rb):
        return rb

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__, ", ".join(repr(p) for p in self._params)
        )

    @classmethod
    def from_opcode(cls, opcode):
        if cls._instructions is None:
            cls._instructions = {}
            classes = [cls]
            while classes:
                instruction = classes.pop()
                if instruction.opcode is not None:
                    cls._instructions[instruction.opcode] = instruction
                classes.extend(instruction.__subclasses__())
        if opcode not in cls._instructions:
            raise ValueError("Invalid opcode {} for Instruction".format(opcode))
        return cls._instructions[opcode]


class Halt(Instruction):
    opcode = 99
    size = 1

    def execute(self):
        return False


class Add(Instruction):
    opcode = 1
    size = 4

    def execute(self):
        a, b, target = self._params
        target.set(a.get() + b.get())


class Mul(Instruction):
    opcode = 2
    size = 4

    def execute(self):
        a, b, target = self._params
        target.set(a.get() * b.get())


class Input(Instruction):
    _input = input
    opcode = 3
    size = 2

    def __init__(self, params, input_func=None, **kwargs):
        super().__init__(params)
        if input_func:
            self._input = input_func

    def execute(self):
        target = self._params[0]
        target.set(int(self._input()))


class Output(Instruction):
    _out = print
    opcode = 4
    size = 2

    def __init__(self, params, output_func=None, **kwargs):
        super().__init__(params)
        if output_func:
            self._out = output_func

    def execute(self):
        value = self._params[0]
        self._out(value.get())


class Jump(Instruction):
    _jump_to = None

    def ip_adjust(self, ip):
        if self._jump_to is not None:
            return self._jump_to
        return super().ip_adjust(ip)


class JumpIfTrue(Jump):
    opcode = 5
    size = 3

    def execute(self):
        test, target = self._params
        if test.get() != 0:
            self._jump_to = target.get()


class JumpIfFalse(Jump):
    opcode = 6
    size = 3

    def execute(self):
        test, target = self._params
        if test.get() == 0:
            self._jump_to = target.get()


class LessThan(Instruction):
    opcode = 7
    size = 4

    def execute(self):
        a, b, target = self._params
        if a.get() < b.get():
            target.set(1)
        else:
            target.set(0)


class Equal(Instruction):
    opcode = 8
    size = 4

    def execute(self):
        a, b, target = self._params
        if a.get() == b.get():
            target.set(1)
        else:
            target.set(0)


class AdjustRelativeBase(Instruction):
    opcode = 9
    size = 2
    _rb_adjust = 0

    def execute(self):
        (target,) = self._params
        self._rb_adjust = target.get()

    def rb_adjust(self, rb):
        return rb + self._rb_adjust
