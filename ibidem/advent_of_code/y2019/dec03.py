#!/usr/bin/env python
# -*- coding: utf-8
import sys

from .board import Board
from .util import get_input_name


def manhattan(pos):
    x, y = pos
    return abs(x) + abs(y)


def part1():
    board = Board(15000, 20000, dtype="<U1")
    with open(get_input_name("dec03")) as fobj:
        wires = []
        for line in fobj:
            wires.append(line.split(","))
    chars = ["E", "O"]
    shortest = sys.maxsize
    step_tracker = {}
    for i, wire in enumerate(wires):
        pos = [0, 0]
        step_tracker[i] = {}
        steps = 0
        for move in wire:
            direction = move[0]
            distance = int(move[1:])
            if direction in ("L", "R"):
                idx = 0
            else:
                idx = 1
            if direction in ("L", "D"):
                factor = -1
            else:
                factor = 1
            for _ in range(distance):
                pos[idx] = pos[idx] + factor
                steps += 1
                step_tracker[i][tuple(pos)] = steps
                if board.set(pos[0], pos[1], chars[i]) not in (" ", chars[i]):
                    board.set(pos[0], pos[1], "X")
                    distance = steps + step_tracker[0][tuple(pos)]
                    if distance < shortest:
                        shortest = distance
    print("Shortest distance is {}".format(shortest))


if __name__ == "__main__":
    part1()
