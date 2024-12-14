#!/usr/bin/env python
import enum
import re
from dataclasses import dataclass

import sympy as sp

from ibidem.advent_of_code.util import get_input_name


class ButtonCost(enum.Enum):
    A = 3
    B = 1


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class ClawMachine:
    button_a: Vector
    button_b: Vector
    prize: Vector
    _cache: dict[Vector, list[ButtonCost]]

    _button_pattern = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    _prize_pattern = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    @classmethod
    def load(cls, input, adjust=False):
        line = next(input)
        m = cls._button_pattern.search(line)
        button_a = Vector(int(m.group(1)), int(m.group(2)))

        line = next(input)
        m = cls._button_pattern.search(line)
        button_b = Vector(int(m.group(1)), int(m.group(2)))

        line = next(input)
        m = cls._prize_pattern.search(line)
        prize_x = int(m.group(1))
        price_y = int(m.group(2))
        if adjust:
            prize_x += 10000000000000
            price_y += 10000000000000
        prize = Vector(prize_x, price_y)

        return cls(button_a, button_b, prize, {})

    def solve_sympy(self):
        a, b = sp.symbols("a b", integer=True, positive=True)
        eq1 = sp.Eq(a * self.button_a.x + b * self.button_b.x, self.prize.x)
        eq2 = sp.Eq(a * self.button_a.y + b * self.button_b.y, self.prize.y)
        sol = sp.solve((eq1, eq2), (a, b))
        if sol:
            return sol[a] * ButtonCost.A.value + sol[b] * ButtonCost.B.value


def load(fobj, adjust=False):
    lines = iter(fobj)
    machines = []
    try:
        while True:
            machines.append(ClawMachine.load(lines, adjust))
            next(lines)
    except StopIteration:
        pass
    return machines


def part1(machines: list[ClawMachine]):
    sum = 0
    for machine in machines:
        cost = machine.solve_sympy()
        if cost is not None:
            sum += cost
    return sum


def part2(machines):
    sum = 0
    for machine in machines:
        cost = machine.solve_sympy()
        if cost is not None:
            sum += cost
    return sum


if __name__ == "__main__":
    with open(get_input_name(13, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(13, 2024)) as fobj:
        p2_result = part2(load(fobj, adjust=True))
        print(f"Part 2: {p2_result}")
