#!/usr/bin/env python
import re

from ibidem.advent_of_code.util import get_input_name

PATTERN = re.compile(r"(forward|up|down) (\d+)")


def load():
    with open(get_input_name(2, 2021)) as fobj:
        return fobj.read().splitlines(keepends=False)


def part1(commands):
    depth = 0
    horizontal = 0
    for command in commands:
        m = PATTERN.match(command)
        if not m:
            raise RuntimeError(f"Invalid command: {command}")
        cmd = m.group(1)
        value = int(m.group(2))
        if cmd == "forward":
            horizontal += value
        if cmd == "up":
            depth -= value
        if cmd == "down":
            depth += value
    return depth * horizontal


def part2(commands):
    depth = 0
    horizontal = 0
    aim = 0
    for command in commands:
        m = PATTERN.match(command)
        if not m:
            raise RuntimeError(f"Invalid command: {command}")
        cmd = m.group(1)
        value = int(m.group(2))
        if cmd == "forward":
            horizontal += value
            depth += aim * value
        if cmd == "up":
            aim -= value
        if cmd == "down":
            aim += value
    return depth * horizontal


if __name__ == "__main__":
    commands = load()
    result = part1(commands)
    print(f"Part 1: {result}")
    result = part2(commands)
    print(f"Part 2: {result}")
