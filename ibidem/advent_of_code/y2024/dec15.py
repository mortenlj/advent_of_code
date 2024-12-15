#!/usr/bin/env python
import enum
from dataclasses import dataclass

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


class Direction(enum.StrEnum):
    Up = ("^", Vector(0, -1))
    Down = ("v", Vector(0, 1))
    Left = ("<", Vector(-1, 0))
    Right = (">", Vector(1, 0))

    def __new__(cls, symbol: str, vector: Vector):
        obj = str.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.vector = vector
        return obj


class Entity:
    def __init__(self, pos: Vector):
        self.pos = pos

    def gps(self):
        return self.pos.x + self.pos.y * 100


class Robot(Entity):
    def __init__(self, pos: Vector, moves: list[Direction]):
        super().__init__(pos)
        self.moves = moves


class Box(Entity):
    def __init__(self, pos: Vector):
        super().__init__(pos)


class EntityTracker:
    def __init__(self, board: Board, entities: dict[Vector, Entity]):
        self.board = board
        self.entities = entities

    def move(self, entity: Entity, direction: Direction):
        old_pos = entity.pos
        assert old_pos in self.entities, "Entity not found at expected position"
        new_pos = entity.pos + direction.vector
        if self.board.get(new_pos.x, new_pos.y) == "#":
            return False
        if new_pos not in self.entities or self.move(self.entities[new_pos], direction):
            del self.entities[old_pos]
            entity.pos = new_pos
            self.entities[new_pos] = entity
            return True
        return False


def load(fobj):
    board_lines = []
    move_lines = []
    reading_board = True
    for line in fobj:
        if not line.strip():
            reading_board = False
            continue
        if reading_board:
            board_lines.append(line.strip())
        else:
            move_lines.append(line.strip())
    return (
        Board.from_string("\n".join(board_lines), fill_value=".", growable=False),
        [Direction(move) for move in "".join(move_lines)]
    )


def extract_entities(board: Board, moves: list[Direction]) -> tuple[Robot, dict[Vector, Box]]:
    """Extract robot and boxes and remove them from the board in-place"""
    boxes = {}
    for y in range(board.size_y):
        for x in range(board.size_x):
            pos = Vector(x, y)
            if board.get(x, y) == "@":
                robot = Robot(pos, moves)
                board.set(x, y, board._fill_value)
            elif board.get(x, y) == "O":
                boxes[pos] = Box(pos)
                board.set(x, y, board._fill_value)
    return robot, boxes


def part1(input):
    board, moves = input
    robot, boxes = extract_entities(board, moves)
    entities = {robot.pos: robot, **boxes}
    tracker = EntityTracker(board, entities)
    for move in moves:
        tracker.move(robot, move)
    return sum(box.gps() for box in boxes.values())


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(15, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
