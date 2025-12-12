#!/usr/bin/env python

import re
from collections import namedtuple

from vectormath import Vector2

from ibidem.advent_of_code.util import get_input_name

Target = namedtuple("Target", ("upper_left", "lower_right"))

PATTERN = re.compile(r"target area: x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)")


def load(fobj):
    s = fobj.read()
    m = PATTERN.search(s)
    upper_left = Vector2(int(m.group(1)), int(m.group(4)))
    lower_right = Vector2(int(m.group(2)), int(m.group(3)))
    return Target(upper_left, lower_right)


class TooFar(Exception):
    pass


class TooShort(Exception):
    pass


def calculate_highest(vel, target):
    pos = Vector2(0, 0)
    heights = []
    while pos.x <= target.lower_right.x and pos.y >= target.lower_right.y:
        pos += vel
        heights.append(pos.y)
        vel.x = max(vel.x - 1, 0)
        vel.y -= 1
        if (
            target.upper_left.x <= pos.x <= target.lower_right.x
            and target.lower_right.y <= pos.y <= target.upper_left.y
        ):
            return max(heights)
        if vel.x == 0 and pos.x < target.upper_left.x:
            raise TooShort
    if pos.x > target.lower_right.x:
        raise TooFar
    if pos.x < target.upper_left.x:
        raise TooShort
    if pos.y < target.lower_right.y:
        raise TooFar


def part1(target):
    max = 0
    for x in range(1, int(target.lower_right.x)):
        if ((x * (x + 1)) / 2) < target.upper_left.x:
            continue
        for y in range(1, abs(int(target.lower_right.y))):
            try:
                height = calculate_highest(Vector2(x, y), target)
                if height > max:
                    max = height
            except TooFar:
                pass
            except TooShort:
                continue
    return max


def part2(target):
    velocities = []
    for x in range(1, int(target.lower_right.x) + 1):
        for y in range(int(target.lower_right.y), abs(int(target.lower_right.y))):
            try:
                vel = Vector2(x, y)
                calculate_highest(vel.copy(), target)
                velocities.append(vel)
            except TooFar:
                pass
            except TooShort:
                continue
    return len(velocities)


if __name__ == "__main__":
    with open(get_input_name(17, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(17, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
