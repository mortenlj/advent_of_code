#!/usr/bin/env python
import copy
import enum
import operator
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from alive_progress import alive_it

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.board.visualize import Config, Images, visualize
from ibidem.advent_of_code.util import get_input_name


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def __str__(self):
        return _dir_to_str[self]

    def next_step(self, x, y):
        return {
            Direction.UP: (x, y - 1),
            Direction.DOWN: (x, y + 1),
            Direction.LEFT: (x - 1, y),
            Direction.RIGHT: (x + 1, y),
        }[self]


_dir_to_str = {
    Direction.UP: "^",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.RIGHT: ">",
}

_dir_rotate = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}


@dataclass(frozen=True)
class Guard:
    x: int
    y: int
    direction: Direction

    def __str__(self):
        return f"G({self.x}, {self.y}, {self.direction})"

    def rotate(self):
        return Guard(self.x, self.y, _dir_rotate[self.direction])


def load(fobj) -> Board:
    return Board.from_string(fobj.read(), growable=False)


def find_things(board: Board):
    row_obstacles = defaultdict(list)
    col_obstacles = defaultdict(list)
    guard = None
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell == "#":
                row_obstacles[y].append(x)
                col_obstacles[x].append(y)
            if cell == "^":
                guard = Guard(x, y, Direction.UP)
    assert guard is not None
    return row_obstacles, col_obstacles, guard


def distance_to_edge(guard: Guard, board: Board) -> int:
    if guard.direction == Direction.UP:
        return guard.y
    if guard.direction == Direction.DOWN:
        return board.size_y - guard.y - 1
    if guard.direction == Direction.LEFT:
        return guard.x
    if guard.direction == Direction.RIGHT:
        return board.size_x - guard.x - 1
    raise ValueError(f"Unknown direction {guard.direction}")


def find_obstacle(guard, row_obstacles, col_obstacles):
    adjust = 1 if guard.direction in (Direction.UP, Direction.LEFT) else -1
    if guard.direction in (Direction.UP, Direction.DOWN):
        reverse = guard.direction != Direction.DOWN
        op = operator.lt if reverse else operator.gt
        if guard.x in col_obstacles:
            for y in sorted(col_obstacles[guard.x], reverse=reverse):
                if op(y, guard.y):
                    return guard.x, y + adjust
    else:
        reverse = guard.direction != Direction.RIGHT
        op = operator.lt if reverse else operator.gt
        if guard.y in row_obstacles:
            for x in sorted(row_obstacles[guard.y], reverse=reverse):
                if op(x, guard.x):
                    return x + adjust, guard.y


def part1(board: Board):
    _, _, guard = find_things(board)
    viz_config = Config({"#": Images.Obstacle, "1": Images.Stone})
    visualizer = visualize(board, viz_config)
    visualizer.pause()
    while True:
        board.set(guard.x, guard.y, "1")
        new_pos = guard.direction.next_step(guard.x, guard.y)
        if new_pos[0] < 0 or new_pos[1] < 0:
            break
        if new_pos[0] >= board.size_x or new_pos[1] >= board.size_y:
            break
        if board.get(*new_pos) == "#":
            guard = guard.rotate()
            continue
        guard = Guard(*new_pos, guard.direction)
        visualizer.draw_board()
    visualizer.close()
    return board.count("1"), board


def part2(original_board: Board, walked_board: Board):
    _, _, start_guard = find_things(original_board)
    loops = 0
    candidates = np.where(walked_board.grid == "1")
    zipped = list(zip(*candidates))
    bar = alive_it(zipped)
    for y, x in bar:
        bar.title = f"Placing obstacle at ({x}, {y})"
        board = original_board.copy()
        guard = copy.deepcopy(start_guard)
        visited = set()
        board.set(x, y, "O")
        while True:
            board.set(guard.x, guard.y, str(guard.direction))
            new_pos = guard.direction.next_step(guard.x, guard.y)
            if new_pos[0] < 0 or new_pos[1] < 0:
                break
            if new_pos[0] >= board.size_x or new_pos[1] >= board.size_y:
                break
            if guard in visited:
                loops += 1
                bar.text = f"Found loop, loops={loops}"
                break
            visited.add(copy.deepcopy(guard))
            if board.get(*new_pos) in ("#", "O"):
                bar.text = f"{guard} rotating"
                guard = guard.rotate()
                continue
            guard = Guard(*new_pos, guard.direction)
    return loops


if __name__ == "__main__":
    with open(get_input_name(6, 2024)) as fobj:
        p1_result, board = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2024)) as fobj:
        p2_result = part2(load(fobj), board)
        print(f"Part 2: {p2_result}")
