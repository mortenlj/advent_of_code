#!/usr/bin/env python

from collections import namedtuple
from enum import Enum

import numpy as np

from ibidem.advent_of_code.util import get_input_name

Command = namedtuple("Command", ("action", "value"))


class Boat:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction


class Direction(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

    def d(self):
        return np.array(self.value)

    def next(self):
        members = list(self.__class__)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

    def prev(self):
        members = list(self.__class__)
        index = members.index(self) - 1
        return members[index]


class Action(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"

    def direction(self):
        return np.array(Direction[self.name].value)


def load():
    with open(get_input_name(12, 2020)) as fobj:
        commands = []
        for line in fobj:
            line = line.strip()
            commands.append(Command(Action(line[0]), int(line[1:])))
        return commands


def part1(commands):
    boat = Boat(np.array((0, 0)), Direction.EAST)
    for command in commands:
        if command.action == Action.LEFT:
            turns = command.value // 90
            for _ in range(turns):
                boat.direction = boat.direction.prev()
        elif command.action == Action.RIGHT:
            turns = command.value // 90
            for _ in range(turns):
                boat.direction = boat.direction.next()
        elif command.action == Action.FORWARD:
            distance = command.value
            boat.pos += boat.direction.d() * distance
        else:
            distance = command.value
            boat.pos += command.action.direction() * distance
    result = abs(boat.pos[0]) + abs(boat.pos[1])
    print(f"Manhattan distance is {result}")
    return result


def part2():
    pass


if __name__ == "__main__":
    commands = load()
    part1(commands)
    part2()
