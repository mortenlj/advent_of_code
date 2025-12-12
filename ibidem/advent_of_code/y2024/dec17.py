#!/usr/bin/env python
import enum
from abc import abstractmethod
from dataclasses import dataclass
from itertools import batched

from ibidem.advent_of_code.util import get_input_name, gen_list


class OperandType(enum.Enum):
    Literal = 0
    Combo = 1


class Operand:
    value: int


class LiteralOperand(Operand):
    def __init__(self, value):
        self.value = value


class RegisterOperand(Operand):
    def __init__(self, register):
        self.register = register

    @property
    def value(self):
        return self.register.value


@dataclass
class Register:
    value: int


class Operator:
    opcode: int
    operand_type: OperandType
    machine: "Machine"

    def __init__(self, machine):
        self.machine = machine

    @classmethod
    def parse_operand(cls, operand_code, machine):
        if cls.operand_type == OperandType.Literal:
            return LiteralOperand(operand_code)
        if operand_code < 4:
            return LiteralOperand(operand_code)
        elif operand_code < 7:
            return RegisterOperand(getattr(machine, "abc"[operand_code - 4]))
        else:
            raise ValueError(f"Invalid operand code: {operand_code}")

    @abstractmethod
    def __call__(self, operand):
        raise NotImplementedError


class AdvOperator(Operator):
    opcode = 0
    operand_type = OperandType.Combo

    def __call__(self, operand):
        self.machine.a.value = self.machine.a.value // 2**operand.value
        return self.machine.ip + 1


class BxlOperator(Operator):
    opcode = 1
    operand_type = OperandType.Literal

    def __call__(self, operand):
        self.machine.b.value = self.machine.b.value ^ operand.value
        return self.machine.ip + 1


class BstOperator(Operator):
    opcode = 2
    operand_type = OperandType.Combo

    def __call__(self, operand):
        self.machine.b.value = operand.value % 8
        return self.machine.ip + 1


class JnzOperator(Operator):
    opcode = 3
    operand_type = OperandType.Literal

    def __call__(self, operand):
        if self.machine.a.value != 0:
            return operand.value // 2
        return self.machine.ip + 1


class BxcOperator(Operator):
    opcode = 4
    operand_type = OperandType.Literal

    def __call__(self, _):
        self.machine.b.value = self.machine.b.value ^ self.machine.c.value
        return self.machine.ip + 1


class OutOperator(Operator):
    opcode = 5
    operand_type = OperandType.Combo

    def __call__(self, operand):
        self.machine.output.append(operand.value % 8)
        return self.machine.ip + 1


class BdvOperator(Operator):
    opcode = 6
    operand_type = OperandType.Combo

    def __call__(self, operand):
        self.machine.b.value = self.machine.a.value // 2**operand.value
        return self.machine.ip + 1


class CdvOperator(Operator):
    opcode = 7
    operand_type = OperandType.Combo

    def __call__(self, operand):
        self.machine.c.value = self.machine.a.value // 2**operand.value
        return self.machine.ip + 1


@dataclass
class Operation:
    operator: Operator
    operand: Operand

    def __call__(self):
        return self.operator(self.operand)


class Machine:
    a: Register
    b: Register
    c: Register
    ip: int
    output: list[int]
    _code: list[Operation]

    def __init__(self, a, b, c, program):
        self.a = Register(a)
        self.b = Register(b)
        self.c = Register(c)
        self.output = []
        self._code = self._compile(program)
        self.ip = 0

    @gen_list
    def _compile(self, program):
        opcode_map = {o.opcode: o for o in Operator.__subclasses__()}

        for opcode, operand_code in batched(program, 2):
            operator_cls = opcode_map[opcode]
            operand = operator_cls.parse_operand(operand_code, self)
            yield Operation(operator_cls(self), operand)

    def run(self):
        while self.ip < len(self._code):
            self.ip = self._code[self.ip]()
        return self.output


def load(fobj):
    for line in fobj:
        if line.startswith("Register A: "):
            a = int(line.split()[2])
        elif line.startswith("Register B: "):
            b = int(line.split()[2])
        elif line.startswith("Register C: "):
            c = int(line.split()[2])
        elif line.startswith("Program: "):
            program = [int(i) for i in line.split()[1].split(",")]
    return Machine(a, b, c, program)


def part1(machine: Machine):
    return ",".join((str(v) for v in machine.run()))


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(17, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(17, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
