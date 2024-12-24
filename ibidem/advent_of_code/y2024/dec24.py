#!/usr/bin/env python
import re
from dataclasses import dataclass, field
from typing import Optional

from ibidem.advent_of_code.util import get_input_name

GATE_PATTERN = re.compile(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)")

@dataclass
class Wire:
    name: str
    input: Optional["Gate"] = None
    outputs: list["Gate"] = field(default_factory=list)
    value: Optional[int] = None

    def __repr__(self):
        return f"Wire({self.name}, {self.value})"

    def set(self, value: int):
        self.value = value
        for gate in self.outputs:
            gate.set()


@dataclass
class Gate:
    op: str
    inputs: list[Wire]
    output: Wire

    def set(self):
        if all(wire.value is not None for wire in self.inputs):
            if self.op == "AND":
                self.output.set(self.inputs[0].value & self.inputs[1].value)
            elif self.op == "OR":
                self.output.set(self.inputs[0].value | self.inputs[1].value)
            elif self.op == "XOR":
                self.output.set(self.inputs[0].value ^ self.inputs[1].value)
            else:
                raise ValueError(f"Unknown op: {self.op}")


def load(fobj):
    initial = {}
    gates = []

    reading_gates = False
    for line in fobj:
        line = line.strip()
        if not line:
            reading_gates = True
            continue
        if reading_gates:
            if m := GATE_PATTERN.match(line):
                gates.append(m.groups())
        else:
            k, v = line.split(": ")
            initial[k] = int(v)

    return initial, gates


def part1(input):
    initial, gates = input
    wires = {}
    for in1, op, in2, out in gates:
        if in1 not in wires:
            wires[in1] = Wire(in1)
        if in2 not in wires:
            wires[in2] = Wire(in2)
        if out not in wires:
            wires[out] = Wire(out)
    for in1, op, in2, out in gates:
        gate = Gate(op, [wires[in1], wires[in2]], wires[out])
        wires[in1].outputs.append(gate)
        wires[in2].outputs.append(gate)
        wires[out].input = gate
    for k, v in initial.items():
        wires[k].set(v)
    outputs = [str(wires[k].value) for k in reversed(sorted(wires.keys())) if k.startswith("z")]
    return int("".join(outputs), base=2)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(24, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(24, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
