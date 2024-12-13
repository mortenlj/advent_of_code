#!/usr/bin/env python
import enum
import re
from collections import deque
from dataclasses import dataclass
from functools import lru_cache

from ibidem.advent_of_code.util import get_input_name


class ButtonPress(enum.Enum):
    A = 3
    B = 1


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass(frozen=True)
class ClawMachine:
    button_a: Vector
    button_b: Vector
    prize: Coordinate
    _cache: dict[Coordinate, list[ButtonPress]]

    _button_pattern = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    _prize_pattern = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    @classmethod
    def load(cls, input):
        line = next(input)
        m = cls._button_pattern.search(line)
        button_a = Vector(int(m.group(1)), int(m.group(2)))

        line = next(input)
        m = cls._button_pattern.search(line)
        button_b = Vector(int(m.group(1)), int(m.group(2)))

        line = next(input)
        m = cls._prize_pattern.search(line)
        prize = Coordinate(int(m.group(1)), int(m.group(2)))

        return cls(button_a, button_b, prize, {})

    def solve(self):
        presses = self._solve(self.prize)
        if presses is not None:
            return sum(p.value for p in presses)
        return None

    def _solve(self, target, depth=0):
        if target in self._cache:
            return self._cache[target]
        if target.x == 0 and target.y == 0:
            return []
        if target.x < 0 or target.y < 0:
            return None
        if depth > 200:
            return None

        result = None
        result_cost = float("inf")
        for press, button in ((ButtonPress.A, self.button_a), (ButtonPress.B, self.button_b)):
            presses = self._solve(target - button, depth + 1)
            if presses is not None:
                presses = presses + [press]
                presses_cost = sum(p.value for p in presses)
                if result is None or presses_cost < result_cost:
                    result = presses
                    result_cost = presses_cost
        self._cache[target] = result
        return result


def load(fobj):
    lines = iter(fobj)
    machines = []
    try:
        while True:
            machines.append(ClawMachine.load(lines))
            next(lines)
    except StopIteration:
        pass
    return machines


def part1(machines: list[ClawMachine]):
    sum = 0
    for machine in machines:
        cost = machine.solve()
        if cost is not None:
            sum += cost
    return sum


def part2(machines):
    return None


if __name__ == "__main__":
    with open(get_input_name(13, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(13, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
