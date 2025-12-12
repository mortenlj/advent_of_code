#!/usr/bin/env python
from dataclasses import dataclass

from ibidem.advent_of_code.a_star import a_star
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, Vector, Direction


@dataclass(frozen=True)
class Node:
    pos: Vector
    direction: Direction

    @property
    def current_symbol(self):
        return str(self.direction)

    def neighbors(self, board: Board):
        candidates = [
            Vector(nx, ny)
            for nx, ny in board.adjacent_indexes(
                self.pos.x, self.pos.y, include_diagonal=False
            )
            if board.get(nx, ny) != "#"
        ]
        for direction in Direction:
            n_pos = self.pos + direction
            if n_pos in candidates:
                yield Node(n_pos, direction)

    def cost_to(self, target):
        if isinstance(target, Node):
            target = target.pos
        distance = abs(self.pos.x - target.x) + abs(self.pos.y - target.y)
        vector_to_target = target - self.pos
        if vector_to_target.x != 0 and vector_to_target.y != 0:
            return 1000 + distance
        if self.direction in (Direction.Up, Direction.Down):
            if vector_to_target.x != 0:
                return 1000 + distance
            if vector_to_target.y * self.direction.vector.y < 0:
                return 2000 + distance
        elif self.direction in (Direction.Left, Direction.Right):
            if vector_to_target.y != 0:
                return 1000 + distance
            if vector_to_target.x * self.direction.vector.x < 0:
                return 2000 + distance
        return distance


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def solve(board: Board):
    start_y, start_x = board.find("S")[0]
    goal_y, goal_x = board.find("E")[0]
    start = Node(Vector(start_x, start_y), Direction.East)
    cost, path = a_star(start, Vector(goal_x, goal_y), board)
    return cost, len(path)


if __name__ == "__main__":
    with open(get_input_name(16, 2024)) as fobj:
        p1_result, p2_result = solve(load(fobj))
        print(f"Part 1: {p1_result}")
        print(f"Part 2: {p2_result}")
