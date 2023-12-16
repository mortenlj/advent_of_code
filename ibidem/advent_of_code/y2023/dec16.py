#!/usr/bin/env python
from dataclasses import dataclass
from enum import Enum

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


@dataclass(eq=True, frozen=True)
class Beam:
    x: int
    y: int
    direction: Direction


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def handle_up(beam, char):
    match char:
        case "|" | ".":
            return [Beam(beam.x, beam.y - 1, beam.direction)]
        case "-":
            return [Beam(beam.x - 1, beam.y, Direction.LEFT), Beam(beam.x + 1, beam.y, Direction.RIGHT)]
        case "/":
            return [Beam(beam.x + 1, beam.y, Direction.RIGHT)]
        case "\\":
            return [Beam(beam.x - 1, beam.y, Direction.LEFT)]
        case _:
            raise ValueError(f"Invalid character {char!r} at {beam.x}, {beam.y}")


def handle_down(beam, char):
    match char:
        case "|" | ".":
            return [Beam(beam.x, beam.y + 1, beam.direction)]
        case "-":
            return [Beam(beam.x - 1, beam.y, Direction.LEFT), Beam(beam.x + 1, beam.y, Direction.RIGHT)]
        case "/":
            return [Beam(beam.x - 1, beam.y, Direction.LEFT)]
        case "\\":
            return [Beam(beam.x + 1, beam.y, Direction.RIGHT)]
        case _:
            raise ValueError(f"Invalid character {char!r} at {beam.x}, {beam.y}")


def handle_left(beam, char):
    match char:
        case "-" | ".":
            return [Beam(beam.x - 1, beam.y, beam.direction)]
        case "|":
            return [Beam(beam.x, beam.y - 1, Direction.UP), Beam(beam.x, beam.y + 1, Direction.DOWN)]
        case "/":
            return [Beam(beam.x, beam.y + 1, Direction.DOWN)]
        case "\\":
            return [Beam(beam.x, beam.y - 1, Direction.UP)]
        case _:
            raise ValueError(f"Invalid character {char!r} at {beam.x}, {beam.y}")


def handle_right(beam, char):
    match char:
        case "-" | ".":
            return [Beam(beam.x + 1, beam.y, beam.direction)]
        case "|":
            return [Beam(beam.x, beam.y - 1, Direction.UP), Beam(beam.x, beam.y + 1, Direction.DOWN)]
        case "/":
            return [Beam(beam.x, beam.y - 1, Direction.UP)]
        case "\\":
            return [Beam(beam.x, beam.y + 1, Direction.DOWN)]
        case _:
            raise ValueError(f"Invalid character {char!r} at {beam.x}, {beam.y}")


def handle_point(beam, char):
    match beam.direction:
        case Direction.UP:
            return handle_up(beam, char)
        case Direction.DOWN:
            return handle_down(beam, char)
        case Direction.LEFT:
            return handle_left(beam, char)
        case Direction.RIGHT:
            return handle_right(beam, char)


def part1(input: Board):
    start = (Beam(0, 0, Direction.RIGHT))
    return solve(input, start)


def solve(board, start):
    beams = [start]
    seen_beams = set()
    while beams:
        beam = beams.pop()
        if beam in seen_beams:
            continue
        try:
            char = board.get(beam.x, beam.y)
        except IndexError:
            continue
        seen_beams.add(beam)
        beams.extend(handle_point(beam, char))
    return len(set((beam.x, beam.y) for beam in seen_beams))


def part2(input: Board):
    result = 0
    for y in range(input.size_y):
        energized_right = solve(input, Beam(0, y, Direction.RIGHT))
        energized_left = solve(input, Beam(input.size_x - 1, y, Direction.LEFT))
        result = max(result, energized_right, energized_left)
    for x in range(input.size_x):
        energized_down = solve(input, Beam(x, 0, Direction.DOWN))
        energized_up = solve(input, Beam(x, input.size_y - 1, Direction.UP))
        result = max(result, energized_up, energized_down)
    return result


if __name__ == "__main__":
    with open(get_input_name(16, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(16, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
