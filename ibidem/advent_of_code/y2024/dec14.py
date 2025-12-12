#!/usr/bin/env python
import re
from dataclasses import dataclass, field

import numpy as np
from rich.progress import track

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name
from ibidem.advent_of_code.visualizer import (
    initialize_and_display_splash,
    Sprites,
    Tiles,
)
from ibidem.advent_of_code.visualizer.board import BoardVisualizer

ROBOT_PATTERN = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class Field:
    tl: list = field(default_factory=list)
    tr: list = field(default_factory=list)
    bl: list = field(default_factory=list)
    br: list = field(default_factory=list)

    def safety_factor(self):
        return len(self.tl) * len(self.tr) * len(self.bl) * len(self.br)


@dataclass
class Vector:
    x: int
    y: int


@dataclass
class Robot:
    position: Vector
    velocity: Vector


def load(fobj, board_x, board_y):
    robots = []
    for line in fobj:
        m = ROBOT_PATTERN.search(line)
        if m:
            robot = Robot(
                Vector(int(m.group(1)), int(m.group(2))),
                Vector(int(m.group(3)), int(m.group(4))),
            )
            robots.append(robot)
    return robots, Board(board_x, board_y, do_translate=False, growable=False)


def part1(input):
    robots, board = input
    mid_x, mid_y, _ = simulate(board, robots, 100)
    field = Field()
    for robot in robots:
        if robot.position.x < mid_x and robot.position.y < mid_y:
            field.tl.append(robot)
        elif robot.position.x < mid_x and robot.position.y > mid_y:
            field.bl.append(robot)
        elif robot.position.x > mid_x and robot.position.y < mid_y:
            field.tr.append(robot)
        elif robot.position.x > mid_x and robot.position.y > mid_y:
            field.br.append(robot)
    return field.safety_factor()


def simulate(board, robots, steps, check=lambda b: False):
    mid_x = board.size_x // 2
    mid_y = board.size_y // 2
    for x in range(board.size_x):
        for y in range(board.size_y):
            if x == mid_x or y == mid_y:
                board.set(x, y, ".")
    blank_board = board.copy()
    visualizer = None
    if visualize:
        initialize_and_display_splash()
        visualizer = BoardVisualizer(
            board, {"#": Sprites.Tank, ".": Tiles.Stone, " ": Tiles.Grass}
        )
        if pause:
            visualizer.pause()
    for step in track(range(steps)):
        board = blank_board.copy()
        for robot in robots:
            robot.position.x = (robot.position.x + robot.velocity.x) % board.size_x
            robot.position.y = (robot.position.y + robot.velocity.y) % board.size_y
            board.set(robot.position.x, robot.position.y, "#")
        if visualizer:
            visualizer.draw_board(board)
        if check(board):
            break
    if pause and visualizer:
        visualizer.pause()
    return mid_x, mid_y, step + 1


def part2(input):
    robots, board = input
    needle = np.array(list("#" * 20))

    def check(board):
        for y in range(board.size_y):
            for x in range(board.size_x - 20):
                if np.array_equal(board.grid[y, x : x + 20], needle):
                    return True

    _, _, step = simulate(board, robots, 10000, check)
    return step


visualize = False
pause = False

if __name__ == "__main__":
    import sys

    if "--visualize" in sys.argv:
        visualize = True
    if "--pause" in sys.argv:
        pause = True
    with open(get_input_name(14, 2024)) as fobj:
        p1_result = part1(load(fobj, 101, 103))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2024)) as fobj:
        p2_result = part2(load(fobj, 101, 103))
        print(f"Part 2: {p2_result}")
