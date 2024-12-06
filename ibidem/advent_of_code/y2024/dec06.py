#!/usr/bin/env python
import enum
import operator
from collections import defaultdict
from dataclasses import dataclass

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def __str__(self):
        return {
            Direction.UP: "^",
            Direction.DOWN: "v",
            Direction.LEFT: "<",
            Direction.RIGHT: ">",
        }[self]


@dataclass
class Guard:
    x: int
    y: int
    direction: Direction

    def __str__(self):
        return f"G({self.x}, {self.y}, {self.direction})"

    def rotate(self):
        self.direction = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }[self.direction]


def load(fobj) -> Board:
    return Board.from_string(fobj.read(), growable=False)


def find_things(board: Board):
    row_obstacles = defaultdict(list)
    col_obstacles = defaultdict(list)
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell == "#":
                row_obstacles[y].append(x)
                col_obstacles[x].append(y)
            if cell == "^":
                guard = Guard(x, y, Direction.UP)
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


def part1(board:Board):
    _, _, guard = find_things(board)
    while True:
        board.set(guard.x, guard.y, "1")
        new_pos = {
            Direction.UP: (guard.x, guard.y - 1),
            Direction.DOWN: (guard.x, guard.y + 1),
            Direction.LEFT: (guard.x - 1, guard.y),
            Direction.RIGHT: (guard.x + 1, guard.y),
        }[guard.direction]
        if new_pos[0] < 0 or new_pos[1] < 0:
            break
        if new_pos[0] >= board.size_x or new_pos[1] >= board.size_y:
            break
        if board.get(*new_pos) == "#":
            guard.rotate()
            continue
        guard.x, guard.y = new_pos
    return board.count("1")


def part1_clever(board: Board):
    row_obstacles, col_obstacles, guard = find_things(board)
    board.grid[guard.y][guard.x] = "1"
    new_pos = find_obstacle(guard, row_obstacles, col_obstacles)
    while new_pos is not None:
        if guard.x == new_pos[0]:
            min_y = min(guard.y, new_pos[1])
            max_y = max(guard.y, new_pos[1]) + 1
            board.grid[min_y:max_y, guard.x] = "1"
        else:
            min_x = min(guard.x, new_pos[0])
            max_x = max(guard.x, new_pos[0]) + 1
            board.grid[guard.y, min_x:max_x] = "1"
        guard.x, guard.y = new_pos
        guard.rotate()
        new_pos = find_obstacle(guard, row_obstacles, col_obstacles)
    visited = board.count("1")
    visited += distance_to_edge(guard, board)
    return visited


def part2(board: Board):
    return None


if __name__ == "__main__":
    with open(get_input_name(6, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(6, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
